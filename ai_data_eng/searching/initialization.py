from queue import PriorityQueue
from typing import Callable

import pandas as pd

from ai_data_eng.searching.graph import Graph
from ai_data_eng.searching.searchning import PrioritizedItem
from ai_data_eng.searching.utils import diff


def initialize_queue(graph: Graph, cost_func: Callable, cost_so_far, came_from_conn, stop_conn,
                     start_stop: str, dep_time: int):
    frontier = PriorityQueue()


    # given only stop name consider all possible start stops??
    j = -1
    for candidate_start_stop in graph.get_possible_stops_t(start_stop):
        cost_so_far[candidate_start_stop] = 0
        graph.add_conn(dep_time, candidate_start_stop, j)
        came_from_conn[j] = None
        stop_conn[candidate_start_stop] = j
        frontier.put(PrioritizedItem(cost_so_far[candidate_start_stop], candidate_start_stop))
        j -= 1
    return frontier


def initialize_with_prev_conn(prev_conn_idx: int, graph: Graph, cost_func: Callable, cost_so_far, came_from_conn, stop_conn,
                     start_stop: str, dep_time: int):

    frontier = initialize_queue(graph, cost_func, cost_so_far, came_from_conn, stop_conn, start_stop, dep_time)
    prev_conn = graph.conn_at_index(prev_conn_idx)
    prev_stop = graph.stop_as_tuple(graph.rename_stop(prev_conn))
    for i in came_from_conn:
        graph.conn_graph.loc[i].line = 'MISSING'
    k = stop_conn[prev_stop]
    graph.conn_graph.drop(k, inplace=True)
    stop_conn[prev_stop] = prev_conn_idx
    came_from_conn[prev_conn_idx] = None
    return frontier