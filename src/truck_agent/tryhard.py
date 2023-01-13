#%%

from api import CargoOffer

data = {
    "uid": 100,
    "origin": "Zaragoza",
    "dest": "Innsbruck",
    "name": "Fruits",
    "price": 1778.0,
    "eta_to_cargo": 8.16,
    "km_to_cargo": 780.0,
    "km_to_deliver": 2730.0,
    "eta_to_deliver": 27.76,
}

offer = CargoOffer(**data)
diesel_price = 2.023
diesel_consumption = 25


def calculate_profit(offer: CargoOffer):
    cost = offer.km_to_cargo * diesel_price * (diesel_consumption / 100)
    return offer.price - cost


calculate_profit(offer)

#%%

import json

with open("map.json", "r") as infile:
    map_data = json.load(infile)

map_data

import networkx as nx

graph = nx.Graph()

for city in map_data:
    for destination in city["roads"]:
        graph.add_edge(
            city["city"],
            destination["dest"],
            km=destination["km"],
            kmh=destination["kmh"],
        )

#%%

graph["Berlin"]["Hamburg"]


#%%

nx.shortest_path_length(graph, "Berlin", "Naples", weight="km")


#%%
import pandas as pd


def get_centrality_measures(graph):
    centrality_measures = pd.DataFrame()
    for measure in (
        nx.betweenness_centrality,
        nx.closeness_centrality,
        nx.degree_centrality,
    ):
        measure_result = measure(graph)
        centrality_measures[str(measure.__name__)] = pd.Series(measure_result)
    return centrality_measures


graph_info = get_centrality_measures(graph)

graph_info.sort_values("betweenness_centrality", ascending=False)


#%%
from api import *

diesel_price = 2.023
diesel_consumption = 25


def calculate_profit(offer: CargoOffer):
    cost = offer.km_to_cargo * diesel_price * (diesel_consumption / 100)
    return (offer.price - cost) / offer.eta_to_deliver


with open("tests/sample_decide_0.json", "r") as infile:
    offer_data = json.load(infile)

request = DecideRequest(**offer_data)
best_cities = ["Berlin", "Warsaw", "Vienna", "Milan", "Munich"]


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

        return DecideResponse(command="DELIVER", argument=best_offer.uid)

    elif command == "ROUTE":

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


request.offers = []
decide(request)

# %%
