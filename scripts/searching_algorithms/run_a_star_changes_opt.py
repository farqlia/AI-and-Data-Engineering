import os
import shutil

import pandas as pd
from ai_data_eng.searching.a_star_p.a_star_changes_opt import a_star_changes_opt

from ai_data_eng.searching.globals import DATA_DIR, A_STAR_RUNS_P
from ai_data_eng.searching.heuristics import ChangeHeuristic

test_cases = pd.read_json(DATA_DIR / 'test_cases/test_cases.json')
test_cases = test_cases.values.tolist()

#if os.path.exists(A_STAR_RUNS_P):
    #shutil.rmtree(A_STAR_RUNS_P)
    #os.makedirs(A_STAR_RUNS_P)

for test_case in test_cases:
    a_star_changes_opt(*test_case, change_time=60, heuristic=ChangeHeuristic())
