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

for node in graph.nodes:
    graph.add_node(node, observed_values=[])

graph.nodes["Berlin"]

#%%

graph.add_node("Berlin", observed_values=[])


#%%

graph["Berlin"]


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


def get_profit_for_offer(offer):
    distance = offer.km_to_deliver - offer.km_to_cargo
    cost = distance * diesel_price * (diesel_consumption / 100)
    return (offer.price - cost) / (offer.eta_to_deliver - offer.eta_to_cargo)


def calculate_profit(offer: CargoOffer):
    cost = offer.km_to_cargo * diesel_price * (diesel_consumption / 100)
    return (offer.price - cost) / offer.eta_to_deliver


def decide(req: DecideRequest) -> DecideResponse:
    """
    See https://app.swaggerhub.com/apis-docs/walter-group/walter-group-hackathon-sustainable-logistics/1.0.0 for
    a detailed description of this endpoint.
    """

    if req.offers:
        command = "DELIVER"
    else:
        command = "ROUTE"

    for offer in req.offers:
        profit = get_profit_for_offer(offer)
        graph.nodes[offer.origin]["observed_values"].append(profit)

    ##########################################
    if command == "DELIVER":

        best_profit = 0
        best_offer = None
        for offer in req.offers:

            profit = calculate_profit(offer)

            if graph.nodes[offer.dest]["observed_values"]:
                print("taking observed values")
                observed = graph.nodes[offer.dest]["observed_values"]
                profit = 0.8 * profit + 0.2 * (sum(observed) / len(observed))

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


# request.offers = []
decide(request)

# %%


def get_profit_for_offer(offer):
    distance = offer.km_to_deliver - offer.km_to_cargo
    cost = distance * diesel_price * (diesel_consumption / 100)
    return (offer.price - cost) / (offer.eta_to_deliver - offer.eta_to_cargo)


#%%
graph.nodes["Berlin"]["observed_values"].append(100)
graph.nodes["Berlin"]

#%%

all_profits = []
for offer in request.offers:
    profit = get_profit_for_offer(offer)
    all_profits.append((profit, offer.origin))
    graph.nodes[offer.origin]["observed_values"].append(profit)

all_profits

#%%

graph.nodes["Valencia"]


#%%

diesel_price = 2.023
diesel_consumption_full = 23
diesel_consumption_empty = 14


def calculate_profit(offer: CargoOffer):
    empty = offer.km_to_cargo
    full = offer.km_to_deliver - offer.km_to_cargo
    cost_empty = empty * diesel_price * (diesel_consumption_empty / 100)
    cost_full = full * diesel_price * (diesel_consumption_full / 100)
    return (offer.price - cost_empty - cost_full) / offer.eta_to_deliver


calculate_profit(request.offers[2])


#%%

preferred_routes = []
for city in map_data:
    for dest in city["roads"]:
        if dest["major"]:
            preferred_routes.append((city["city"], dest["dest"]))
preferred_routes
