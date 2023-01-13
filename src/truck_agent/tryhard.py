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
