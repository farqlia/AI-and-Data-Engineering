from functools import partial
from typing import List

import numpy as np
import pandas as pd

from ai_data_eng.searching.a_star_changes_opt import find_path_a_star_p, path_to_list_p
from ai_data_eng.searching.a_star_time_opt import find_path_a_star_t
from ai_data_eng.searching.globals import DATA_DIR
from ai_data_eng.searching.graph import Graph, add_const_change_time, is_conn_change
from ai_data_eng.searching.heuristics import WeightedAverageTimeHeuristic, ChangeHeuristic
from ai_data_eng.searching.initialization import initialize_with_prev_conn
from ai_data_eng.searching.searchning import OptimizationType, idxs_to_nodes, print_path, get_number_of_line_changes
from ai_data_eng.searching.utils import sec_to_time, diff
from typing import Set


def get_matched_stops(solution, visiting_stops: List[str]):
    visiting_stops = set(visiting_stops)
    matched_stops = 0
    for conn in solution:
        if conn['start_stop'] in visiting_stops:
            visiting_stops.remove(conn['start_stop'])
            matched_stops += 1
    return matched_stops, visiting_stops

# Not so easy because a stop can occurs multiple times (so take the last occurence)
def get_matched_connections(connections, visiting_stops):
    visiting_stops = set(visiting_stops)
    indexes = set()
    for i, conn in enumerate(connections):
        if conn['end_stop'] in visiting_stops:
            indexes.add(i)
    indexes = list(indexes)
    indexes = sorted(indexes)
    return indexes


def judge_t_solution(solution):
    conn_time = diff(solution[-1]['arrival_sec'], solution[0]['departure_sec'])
    return conn_time


def judge_p_solution(solution):
    return get_number_of_line_changes(solution)