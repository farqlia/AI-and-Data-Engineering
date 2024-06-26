import pandas as pd
from ai_data_eng.searching.a_star_changes_opt import a_star_changes_opt

from ai_data_eng.searching.globals import DATA_DIR
from ai_data_eng.searching.heuristics import MockHeuristic

test_cases = pd.read_json(DATA_DIR / 'test_cases/test_cases.json')
test_cases = test_cases.values.tolist()

# if os.path.exists(A_STAR_RUNS_P):
# shutil.rmtree(A_STAR_RUNS_P)
# os.makedirs(A_STAR_RUNS_P)

a_star_changes_opt(*test_cases[2], change_time=0, heuristic=MockHeuristic())
