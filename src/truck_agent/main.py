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


diesel_price = 2.023
diesel_consumption = 20


def calculate_profit(offer: CargoOffer):
    cost = offer.km_to_deliver * diesel_price * (diesel_consumption / 100)
    return (offer.price - cost) / offer.eta_to_deliver


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

    ##########################################
    if command == "DELIVER":

        best_profit = 0
        best_offer = None
        for offer in req.offers:
            profit = calculate_profit(offer)
            if profit > best_profit:
                best_profit = profit
                best_offer = offer

        if best_profit == 0:
            command = "ROUTE"

        return DecideResponse(command="DELIVER", argument=best_offer.uid)

    if command == "ROUTE":

        current_loc = req.truck.loc
        best_distance = 100000
        next_city = ""
        for city in best_cities:
            distance = nx.shortest_path_length(graph, current_loc, city, weight="km")
            if distance < best_distance:
                next_city = city
                best_distance = distance

        return DecideResponse(command="ROUTE", argument=next_city)
    else:

        return DecideResponse(command="SLEEP", argument=1)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
