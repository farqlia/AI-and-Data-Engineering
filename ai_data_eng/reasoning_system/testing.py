from enum import Enum
from typing import Optional

import schema
import schema as s
from experta import *
from experta.fact import *


class AFact(Fact):
    name = Field(s.Use(str), default="name")


class BFact(AFact):

    def __init__(self):
        super().__init__(name="bfact")


class Rules(KnowledgeEngine):

    @DefFacts()
    def startup(self):
        yield BFact()

    @Rule(AS.a << AFact())
    def match(self, a):
        print(f"{a} is matched")


if __name__ == "__main__":
    engine = Rules()
    engine.reset()
    engine.run()