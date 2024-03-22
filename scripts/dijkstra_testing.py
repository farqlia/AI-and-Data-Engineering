import pandas as pd

from ai_data_eng.searching.dijkstra import dijkstra
from ai_data_eng.searching.globals import DATA_DIR

test_cases = pd.read_json(DATA_DIR / 'test_cases.json')
test_cases['dept_time'] = test_cases['dept_time'].apply(lambda x: x.strftime('%H:%M:%S'))

test_cases = test_cases.values

for test_case in test_cases:
    dijkstra(**test_case)

