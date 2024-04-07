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
from ai_data_eng.searching.searchning import OptimizationType, idxs_to_nodes, print_path, assert_connection_path, \
    print_path_mark_stops, connections_idx
from ai_data_eng.searching.utils import sec_to_time, diff, time_to_normalized_sec
from typing import Set

from ai_data_eng.tabu_search.evaluate import get_matched_stops, get_matched_connections, judge_t_solution
from ai_data_eng.tabu_search.neighbourhood_search import insert_conn_between
from ai_data_eng.utils.utilities import stop_name
from ai_data_eng.tabu_search.globals import TABU_SEARCH_DIR

from ai_data_eng.tabu_search.searching import naive_solution


def tabu_search(g: Graph, criterion: OptimizationType, start_stop: str, visiting_stops: List[str], leave_hour: str,
                outer_loops=5):
    # This initial solution could be the best solution from the possible stops permutations?
    solution = naive_solution(g)(criterion, start_stop, visiting_stops, leave_hour)
    assert_connection_path(time_to_normalized_sec(leave_hour), start_stop, start_stop, solution)
    found_solutions = set()
    insert_conn = insert_conn_between(g, criterion)
    with open(TABU_SEARCH_DIR / stop_name(start_stop), mode='w', encoding='utf-8') as f:
        f = None
        print_path_mark_stops(solution, visiting_stops, f)
        print(get_matched_stops(solution, visiting_stops), file=f)

        for _ in range(outer_loops):
            curr_min_cost = judge_t_solution(solution, visiting_stops)
            curr_min = solution
            indexes_of_matched = get_matched_connections(solution, visiting_stops)
            print(f"cost = {round(curr_min_cost, 2)}", file=f)
            o = 4
            # for o in range(len(indexes_of_matched) - 1):
            i, j = indexes_of_matched[o], indexes_of_matched[o + 1]
            print(f"--------- [{o}] i={i}, j={j} -----------", file=f)
            for k in range(i):
                print(f"k = {k}", file=f)
                for m in range(k):
                    print(f"m = {m}", file=f)
                    perturbated_solution = insert_conn(solution, m, k, i, j)
                    assert_connection_path(time_to_normalized_sec(leave_hour), start_stop, start_stop,
                                           perturbated_solution)
                    pert_cost = judge_t_solution(perturbated_solution, visiting_stops)
                    matched_all_stops = get_matched_stops(perturbated_solution, visiting_stops)[0] == len(
                        visiting_stops)
                    sol_idx = connections_idx(perturbated_solution)

                    not_yet_visited = sol_idx not in found_solutions
                    if not_yet_visited:
                        found_solutions.add(sol_idx)
                        if matched_all_stops and pert_cost < curr_min_cost:
                            print(f"IMPROVEMENT", file=f)
                            print_path_mark_stops(perturbated_solution, visiting_stops, f)
                            print(get_matched_stops(perturbated_solution, visiting_stops), file=f)
                            print(f"cost = {round(pert_cost, 2)}", file=f)
                            curr_min = perturbated_solution
                            curr_min_cost = pert_cost
                        elif matched_all_stops:
                            print(f"NOT IMPROVEMENT of {round(pert_cost, 2)}, but matched all", file=f)
                    else:
                        print(f"Already matched", file=f)
                prev_best_sol = solution
                solution = curr_min
            if solution == prev_best_sol:
                break

    return curr_min