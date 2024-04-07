import math
from typing import List

from ai_data_eng.searching.graph import Graph
from ai_data_eng.searching.searchning import OptimizationType, assert_connection_path, \
    print_path_mark_stops, connections_idx
from ai_data_eng.searching.utils import sec_to_time, time_to_normalized_sec
from ai_data_eng.tabu_search.evaluate import get_matched_stops, get_matched_connections, judge_t_solution, \
    judge_p_solution, get_judge_func
from ai_data_eng.tabu_search.neighbourhood_search import insert_conn_between
from ai_data_eng.tabu_search.searching import naive_solution


def contains_all_stops(solution, visiting_stops):
    return get_matched_stops(solution, visiting_stops)[0] == len(visiting_stops)


def tabu_neighbourhood_search(start_stop: str, visiting_stops: List[str], leave_hour: str, insert_conn, judge_solution,
                              found_solutions, list_size):

    solutions = []

    def add_to_visited(sol_idx, iteration):
        nonlocal solutions

        if len(solutions) > list_size:
            solutions = solutions[1:]
        solutions.append(sol_idx)
        found_solutions[sol_idx] = iteration

    def not_visited(sol_idx):
        return sol_idx not in solutions

    def iterate(solution: List[int], curr_min_cost, curr_iteration):
        indexes_of_matched = get_matched_connections(solution, visiting_stops)

        for o in range(len(indexes_of_matched) - 1):
            i, j = indexes_of_matched[o], indexes_of_matched[o + 1]
            print(f"--------- [{o}] i={i}, j={j} -----------")
            for k in range(i):

                for m in range(k):

                    permuted_solution = insert_conn(solution, m, k, i, j)
                    assert_connection_path(time_to_normalized_sec(leave_hour), start_stop, start_stop,
                                           permuted_solution)
                    pert_cost = judge_solution(permuted_solution)
                    matched_all_stops = contains_all_stops(permuted_solution, visiting_stops)
                    sol_idx = connections_idx(permuted_solution)

                    if not_visited(sol_idx):
                        add_to_visited(sol_idx, curr_iteration)
                        if matched_all_stops and pert_cost < curr_min_cost:
                            print_path_mark_stops(permuted_solution, visiting_stops)
                            print(get_matched_stops(permuted_solution, visiting_stops))
                            print(f"cost = {pert_cost}")
                            return permuted_solution, pert_cost, curr_iteration

                        elif matched_all_stops:
                            print(f"NOT IMPROVEMENT of {pert_cost}, but matched all")
                    else:
                        print(f"Already matched {sol_idx}")
                        break
                    curr_iteration += 1
        return solution, curr_min_cost, curr_iteration

    return iterate


def tabu_list_size(start_stop: str, visiting_stops: List[str]):
    return 100


def tabu_search(g: Graph, criterion: OptimizationType, start_stop: str, visiting_stops: List[str], leave_hour: str,
                    outer_loops=5, list_size=math.inf):
    # This initial solution could be the best solution from the possible stops permutations?
    solution = naive_solution(g)(criterion, start_stop, visiting_stops, leave_hour)
    assert_connection_path(time_to_normalized_sec(leave_hour), start_stop, start_stop, solution)
    found_solutions = {}
    judge_solution = get_judge_func(criterion)
    insert_conn = insert_conn_between(g, criterion)
    curr_iteration = 0
    search = tabu_neighbourhood_search(start_stop, visiting_stops, leave_hour, insert_conn, judge_solution,
                                       found_solutions, list_size)
    print(f"GENERATED SOLUTION")
    print_sol_info(solution, visiting_stops)
    best_sol = solution
    best_sol_cost = judge_solution(solution)
    prev_sol = solution
    for _ in range(outer_loops):
        prev_cost = judge_solution(prev_sol)
        iteration_sol, iteration_cost, curr_iteration = search(prev_sol,
                                                               prev_cost, curr_iteration)
        print_path_mark_stops(iteration_sol, visiting_stops)
        if iteration_cost < best_sol_cost:
            print(f"IMPROVEMENT {curr_iteration}")
            print_sol_info(solution, visiting_stops)
            best_sol = iteration_sol
            best_sol_cost = iteration_cost

        if prev_sol == iteration_sol:
            break
        prev_sol = iteration_sol

    return structure_solution(best_sol), found_solutions


def print_sol_info(solution, visiting_stops):
    print(f"time cost = {sec_to_time(judge_t_solution(solution))}")
    print(f"changes cost = {judge_p_solution(solution)}")
    print(get_matched_stops(solution, visiting_stops))


def structure_solution(solution):
    return {
        "conn_idx": connections_idx(solution),
        "commute_time": int(judge_t_solution(solution)),
        "n_of_changes": int(judge_p_solution(solution))
    }


