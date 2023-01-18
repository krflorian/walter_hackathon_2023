import json
import networkx as nx
import pandas as pd

from .api import TruckState, CargoOffer
from .deliver import get_profit_for_offer

best_cities = ["Berlin", "Warsaw", "Vienna", "Milan", "Munich", "Brussels", "Cologne"]


with open("map.json", "r") as infile:
    map_data = json.load(infile)

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


def update_graph(offers: list[CargoOffer]):

    for offer in offers:
        profit = get_profit_for_offer(offer)
        graph.nodes[offer.origin]["observed_values"].append(profit)

    return graph


def route(truck: TruckState):

    best_distance = 1000000
    next_city = ""

    for city in best_cities:
        distance = nx.shortest_path_length(graph, truck.loc, city, weight="km")
        if distance < best_distance:
            next_city = city
            best_distance = distance

    return next_city


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
