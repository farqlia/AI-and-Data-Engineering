from dataclasses import dataclass


@dataclass
class CoffeeType:
    name: str
    needs_milk: bool
    water_use: float


latte = CoffeeType("latte", True, 0.2)
espresso = CoffeeType("espresso", False, 0.1)