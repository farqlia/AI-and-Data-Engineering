import pandas as pd

from ai_data_eng.searching.globals import DATA_DIR
from ai_data_eng.searching.a_star import a_star, MaxVelocityTimeHeuristic, WeightedAverageTimeHeuristic, ChangeHeuristic
from ai_data_eng.searching.searchning import OptimizationType

test_cases = pd.read_json(DATA_DIR / 'test_cases/test_cases.json')
test_cases = test_cases.values.tolist()

# a_star(*test_cases[0], heuristic=WeightedAverageTimeHeuristic(), criterion=OptimizationType.TIME)
test_case = {
    "start_stop": "most Grunwaldzki", "goal_stop": "Rynek", "leave_hour": "08:00:00"
}


for test_case in test_cases:
    a_star(*test_case, heuristic=WeightedAverageTimeHeuristic(), criterion=OptimizationType.TIME)