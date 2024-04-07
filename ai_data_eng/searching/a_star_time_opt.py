from functools import partial
from queue import PriorityQueue
from queue import PriorityQueue
from typing import Callable

import pandas as pd

from ai_data_eng.searching.globals import A_STAR_RUNS_T
from ai_data_eng.searching.graph import Graph
from ai_data_eng.searching.heuristics import Heuristic
from ai_data_eng.searching.initialization import initialize_queue, initialize_with_prev_conn
from ai_data_eng.searching.searchning import run_solution, assert_connection_path, idxs_to_nodes, \
    print_path, OptimizationType, PrioritizedItem, write_solution_to_file, a_star_print_info
from ai_data_eng.searching.utils import time_to_normalized_sec, sec_to_time

pd.options.mode.chained_assignment = None


def find_path_a_star_t(graph: Graph, heuristic: Heuristic, cost_func: Callable,
                       neighbours_gen: Callable, start_stop: str, goal_stop: str, leave_hour: str, prev_conn_idx=None):

    dep_time = time_to_normalized_sec(leave_hour)

    # print_info = a_star_print_info(sec_to_time)
    cost_so_far = {start_stop: 0}
    # if commuting A -> B, then this will be came_from_conn[B] = A so we can recreate the path
    came_from_conn = {}
    stop_conn = {}

    if prev_conn_idx is not None:
        frontier = initialize_with_prev_conn(prev_conn_idx, graph=graph, cost_so_far=cost_so_far,
                                   came_from_conn=came_from_conn, stop_conn=stop_conn,
                                   start_stop=start_stop, dep_time=dep_time)
    else:
        frontier = initialize_queue(graph=graph, cost_so_far=cost_so_far,
                                             came_from_conn=came_from_conn, stop_conn=stop_conn,
                                             start_stop=start_stop, dep_time=dep_time)

    item = PrioritizedItem(cost_so_far[start_stop], start_stop)
    frontier.put(item)

    closest_set = {start_stop}
    goal_stop_index = None
    goal_stop_coords = graph.compute_stop_coords(goal_stop)
    goal_stop = (goal_stop, goal_stop_coords['stop_lat'], goal_stop_coords['stop_lon'])
    start_stop_coords = graph.compute_stop_coords(start_stop)
    start_stop = (start_stop, start_stop_coords['stop_lat'], start_stop_coords['stop_lon'])

    i = 0
    while not frontier.empty():
        # get the stop with the lowest cost
        item = frontier.get()
        _, current = item.priority, item.item

        conn = graph.conn_at_index(stop_conn[current])

        # consider all possible end stops
        if current == goal_stop[0]:
            goal_stop_index = conn.name
            # theory - first found is the best
            break

        cost = cost_so_far[current]
        for next_conn in neighbours_gen(conn).itertuples():
            # cost of commuting start --> current and current --> next
            new_cost = cost + cost_func(next_conn=next_conn, prev_conn=conn)
            heuristic_cost = heuristic.compute(start_stop, goal_stop, conn, next_conn, cost=cost)
            approx_goal_cost = new_cost + heuristic_cost
            if next_conn.end_stop not in cost_so_far or new_cost < cost_so_far[next_conn.end_stop]:
                cost_so_far[next_conn.end_stop] = new_cost
                frontier.put(PrioritizedItem(approx_goal_cost, next_conn.end_stop))
                came_from_conn[next_conn.Index] = conn.name
                stop_conn[next_conn.end_stop] = next_conn.Index
        closest_set.add(current)
        graph.exclude_stop(current)

    graph.reset()
    return goal_stop_index, came_from_conn, cost_so_far


def a_star_time_opt(start_stop: str, goal_stop: str, leave_hour: str, heuristic: Heuristic, change_time):
    with open(A_STAR_RUNS_T / f'run-change_time-{change_time}', mode='a', encoding='utf-8') as f:
        print(f'Testcase: {start_stop} -> {goal_stop}\nStart time: {leave_hour}\nRoute', file=f)
        graph, goal_index, came_from, costs, elapsed_time = run_solution(
            partial(find_path_a_star_t, heuristic=heuristic),
            start_stop, goal_stop, leave_hour, change_time, heuristic.criterion)
        connections = idxs_to_nodes(graph, goal_index, came_from)
        assert_connection_path(time_to_normalized_sec(leave_hour), start_stop, goal_stop, connections)
        print_path(connections, f)
        solution_cost = costs[graph.conn_at_index(goal_index).end_stop]
        print(f'Total trip time is {sec_to_time(solution_cost)}', file=f)
        print(f'Algorithm took {elapsed_time:.2f}s to execute\n', file=f)
        write_solution_to_file(A_STAR_RUNS_T / 'summary', connections, leave_hour, elapsed_time, solution_cost, change_time)
    return graph, connections


def a_star_time_opt_light(start_stop: str, goal_stop: str, leave_hour: str, heuristic: Heuristic, change_time,
                    initialization_func=initialize_queue):
    graph, goal_index, came_from, costs, elapsed_time = run_solution(
            partial(find_path_a_star_t, heuristic=heuristic, initialization_func=initialization_func),
            start_stop, goal_stop, leave_hour, change_time, heuristic.criterion)
    connections = idxs_to_nodes(graph, goal_index, came_from)
    return graph, connections