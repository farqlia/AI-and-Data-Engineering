import os
import shutil

import pandas as pd

from ai_data_eng.searching.dijkstra import dijkstra
from ai_data_eng.searching.globals import DATA_DIR, DIJKSTRA

test_cases = pd.read_json(DATA_DIR / 'test_cases/test_cases.json')
test_cases = test_cases.values

if os.path.exists(DIJKSTRA):
    shutil.rmtree(DIJKSTRA)
    os.makedirs(DIJKSTRA)

for test_case in test_cases:
    dijkstra(*test_case)

