from dataclasses import dataclass


@dataclass
class CoffeeType:
    name: str
    milk_use: float
    water_use: float


latte = CoffeeType("latte", 0.3, 0.3)
flat_white = CoffeeType("flat white", 0.2, 0.3)
espresso = CoffeeType("espresso", 0.0, 0.1)