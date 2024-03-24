import os
import shutil

import pandas as pd

from ai_data_eng.searching.globals import DATA_DIR, A_STAR_RUNS_T
from ai_data_eng.searching.a_star_time_opt import a_star_time_opt
from ai_data_eng.searching.heuristics import WeightedAverageTimeHeuristic

test_cases = pd.read_json(DATA_DIR / 'test_cases/test_cases.json')
test_cases = test_cases.values.tolist()

if os.path.exists(A_STAR_RUNS_T):
    shutil.rmtree(A_STAR_RUNS_T)
    os.makedirs(A_STAR_RUNS_T)

for test_case in test_cases:
    a_star_time_opt(*test_case, change_time=0, heuristic=WeightedAverageTimeHeuristic())
