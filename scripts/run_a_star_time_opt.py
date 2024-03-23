import pandas as pd

from ai_data_eng.searching.globals import DATA_DIR
from ai_data_eng.searching.a_star_time_opt import a_star_time_opt
from ai_data_eng.searching.heuristics import WeightedAverageTimeHeuristic

test_cases = pd.read_json(DATA_DIR / 'test_cases/test_cases.json')
test_cases = test_cases.values.tolist()

for test_case in test_cases:
    a_star_time_opt(*test_case, heuristic=WeightedAverageTimeHeuristic())
