import random
from enum import Enum
from typing import Optional

import schema as s
from experta import *
from experta.fact import *

from ai_data_eng.reasoning_system.coffees import *


class Actions(Enum):
    MAKE_COFFEE = "make coffee"
    FILL_WATER = "fill water"
    FILL_MILK = "fill milk"
    FILL_BEANS = "fill beans"
    SHOW_FACTS = "show facts"
    TROUBLESHOOT = "troubleshoot"
    CLEAR_NOZZLE = "clear nozzle"
    DESCALE = "descale"
    STOP = "stop"


class Problems(Enum):
    MILK_FORTHER = " Insufficient foam is produced when the milk is frothed or milk sprays out of the professional fine foam frother"


ACTIONS = [Actions.MAKE_COFFEE, Actions.FILL_WATER,
           Actions.SHOW_FACTS, Actions.DESCALE, Actions.CLEAR_NOZZLE,
           Actions.TROUBLESHOOT, Actions.STOP]


class CoffeeMachine(Fact):
    """A fact representing the coffee machine."""
    pass


def from_type(coffee_type: CoffeeType):
    return Coffee(name=coffee_type.name,
                  water_use=coffee_type.water_use,
                  milk_use=coffee_type.milk_use,
                  beans_use=coffee_type.beans_use)


class Coffee(Fact):
    milk_use = Field(s.And(s.Use(float), lambda l: 0.0 <= l <= 1.0), default=0.0)
    water_use = Field(s.And(s.Use(float), lambda l: 0.0 <= l <= 1.0), default=0.2)
    beans_use = Field(s.And(s.Use(float), lambda l: 0.0 <= l <= 1.0), default=0.2)
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
    scale = Field(s.Use(float), default=0.0)


class Milk(Component):
    """A fact representing the milk component."""
    level = Field(s.And(s.Use(float), lambda l: 0.0 <= l <= 1.0), default=1.0)


class Grinder(Component):
    """A fact representing the grinder component."""
    level = Field(s.And(s.Use(float), lambda l: 0.0 <= l <= 1.0), default=1.0)
    state = Field(s.Or("grinding", "inactive", "blocked"), default="inactive")
    degree = Field(s.And(s.Use(int), lambda x: 1 <= x <= 5), default=3)


class Heater(Component):
    """A fact representing the heater component."""
    temperature = Field(s.And(s.Use(int), lambda x: 0 <= x < 100), default=0)
    upper_threshold = 80


class Brew(Fact):
    """A fact representing the brewing process."""
    status = Field(s.And(s.Use(str), s.Or("ready", "in progress", "done")))


class MilkNozzle(Component):
    """A fact representing the nozzle for heating milk."""
    status = Field(s.Or("blocked", "nozzling", "inactive"), default="inactive")


def get_user_coffee() -> Optional[Coffee]:
    print("Choose coffee")
    for i, coffee in enumerate(coffees):
        print(f"[{i}] {coffee.name}")
    cof = int(input("Choice: "))
    return from_type(coffees[cof]) if 0 <= cof < len(coffees) else None


def get_user_input(actions=ACTIONS) -> Actions:
    print("Choose from a set of possible actions")
    for i, action in enumerate(actions):
        print(f"[{i}] {action.value}")
    act = int(input("Choice: "))
    return actions[act] if 0 <= act < len(actions) else Actions.STOP

def get_user_problem() -> Optional[Problems]:
    print("Choose from a set of possible actions")
    problems = list(Problems.__members__.values())
    for i, problem in enumerate(problems):
        print(f"[{i}] {problem.value}")
    prob = int(input("Choice: "))
    return problems[prob] if 0 <= prob < len(problems) else None

class UserInput(Fact):
    """A fact representing user input for the coffee machine."""
    # user can choose coffee, hot water or ex. system conservation
    action = Field(s.Or(*ACTIONS))


class TroubleShooting(Fact):
    problem = Field(s.Or(*list(Problems.__members__.values())))
    solved = Field(bool, default=False)


class CoffeeMachineRules(KnowledgeEngine):
    """The rule-based system for the coffee machine."""

    @DefFacts()
    def startup(self):
        print("Coffee machine started.")
        yield CoffeeMachine()
        yield Grinder(level=1.0)
        yield Milk(level=1.0)
        yield Water(level=1.0)
        # Also manipulate with temperature
        yield Heater(temperature=0)
        # And with this too
        yield MilkNozzle(status="inactive")

    @Rule(CoffeeMachine(), NOT(UserInput()))
    def require_user_action(self):
        user_action = get_user_input()
        self.declare(UserInput(action=user_action))

    @Rule(CoffeeMachine(),
          AS.f1 << UserInput(action=Actions.MAKE_COFFEE))
    def choose_coffee(self, f1):
        coffee = get_user_coffee()
        if coffee:
            self.declare(coffee)
        else:
            self.retract(f1)

    @Rule(CoffeeMachine(),
          AS.c << Coffee(name=MATCH.n))
    def make_coffee(self, c, n):
        print(f"Making {n}")
        self.declare(Brew(status="ready"))

    @Rule(CoffeeMachine(), AS.b << Brew(status="ready"),
          AS.mn << MilkNozzle(),
          AS.g << Grinder(level=MATCH.beans_l),
          AS.m << Milk(level=MATCH.milk_l),
          AS.w << Water(level=MATCH.water_l, scale=MATCH.scale),
          AS.c << Coffee(name=MATCH.n, water_use=MATCH.water_u,
                         milk_use=MATCH.milk_u, beans_use=MATCH.beans_u),
          TEST(lambda milk_l, milk_u: milk_u <= milk_l),
          TEST(lambda beans_l, beans_u: beans_u <= beans_l),
          UserInput(action=P(lambda x: x == Actions.MAKE_COFFEE)))
    def start_brewing(self, mn, n, m, w, b, g, milk_l, milk_u, water_l, water_u,
                      beans_l, beans_u, scale):
        print(f"Start brewing {n}.")
        # check whether all conditions are met to brew coffee
        self.retract(m)
        self.retract(w)
        self.retract(b)
        self.retract(g)
        self.retract(mn)
        self.declare(Brew(status="done"))
        self.declare(Water(level=water_l - water_u, scale=scale + SCALE_AMOUNT))
        block = bool(random.random() > 0.1)
        self.declare(MilkNozzle(status="blocked" if block else "nozzling"))
        self.declare(Milk(level=milk_l - milk_u))
        self.declare(Grinder(level=beans_l - beans_u))

    @Rule(CoffeeMachine(), AS.b << Brew(status="done"),
          AS.c << Coffee(name=MATCH.n),
          AS.mn << MilkNozzle(),
          AS.f1 << UserInput(action=Actions.MAKE_COFFEE))
    def end_brewing(self, c, n, b, mn, f1):
        print(f"End brewing {n}.")
        self.retract(c)
        self.retract(mn)
        self.retract(b)
        self.retract(f1)
        self.declare(MilkNozzle(status="inactive"))

    @Rule(CoffeeMachine(),
          AS.w << Water(level=MATCH.water_l),
          AS.ui << UserInput(action=MATCH.act),
          Coffee(water_use=MATCH.water_u),
          TEST(lambda act: act != Actions.FILL_WATER),
          TEST(lambda water_l, water_u: water_u > water_l),
          salience=1)
    def require_fill_water(self):
        print("Before proceeding you need to fill water.")
        user_action = get_user_input([Actions.FILL_WATER, Actions.STOP])
        if user_action == Actions.FILL_WATER:
            self.declare(UserInput(action=Actions.FILL_WATER))

    @Rule(CoffeeMachine(),
          AS.w << Water(scale=MATCH.scale),
          AS.ui << UserInput(action=P(lambda x: x == Actions.FILL_WATER)))
    def fill_water(self, w, ui, scale):
        print("Add water to the coffee machine.")
        self.retract(w)
        self.retract(ui)
        self.declare(Water(level=1.0, scale=scale))
        print(self.facts)

    @Rule(CoffeeMachine(),
          AS.m << Milk(level=MATCH.milk_l),
          Coffee(milk_use=MATCH.milk_u),
          TEST(lambda milk_l, milk_u: milk_u > milk_l))
    def fill_milk(self, m):
        print("Add milk to the coffee machine.")
        user_action = get_user_input([Actions.FILL_MILK, Actions.STOP])
        if user_action == Actions.FILL_MILK:
            self.retract(m)
            self.declare(Milk(level=1.0))

    @Rule(CoffeeMachine(),
          Coffee(beans_use=MATCH.beans_u),
          AS.g << Grinder(level=MATCH.beans_l),
          TEST(lambda beans_l, beans_u: beans_l < beans_u))
    def fill_grinder(self, g):
        print("Fill grinder with coffee beans.")
        user_action = get_user_input([Actions.FILL_BEANS, Actions.STOP])
        if user_action == Actions.FILL_BEANS:
            self.retract(g)
            self.declare(Grinder(level=1.0))

    @Rule(CoffeeMachine(),
          Heater(temperature=P(lambda x: x >= Heater.upper_threshold)))
    def heater_too_hot(self):
        print("Heater is too hot.")



    @Rule(CoffeeMachine(),
          AS.mn << MilkNozzle(),
          OR(
              AND(MilkNozzle(status="blocked"),
                  Brew(status=MATCH.pro)),
              AND(AS.t << TroubleShooting(problem=Problems.MILK_FORTHER, solved=False))
          ), salience=1)
    def require_clear_nozzle(self):
        print("Before proceeding you need to clear nozzle.")
        user_action = get_user_input([Actions.CLEAR_NOZZLE, Actions.STOP])
        if user_action == Actions.CLEAR_NOZZLE:
            self.declare(UserInput(action=Actions.CLEAR_NOZZLE))

    @Rule(CoffeeMachine(),
          AS.mn << MilkNozzle(),
          AS.ui << UserInput(action=Actions.CLEAR_NOZZLE),
          AS.t << TroubleShooting(), salience=1)
    def clear_nozzle(self, mn, ui, t=None, pro="inactive"):
        self.retract(ui)
        if t:
            self.retract(t)
            self.declare(TroubleShooting(problem=Problems.MILK_FORTHER, solved=True))
        self.retract(mn)
        self.declare(MilkNozzle(status="nozzling" if pro == "in progress" else "inactive"))
        print("Nozzle is cleared.")

    @Rule(CoffeeMachine(),
          AS.ui << UserInput(action=Actions.SHOW_FACTS))
    def show_facts(self, ui):
        print("Showing facts...")
        print(self.facts)
        self.retract(ui)

    @Rule(CoffeeMachine(),
          Water(scale=MATCH.scale),
          # Do not disrupt preparing coffee
          NOT(UserInput()),
          TEST(lambda scale: scale >= 1.0))
    def require_descaling(self):
        print("Before proceeding you need to descale machine.")
        user_action = get_user_input([Actions.DESCALE, Actions.STOP])
        if user_action == Actions.DESCALE:
            self.declare(UserInput(action=Actions.DESCALE))

    @Rule(CoffeeMachine(),
          AS.ui << UserInput(action=Actions.DESCALE),
          AS.w << Water())
    def descale(self, w, ui):
        print(f"Descaling ...")
        self.retract(w)
        self.retract(ui)
        self.declare(Water(level=1.0, scale=0.0))

    @Rule(CoffeeMachine(),
          AS.ui << UserInput(action=Actions.TROUBLESHOOT))
    def troubleshoot(self, ui):
        user_problem = get_user_problem()
        if user_problem:
            self.declare(TroubleShooting(problem=user_problem))
        else:
            self.retract(ui)

    @Rule(CoffeeMachine(),
        AS.ui << UserInput(action=Actions.TROUBLESHOOT),
          AS.t << TroubleShooting(solved=True))
    def solve_troubleshoot(self, ui, t):
        print(f"Your problem was solved")
        self.retract(ui)
        self.retract(t)


if __name__ == "__main__":
    # Initializing the rules engine
    engine = CoffeeMachineRules()
    engine.reset()
    engine.run()
