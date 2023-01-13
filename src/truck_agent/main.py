from fastapi import FastAPI
import uvicorn
from .api import *
import networkx as nx
import json

with open("map.json", "r") as infile:
    map_data = json.load(infile)

app = FastAPI()

graph = nx.Graph()

for city in map_data:
    for destination in city["roads"]:
        graph.add_edge(
            city["city"],
            destination["dest"],
            km=destination["km"],
            kmh=destination["kmh"],
        )

for node in graph.nodes:
    graph.add_node(node, observed_values=[])

best_cities = ["Berlin", "Warsaw", "Vienna", "Milan", "Munich"]

pickup_time_ranking = [5, 9, 13, 17, 20]


def driver_rested_at_cargo(truck: TruckState, offer: CargoOffer):

    hours_since_full_rest = truck.hours_since_full_rest + offer.eta_to_cargo
    if hours_since_full_rest > 8:
        return False
    else:
        return True


diesel_price = 2.023
diesel_consumption_full = 22
diesel_consumption_empty = 15


def get_profit_for_offer(offer: CargoOffer):
    distance = offer.km_to_deliver - offer.km_to_cargo
    cost = distance * diesel_price * (diesel_consumption_full / 100)
    return (offer.price - cost) / (offer.eta_to_deliver - offer.eta_to_cargo)


def calculate_profit(offer: CargoOffer):

    empty = offer.km_to_cargo
    full = offer.km_to_deliver - offer.km_to_cargo

    cost_empty = empty * diesel_price * (diesel_consumption_empty / 100)
    cost_full = full * diesel_price * (diesel_consumption_full / 100)

    return (offer.price - cost_empty - cost_full) / offer.eta_to_deliver


@app.post("/decide", response_model=DecideResponse)
def decide(req: DecideRequest) -> DecideResponse:
    """
    See https://app.swaggerhub.com/apis-docs/walter-group/walter-group-hackathon-sustainable-logistics/1.0.0 for
    a detailed description of this endpoint.
    """

    if req.offers:
        command = "DELIVER"
    else:
        command = "ROUTE"

    """
    for offer in req.offers:
        profit = get_profit_for_offer(offer)
        if profit > 0:
            graph.nodes[offer.origin]["observed_values"].append(profit)
    """

    current_time = req.truck.time % 24
    if (20 < current_time % 24 < 24) or (0 < current_time % 24 < 5):
        if req.truck.hours_since_full_rest > 12:
            return DecideResponse(command="SLEEP", argument=8)

    ##########################################
    if command == "DELIVER":

        best_profit = 0
        best_offer = None
        for offer in req.offers:

            profit = calculate_profit(offer)
            time_at_cargo = (req.truck.time + offer.eta_to_cargo) % 24

            # if time_at_cargo

            if profit > best_profit:
                best_profit = profit
                best_offer = offer

        if best_profit == 0:
            command = "ROUTE"
        else:
            return DecideResponse(command="DELIVER", argument=best_offer.uid)

    current_loc = req.truck.loc
    best_distance = 1000000
    next_city = ""
    for city in best_cities:
        distance = nx.shortest_path_length(graph, current_loc, city, weight="km")
        if distance < best_distance:
            next_city = city
            best_distance = distance

    return DecideResponse(command="ROUTE", argument=next_city)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
