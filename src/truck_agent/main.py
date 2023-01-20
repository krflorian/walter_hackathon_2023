from fastapi import FastAPI
import uvicorn

from .api import *
from .deliver import deliver
from .route import route, update_graph

app = FastAPI()


@app.post("/decide", response_model=DecideResponse)
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


def main():
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")


if __name__ == "__main__":
    main()
