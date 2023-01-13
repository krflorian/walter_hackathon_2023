from fastapi import FastAPI
import uvicorn
from .api import *

app = FastAPI()

diesel_price = 2.023
diesel_consumption = 25


def calculate_profit(offer: CargoOffer):
    cost = offer.km_to_cargo * diesel_price * (diesel_consumption / 100)
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

        return DecideResponse(command="DELIVER", argument=best_offer.uid)
    elif command == "ROUTE":

        return DecideResponse(command="ROUTE", argument="Berlin")
    else:

        return DecideResponse(command="SLEEP", argument=1)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
