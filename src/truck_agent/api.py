"""
Data types that are passed to the agents and expected in return
"""
from typing import List, Dict, Literal, Union
from pydantic import BaseModel


# Request and response

class CargoOffer(BaseModel):
    uid: int  # unique cargo id
    origin: str
    dest: str
    name: str
    price: float  # how much do you get for the cargo
    eta_to_cargo: float
    km_to_cargo: float
    km_to_deliver: float
    eta_to_deliver: float


class TruckState(BaseModel):
    balance: float
    uid: int
    loc: str
    hours_since_full_rest: float
    time: float


class DecideRequest(BaseModel):
    truck: TruckState
    offers: List[CargoOffer]


class DecideResponse(BaseModel):
    command: Literal["ROUTE", "DELIVER", "SLEEP"]
    argument: Union[str, int, None] = None

# The world map can be downloaded by a truck agent from https://github.com/WALTER-GROUP/hackathon-sustainable-logistics/blob/main/data/map.json during a simulation run.
# It is not required to download it, but a team might be able to get some useful  information from the map to optimize their truck agents decisions.
# To make individual decide requests as fast as possible, it is better to download the map at the very beginning, when the agent starts up,
# otherwise the simulation might decide that the truck is reacting too slow and exclude it from the current simulation run.

class Road(BaseModel):
    dest: str
    km: float
    kmh: float
    major: bool

class Location(BaseModel):
    city: str
    country: str
    lat: float
    lng: float
    population: int
    roads: List[Road]
