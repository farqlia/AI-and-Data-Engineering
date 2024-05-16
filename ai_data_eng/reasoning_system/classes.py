from enum import Enum
from typing import Optional

import schema as s
from experta import *
from experta.fact import *

from ai_data_eng.reasoning_system.coffees import *


class Actions(Enum):
    MAKE_COFFEE = "make coffee"
    FILL_WATER = "fill water"
    SHOW_FACTS = "show facts"
    CONSERVE = "conserve"
    STOP = "stop"


actions = [Actions.MAKE_COFFEE, Actions.FILL_WATER, Actions.SHOW_FACTS, Actions.CONSERVE, Actions.STOP]


class CoffeeMachine(Fact):
    """A fact representing the coffee machine."""
    pass


def from_type(coffee_type: CoffeeType):
    return Coffee(name=coffee_type.name,
                  water_use=coffee_type.water_use,
                  milk_use=coffee_type.milk_use)


class Coffee(Fact):
    milk_use = Field(s.And(s.Use(float), lambda l: 0.0 <= l <= 1.0), default=0.0)
    water_use = Field(s.And(s.Use(float), lambda l: 0.0 <= l <= 1.0), default=0.2)
    name = Field(str, mandatory=True)


coffees = [latte, espresso, flat_white]


class Component(Fact):
    """A fact representing a component of the coffee machine."""
    pass


class Water(Component):
    """A fact representing the water component."""
    level = Field(s.And(s.Use(float), lambda l: 0.0 <= l <= 1.0), default=1.0)
    # This should be set at the beginning
    water_hardness = Field(s.Or("soft", "medium", "hard"), default="medium")


class Milk(Component):
    """A fact representing the milk component."""
    level = Field(s.And(s.Use(float), lambda l: 0.0 <= l <= 1.0), default=1.0)
    # Add state here too?


class Grinder(Component):
    """A fact representing the grinder component."""
    filled = Field(bool, default=False)
    state = Field(s.Or("grinding", "inactive", "glitch"), default="inactive")
    degree = Field(s.And(s.Use(int), lambda x: 1 <= x <= 5), default=1)


class Heater(Component):
    """A fact representing the heater component."""
    temperature = Field(s.And(s.Use(int), lambda x: 0 <= x < 100), default=0)
    upper_threshold = 80


class Brew(Fact):
    """A fact representing the brewing process."""
    status = Field(s.And(s.Use(str), s.Or("ready", "making", "done")))


class Nozzle(Component):
    """A fact representing the nozzle for dispensing coffee."""
    status = Field(s.Or("blocked", "nozzling", "inactive"), default="inactive")


def get_user_coffee() -> Optional[Coffee]:
    print("Choose coffee")
    for i, coffee in enumerate(coffees):
        print(f"[{i}] {coffee.name}")
    cof = int(input("Choice: "))
    return from_type(coffees[cof]) if 0 <= cof < len(coffees) else None


def get_user_input() -> Actions:
    print("Choose from a set of possible actions")
    for i, action in enumerate(actions):
        print(f"[{i}] {action.value}")
    act = int(input("Choice: "))
    return actions[act] if 0 <= act < len(actions) else Actions.STOP


class UserInput(Fact):
    """A fact representing user input for the coffee machine."""
    # user can choose coffee, hot water or ex. system conservation
    action = Field(s.Or(*actions))


class CoffeeMachineRules(KnowledgeEngine):
    """The rule-based system for the coffee machine."""

    @DefFacts()
    def startup(self):
        print("Coffee machine started.")
        yield CoffeeMachine()
        yield Grinder(filled=True)
        yield Milk(amount=1.0)
        yield Water(level=1.0)
        yield Heater(temperature=0)
        yield Nozzle()

    @Rule(CoffeeMachine(),
          AS.w << Water(level=MATCH.water_l),
          Coffee(water_use=MATCH.water_u),
          TEST(lambda water_l, water_u: water_u > water_l))
    def add_water(self, w):
        print("Add water to the coffee machine.")
        self.retract(w)
        self.declare(Water(level=1.0))

    @Rule(CoffeeMachine(),
          AS.m << Milk(level=MATCH.milk_l),
          Coffee(milk_use=MATCH.milk_u),
          TEST(lambda milk_l, milk_u: milk_u > milk_l))
    def add_milk(self, m):
        print("Add milk to the coffee machine.")
        self.retract(m)
        self.declare(Milk(level=1.0))

    @Rule(CoffeeMachine(),
          Brew(status="ready"), Grinder(filled=False))
    def fill_grinder(self):
        print("Fill grinder with coffee beans.")

    @Rule(CoffeeMachine(),
              Heater(temperature=P(lambda x: x >= Heater.upper_threshold)))
    def heater_too_hot(self):
        print("Heater is too hot.")

    @Rule(CoffeeMachine(), AS.b << Brew(status="ready"),
          Grinder(filled=True),
          AS.m << Milk(level=MATCH.milk_l),
          AS.w << Water(level=MATCH.water_l),
          AS.c << Coffee(name=MATCH.n, water_use=MATCH.water_u,
                         milk_use=MATCH.milk_u),
          TEST(lambda water_l, water_u: water_u <= water_l),
          TEST(lambda milk_l, milk_u: milk_u <= milk_l),
          AS.f1 << UserInput(action=Actions.MAKE_COFFEE))
    def start_brewing(self, c, n, f1, m, w, b, milk_l, milk_u, water_l, water_u):
        print(f"Start brewing {n}.")
        # check whether all conditions are met to brew coffee
        self.retract(f1)
        self.retract(c)
        self.retract(m)
        self.retract(w)
        self.retract(b)
        self.declare(Water(level=water_l - water_u))
        self.declare(Milk(level=milk_l - milk_u))

    @Rule(AND(CoffeeMachine(), Nozzle(status="blocked")))
    def clear_nozzle(self):
        print("Clear nozzle for dispensing.")

    @Rule(CoffeeMachine(), NOT(UserInput()))
    def require_user_action(self):
        user_action = get_user_input()
        self.declare(UserInput(action=user_action))

    @Rule(CoffeeMachine(),
          AS.ui << UserInput(action=Actions.SHOW_FACTS))
    def show_facts(self, ui):
        print("Showing facts...")
        print(self.facts)
        self.retract(ui)

    @Rule(CoffeeMachine(),
          AS.f1 << UserInput(action=Actions.MAKE_COFFEE))
    def choose_coffee(self, f1):
        coffee = get_user_coffee()
        if coffee:
            self.declare(coffee)
        else:
            self.retract(f1)
        # self.declare(Coffee(needs_milk=True, name='Latte'))

    @Rule(CoffeeMachine(),
          AS.c << Coffee(name=MATCH.n))
    def make_coffee(self, c, n):
        print(f"Making {n}")
        self.declare(Brew(status="ready"))


if __name__ == "__main__":
    # Initializing the rules engine
    engine = CoffeeMachineRules()
    engine.reset()
    engine.run()
