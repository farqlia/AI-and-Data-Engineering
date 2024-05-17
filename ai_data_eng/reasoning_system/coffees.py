from dataclasses import dataclass

HEATING_TEMPERATURE = 70
SCALE_AMOUNT = 0.1


@dataclass
class CoffeeType:
    name: str
    milk_use: float
    water_use: float
    beans_use: float


latte = CoffeeType("latte", 0.3, 0.3, 0.1)
flat_white = CoffeeType("flat white", 0.2, 0.3, 0.2)
espresso = CoffeeType("espresso", 0.0, 0.1, 0.2)

