from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from ai_data_eng.searching.a_star_p import find_path
from ai_data_eng.searching.globals import DATA_DIR
from ai_data_eng.searching.graph import Graph, add_constant_change_time
from ai_data_eng.searching.heuristics import ChangeHeuristic
from ai_data_eng.searching.searchning import *

connection_graph = pd.read_csv(DATA_DIR / 'connection_graph.csv',
                               usecols=['line', 'departure_time', 'arrival_time', 'start_stop',
       'end_stop', 'start_stop_lat', 'start_stop_lon', 'end_stop_lat',
       'end_stop_lon'])


g = Graph(connection_graph, add_constant_change_time)

test_cases = pd.read_json(DATA_DIR / 'test_cases/test_cases.json')
test_cases = test_cases.values.tolist()

goal, came_from_conn, stop_conn, cost_so_far = find_path(g, ChangeHeuristic(), *test_cases[2])
print(goal)
print(came_from_conn)
print(cost_so_far)

line, current = goal
index = stop_conn[(line, current)]
conns = []
while index > 0:
    conns.append(index)
    (line, current) = came_from_conn[(line, current)]
    index = stop_conn[(line, current)]
conns.reverse()
print(conns)
print_path([g.conn_at_index(idx) for idx in conns])
print(round(cost_so_far[goal], 2))