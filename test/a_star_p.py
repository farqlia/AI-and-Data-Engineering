from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from ai_data_eng.searching.a_star_p import find_path
from ai_data_eng.searching.globals import DATA_DIR
from ai_data_eng.searching.graph import Graph, add_constant_change_time

@pytest.fixture
def g():
    connection_graph = pd.read_csv(DATA_DIR / 'connection_graph.csv',
                               usecols=['line', 'departure_time', 'arrival_time', 'start_stop',
       'end_stop', 'start_stop_lat', 'start_stop_lon', 'end_stop_lat',
       'end_stop_lon'])
    return Graph(connection_graph, add_constant_change_time)


def test_a_star_p(g):
    start_stop = "PL. GRUNWALDZKI"
    goal_stop = "Młodych Techników"
    goal, came_from_conn, cost_so_far = find_path(g, start_stop, goal_stop, "20:32:00")
    print(goal)
    print(came_from_conn)
    print(cost_so_far)

    node = goal
    conns = []
    while node:
        conns.append(node)
        node = came_from_conn[node]
    conns.reverse()
    print(conns)