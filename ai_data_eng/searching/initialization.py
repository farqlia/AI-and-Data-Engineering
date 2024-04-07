from queue import PriorityQueue
from typing import Callable

import pandas as pd

from ai_data_eng.searching.graph import Graph
from ai_data_eng.searching.searchning import PrioritizedItem
from ai_data_eng.searching.utils import diff


def initialize_queue(graph: Graph,cost_so_far, came_from_conn, stop_conn,
                     start_stop: str, dep_time: int):
    frontier = PriorityQueue()

    start_stop_coords = graph.compute_stop_coords(start_stop)

    # given only stop name consider all possible start stops??
    came_from_conn[-1] = None
    stop_conn[start_stop] = -1

    start_stop = (start_stop, start_stop_coords['stop_lat'], start_stop_coords['stop_lon'])

    graph.add_conn(dep_time, start_stop, -1)

    return frontier


def initialize_with_prev_conn(prev_conn_idx: int, graph: Graph, cost_so_far, came_from_conn, stop_conn,
                     start_stop: str, dep_time: int):

    frontier = PriorityQueue()
    prev_conn = graph.conn_at_index(prev_conn_idx)

    stop_conn[prev_conn.end_stop] = prev_conn_idx
    came_from_conn[prev_conn_idx] = None
    return frontier