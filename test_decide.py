#%%

from src.truck_agent.api import DecideRequest, DecideResponse
from src.truck_agent.deliver import deliver
from src.truck_agent.route import update_graph, route, graph

import json


def decide(req: DecideRequest):

    graph = update_graph(offers=req.offers)

    if req.offers:

        offer_id = deliver(req.offers, graph)
        if offer_id is not None:
            return DecideResponse(command="DELIVER", argument=offer_id)

    city = route(req.truck)
    if city is not None:
        if not city == req.truck.loc:
            return DecideResponse(command="ROUTE", argument=city)

    return DecideResponse(command="SLEEP", argument=8)


for i in range(4):

    filename = f"sample_decide_{i}"
    with open(f"tests/{filename}.json", "r") as infile:
        data = json.load(infile)
        req = DecideRequest(**data)

        print("________________________")
        print(f"{i}: ", req.truck.loc)
        response = decide(req)
        print(response)


#%%

import pandas as pd
import networkx as nx


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

graph_info.sort_values("closeness_centrality", ascending=False)

