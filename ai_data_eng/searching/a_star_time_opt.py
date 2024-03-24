from functools import partial
from queue import PriorityQueue
from queue import PriorityQueue
from typing import Callable

import pandas as pd

from ai_data_eng.searching.globals import A_STAR_RUNS_T
from ai_data_eng.searching.graph import Graph
from ai_data_eng.searching.heuristics import Heuristic
from ai_data_eng.searching.initialization import initialize_queue
from ai_data_eng.searching.searchning import run_solution, assert_connection_path, idxs_to_nodes, \
    print_path, OptimizationType, PrioritizedItem, write_solution_to_file, a_star_print_info
from ai_data_eng.searching.utils import time_to_normalized_sec, sec_to_time

pd.options.mode.chained_assignment = None


def find_path(graph: Graph, heuristic: Heuristic, cost_func: Callable, initialization_func: Callable,
              neighbours_gen: Callable, start_stop: str, goal_stop: str, leave_hour: str,):

    dep_time = time_to_normalized_sec(leave_hour)

    # print_info = a_star_print_info(sec_to_time)
    cost_so_far = {}
    # if commuting A -> B, then this will be came_from_conn[B] = A so we can recreate the path
    came_from_conn = {}
    stop_conn = {}

    frontier = initialization_func(graph=graph, cost_func=cost_func, cost_so_far=cost_so_far,
                                   came_from_conn=came_from_conn, stop_conn=stop_conn,
                                   start_stop=start_stop, dep_time=dep_time)

    closest_set = {start_stop}

    goal_stop_coords = graph.compute_stop_coords(goal_stop)
    goal_stop = (goal_stop, goal_stop_coords['stop_lat'], goal_stop_coords['stop_lon'])
    start_stop_coords = graph.compute_stop_coords(start_stop)
    start_stop = (start_stop, start_stop_coords['stop_lat'], start_stop_coords['stop_lon'])

    i = 0
    while not frontier.empty():
        # get the stop with the lowest cost
        item = frontier.get()
        current = item.item

        conn = graph.conn_at_index(stop_conn[current])

        # consider all possible end stops
        if current[0] == goal_stop[0]:
            goal_stop_index = conn.name
            # theory - first found is the best
            break

        # print(f'[{i}]')
        cost = cost_so_far[current]
        for next_conn in neighbours_gen(conn['arrival_sec'], current, conn['line'], closest_set).itertuples():
            # cost of commuting start --> current and current --> next
            next_stop = (next_conn.end_stop, next_conn.end_stop_lat, next_conn.end_stop_lon)
            new_cost = cost + cost_func(next_conn=next_conn, prev_conn=conn)
            heuristic_cost = heuristic.compute(start_stop, current, next_stop, goal_stop, conn, next_conn)
            approx_goal_cost = new_cost + heuristic_cost
            if next_stop not in cost_so_far or new_cost < cost_so_far[next_stop]:
                # print_info(next_conn, new_cost, heuristic_cost)
                cost_so_far[next_stop] = new_cost
                frontier.put(PrioritizedItem(approx_goal_cost, next_stop))
                came_from_conn[next_conn.Index] = conn.name
                stop_conn[next_stop] = next_conn.Index
        closest_set.add(current[0])
        # i += 1

    return goal_stop_index, came_from_conn, cost_so_far


def a_star_time_opt(start_stop: str, goal_stop: str, leave_hour: str, heuristic: Heuristic, change_time,
                    initialization_func=initialize_queue):
    with open(A_STAR_RUNS_T / f'run-change_time-{change_time}', mode='a', encoding='utf-8') as f:
        print(f'Testcase: {start_stop} -> {goal_stop}\nStart time: {leave_hour}\nRoute', file=f)
        graph, goal_index, came_from, costs, elapsed_time = run_solution(
            partial(find_path, heuristic=heuristic, initialization_func=initialization_func),
            start_stop, goal_stop, leave_hour, change_time, heuristic.criterion)
        connections = idxs_to_nodes(graph, goal_index, came_from)
        assert assert_connection_path(time_to_normalized_sec(leave_hour), connections)
        print_path(connections, f)
        solution_cost = sec_to_time(costs[graph.stop_as_tuple(graph.rename_stop(graph.conn_at_index(goal_index)))])
        print(f'Total trip time is {solution_cost}', file=f)
        print(f'Algorithm took {elapsed_time:.2f}s to execute\n', file=f)
        write_solution_to_file(A_STAR_RUNS_T / 'summary', connections, leave_hour, elapsed_time, solution_cost, change_time)
    return graph, connections