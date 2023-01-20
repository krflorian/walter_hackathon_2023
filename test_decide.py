#%%

from src.truck_agent.api import DecideRequest, DecideResponse
from src.truck_agent.deliver import deliver
from src.truck_agent.route import update_graph, route

import json

#%%


def decide(req: DecideRequest) -> DecideResponse:
    """
    See https://app.swaggerhub.com/apis-docs/walter-group/walter-group-hackathon-sustainable-logistics/1.0.0 for
    a detailed description of this endpoint.
    deploy
    """

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


#%%

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

#%%


import json
import pandas as pd
import plotly.express as xp

# initialize graph
with open("map.json", "r") as infile:
    map_data = json.load(infile)

cities = pd.DataFrame(
    [{k: v for k, v in city.items() if k != "roads"} for city in map_data]
)
cities.sort_values("population", ascending=False)


xp.scatter(cities, x="lng", y="lat", hover_data=["country", "population", "city"])

#%%
