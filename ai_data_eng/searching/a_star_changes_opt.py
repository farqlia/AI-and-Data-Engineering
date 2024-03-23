import re
from functools import partial
from queue import PriorityQueue
from typing import Callable

from ai_data_eng.searching.a_star_time_opt import Heuristic
from ai_data_eng.searching.globals import A_STAR_RUNS_P
from ai_data_eng.searching.graph import *
from ai_data_eng.searching.searchning import a_star_print_info, PrioritizedItem, OptimizationType, run_solution, \
    idxs_to_nodes, assert_connection_path, print_path, write_solution_to_file
from ai_data_eng.searching.utils import *


def find_path(graph: Graph, heuristic: Heuristic, cost_func: Callable,
              neighbours_gen: Callable, start_stop: str, goal_stop: str, leave_hour: str):
    frontier = PriorityQueue()
    dep_time = time_to_normalized_sec(leave_hour)

    cost_so_far = {}
    # if commuting A -> B, then this will be came_from_conn[B] = A so we can recreate the path
    came_from_conn = {}
    stop_conn = {}
    goal_stop_coords = graph.compute_stop_coords(goal_stop)
    goal_stop = (goal_stop, goal_stop_coords['stop_lat'], goal_stop_coords['stop_lon'])
    start_stop_coords = graph.compute_stop_coords(start_stop)
    print(f'{start_stop} -> {goal_stop}')

    cost_so_far[('', start_stop)] = 0
    stop_conn[('', start_stop)] = -1
    came_from_conn[('', start_stop)] = None
    item = PrioritizedItem(cost_so_far[('', start_stop)], ('', start_stop))
    frontier.put(item)

    start_stop = (start_stop, start_stop_coords['stop_lat'], start_stop_coords['stop_lon'])

    graph.add_conn(dep_time, start_stop, -1)

    while not frontier.empty():
        # get the stop with the lowest cost
        item = frontier.get()
        (line, current) = item.item

        conn = graph.conn_at_index(stop_conn[(line, current)])
        # consider all possible end stops
        if current == goal_stop[0]:
            goal = (line, current)
            # theory - first found is the best
            break

        current_stop = graph.stop_as_tuple(graph.rename_stop(conn))
        for next_conn in neighbours_gen(conn['arrival_sec'], current_stop, conn['line']).itertuples():
            # cost of commuting start --> current and current --> next
            next_stop_coords = graph.compute_stop_coords(next_conn.end_stop)
            next_stop = (next_conn.end_stop, next_stop_coords.stop_lat, next_stop_coords.stop_lon)
            new_cost = cost_so_far[(line, current)] + cost_func(prev_conn=conn, next_conn=next_conn)
            heuristic_cost = heuristic.compute(start_stop, current_stop, next_stop, goal_stop,
                                               conn, next_conn, new_cost)
            approx_goal_cost = new_cost + heuristic_cost
            if (next_conn.line, next_conn.end_stop) not in cost_so_far or new_cost < cost_so_far[(next_conn.line, next_conn.end_stop)]:
                cost_so_far[(next_conn.line, next_conn.end_stop)] = new_cost
                item = PrioritizedItem(approx_goal_cost, (next_conn.line, next_conn.end_stop))
                frontier.put(item)
                came_from_conn[(next_conn.line, next_conn.end_stop)] = (line, current)
                stop_conn[(next_conn.line, next_conn.end_stop)] = next_conn.Index


    return goal, (came_from_conn, stop_conn), cost_so_far


def path_to_list(goal, came_from_conn, stop_conn):
    line, current = goal
    index = stop_conn[(line, current)]
    conns = []
    while index > 0:
        conns.append(index)
        (line, current) = came_from_conn[(line, current)]
        index = stop_conn[(line, current)]
    conns.reverse()
    return conns


def a_star_changes_opt(start_stop: str, goal_stop: str, leave_hour: str,
                       heuristic: Heuristic):
    with open(A_STAR_RUNS_P / 'run', mode='a', encoding='utf-8') as f:
        print(f'Testcase: {start_stop} -> {goal_stop}\nStart time: {leave_hour}\nRoute', file=f)
        graph, goal, came_from, costs, elapsed_time = run_solution(
            partial(find_path, heuristic=heuristic),
            start_stop, goal_stop, leave_hour, OptimizationType.CHANGES)
        came_from_conn, stop_conn = came_from
        conns = path_to_list(goal, came_from_conn, stop_conn)
        connections = [graph.conn_at_index(idx) for idx in conns]
        assert assert_connection_path(time_to_normalized_sec(leave_hour), connections)
        print_path(connections, f)
        # write_solution_to_file(A_STAR_RUNS_P / f'{start_stop}-{goal_stop}')
        print(f'Total number of changes is {costs[goal]}', file=f)
        print(f'Algorithm took {elapsed_time:.2f}s to execute\n', file=f)
        write_solution_to_file(A_STAR_RUNS_P / 'summary', connections, elapsed_time, costs[goal])