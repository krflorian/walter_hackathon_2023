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

    return (offer.price - cost_empty) / offer.eta_to_deliver


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

    current_time = req.truck.time % 24
    if (20 < current_time < 24) or (0 < current_time < 5):
        return DecideResponse(command="SLEEP", argument=8)

    ##########################################
    if command == "DELIVER":

        best_profit = 0
        best_offer = None

        choose_offers = []
        for offer in req.offers:

            path = nx.shortest_path(graph, req.truck.loc, offer.origin)
            path_full = nx.shortest_path(graph, offer.origin, offer.dest)

            path.extend(path_full[1:])

            kmh = []
            origin = path[0]
            for city in path[1:]:
                kmh.append(graph[origin][city]["kmh"])
                origin = city
            if sum(kmh) / len(kmh) > 90:
                choose_offers.append(offer)

        for offer in choose_offers:

            profit = calculate_profit(offer)
            time_at_cargo = (req.truck.time + offer.eta_to_cargo) % 24
            # rest_at_cargo = req.truck.hours_since_full_rest + offer.eta_to_cargo

            if 5 < time_at_cargo < 22:
                profit = profit
            else:
                profit = profit * 0.8

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


major_roads = [
    ("Berlin", "Hamburg"),
    ("Berlin", "Copenhagen"),
    ("Berlin", "Vienna"),
    ("Berlin", "Munich"),
    ("Berlin", "Warsaw"),
    ("Madrid", "Barcelona"),
    ("Madrid", "Brussels"),
    ("Madrid", "Paris"),
    ("Rome", "Munich"),
    ("Rome", "Naples"),
    ("Rome", "Milan"),
    ("Paris", "Barcelona"),
    ("Paris", "Brussels"),
    ("Paris", "Madrid"),
    ("Paris", "Cologne"),
    ("Bucharest", "Budapest"),
    ("Bucharest", "Sofia"),
    ("Bucharest", "Warsaw"),
    ("Warsaw", "Berlin"),
    ("Warsaw", "Vienna"),
    ("Warsaw", "Budapest"),
    ("Warsaw", "Bucharest"),
    ("Hamburg", "Brussels"),
    ("Hamburg", "Berlin"),
    ("Hamburg", "Copenhagen"),
    ("Hamburg", "Cologne"),
    ("Budapest", "Sofia"),
    ("Budapest", "Vienna"),
    ("Budapest", "Warsaw"),
    ("Budapest", "Bucharest"),
    ("Vienna", "Berlin"),
    ("Vienna", "Sofia"),
    ("Vienna", "Munich"),
    ("Vienna", "Warsaw"),
    ("Vienna", "Naples"),
    ("Vienna", "Budapest"),
    ("Barcelona", "Madrid"),
    ("Barcelona", "Paris"),
    ("Barcelona", "Milan"),
    ("Sofia", "Budapest"),
    ("Sofia", "Vienna"),
    ("Sofia", "Bucharest"),
    ("Munich", "Berlin"),
    ("Munich", "Vienna"),
    ("Munich", "Rome"),
    ("Munich", "Milan"),
    ("Milan", "Barcelona"),
    ("Milan", "Munich"),
    ("Milan", "Naples"),
    ("Milan", "Cologne"),
    ("Milan", "Rome"),
    ("Copenhagen", "Hamburg"),
    ("Copenhagen", "Berlin"),
    ("Copenhagen", "Cologne"),
    ("Brussels", "Madrid"),
    ("Brussels", "Hamburg"),
    ("Brussels", "Paris"),
    ("Brussels", "Cologne"),
    ("Naples", "Vienna"),
    ("Naples", "Rome"),
    ("Naples", "Milan"),
    ("Cologne", "Brussels"),
    ("Cologne", "Hamburg"),
    ("Cologne", "Copenhagen"),
    ("Cologne", "Paris"),
    ("Cologne", "Milan"),
]


def main():
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
