import pandas as pd

from ai_data_eng.searching.a_star_time_opt import a_star_time_opt
from ai_data_eng.searching.globals import DATA_DIR
from ai_data_eng.searching.heuristics import WeightedAverageTimeHeuristic
from functools import partial

from ai_data_eng.searching.initialization import initialize_with_prev_conn

test_cases = pd.read_json(DATA_DIR / 'test_cases/test_cases.json')
test_cases = test_cases.values.tolist()

a_star_time_opt(*test_cases[5], heuristic=WeightedAverageTimeHeuristic())

# a_star_time_opt(*test_cases[0], heuristic=WeightedAverageTimeHeuristic(), initialization_func=partial(initialize_with_prev_conn, prev_conn_idx=182859))