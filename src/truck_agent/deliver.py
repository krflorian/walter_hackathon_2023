from .api import CargoOffer

diesel_price = 2.023
diesel_consumption_full = 23
diesel_consumption_empty = 14


def get_profit_for_offer(offer: CargoOffer):
    distance = offer.km_to_deliver - offer.km_to_cargo
    time = offer.eta_to_deliver - offer.eta_to_cargo

    cost = distance * diesel_price * (diesel_consumption_full / 100)

    return (offer.price - cost) / time


def calculate_profit(offer: CargoOffer):

    empty = offer.km_to_cargo
    full = offer.km_to_deliver - offer.km_to_cargo

    cost_empty = empty * diesel_price * (diesel_consumption_empty / 100)
    cost_full = full * diesel_price * (diesel_consumption_full / 100)

    profit = (offer.price - cost_empty - cost_full) / offer.eta_to_deliver

    if empty <= 10:
        return profit
    else:
        return profit - (cost_empty / offer.eta_to_cargo)


def deliver(offers, graph):

    best_profit = 0
    best_offer = None
    offers = sorted(offers, key=lambda x: x.eta_to_cargo)[:-5]

    for offer in offers:

        profit = calculate_profit(offer)

        if graph.nodes[offer.dest]["observed_values"]:
            observed = graph.nodes[offer.dest]["observed_values"]
            profit = 0.9 * profit + 0.1 * (sum(observed) / len(observed))

        if profit > best_profit:
            best_profit = profit
            best_offer = offer

    if best_profit <= 10:
        print("no offer fits parameters")
        return None
    else:
        print("profit", best_profit)
        print(best_offer)
        return best_offer.uid
