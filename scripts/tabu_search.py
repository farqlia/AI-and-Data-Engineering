import json
import os.path
from functools import partial

import pandas as pd

from ai_data_eng.searching.globals import DATA_DIR
from ai_data_eng.searching.graph import add_const_change_time, Graph
from ai_data_eng.searching.searchning import OptimizationType
from ai_data_eng.tabu_search.globals import TABU_SEARCH_DIR
from ai_data_eng.tabu_search.tabu_search import tabu_search
from ai_data_eng.utils.utilities import stop_name

test_cases = pd.read_json(DATA_DIR / 'test_cases/tabu-search-cases.json')
test_cases = test_cases.values.tolist()

if __name__ == "__main__":

    if os.path.exists(TABU_SEARCH_DIR / 'summary'):
        os.remove(TABU_SEARCH_DIR / 'summary')

    connection_graph = pd.read_csv(DATA_DIR / 'connection_graph.csv',
                                   usecols=['line', 'departure_time', 'arrival_time', 'start_stop',
                                            'end_stop', 'start_stop_lat', 'start_stop_lon', 'end_stop_lat',
                                            'end_stop_lon'])

    g = Graph(connection_graph, partial(add_const_change_time, change_time=0))
    solutions = []

    for test_case in test_cases:
        print(f"TEST CASE {test_case[0]} with stops {test_case[1]}")
        new_sol, _ = tabu_search(g, OptimizationType.TIME, *test_case)
        solutions.append(new_sol)
        with open(TABU_SEARCH_DIR / (stop_name(test_case[0]) + '.json'), mode='w', encoding='utf-8') as f:
            json.dump({"solution": new_sol}, f, indent=4)

    with open(TABU_SEARCH_DIR / 'summary.json', mode='a', encoding='utf-8') as f:
        json.dump(solutions, f, indent=4)
