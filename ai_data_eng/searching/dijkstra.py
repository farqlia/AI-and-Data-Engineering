from queue import PriorityQueue
from typing import Callable

import pandas as pd

from ai_data_eng.searching.globals import DIJKSTRA
from ai_data_eng.searching.graph import Graph
from ai_data_eng.searching.initialization import initialize_queue
from ai_data_eng.searching.searchning import run_solution, assert_connection_path, idxs_to_nodes, \
    print_path, OptimizationType, PrioritizedItem, write_solution_to_file
from ai_data_eng.searching.utils import time_to_normalized_sec, sec_to_time

pd.options.mode.chained_assignment = None

def find_path(graph: Graph, cost_func: Callable, neighbours_gen: Callable, start_stop: str, goal_stop: str, leave_hour: str):

    dep_time = time_to_normalized_sec(leave_hour)

    cost_so_far = {}
    # if commuting A -> B, then this will be came_from_conn[B] = A so we can recreate the path
    came_from_conn = {}
    stop_conn = {}

    closest_set = {start_stop}

    frontier = initialize_queue(graph, cost_so_far, came_from_conn, stop_conn, start_stop, dep_time)

    while not frontier.empty():
        # get the stop with the lowest cost
        item = frontier.get()
        cost, current = item.priority, item.item

        conn = graph.conn_at_index(stop_conn[current])

        # consider all possible end stops
        if current == goal_stop:
            goal_stop_index = conn.name
            # theory - first found is the best
            break

        for next_conn in neighbours_gen(conn).itertuples():
            # cost of commuting start --> current and current --> next
            new_cost = cost + cost_func(next_conn=next_conn, prev_conn=conn)
            if next_conn.end_stop not in cost_so_far or new_cost < cost_so_far[next_conn.end_stop]:
                cost_so_far[next_conn.end_stop] = new_cost
                frontier.put(PrioritizedItem(new_cost, next_conn.end_stop))
                came_from_conn[next_conn.Index] = conn.name
                stop_conn[next_conn.end_stop] = next_conn.Index
        closest_set.add(current)
        graph.exclude_stop(current)

    return goal_stop_index, came_from_conn, cost_so_far


def dijkstra(start_stop: str, goal_stop: str, leave_hour: str, change_time: int):
    with open(DIJKSTRA / f'run-change_time-{change_time}', mode='a', encoding='utf-8') as f:
        print(f'Testcase: {start_stop} -> {goal_stop}\nStart time: {leave_hour}\nRoute', file=f)
        graph, goal_index, came_from, costs, elapsed_time = run_solution(find_path, start_stop, goal_stop,
                                                                    leave_hour, change_time, OptimizationType.TIME)

        connections = idxs_to_nodes(graph, goal_index, came_from)
        assert assert_connection_path(time_to_normalized_sec(leave_hour), connections)
        print_path(connections, f)
        solution_cost = costs[graph.conn_at_index(goal_index).end_stop]
        write_solution_to_file(DIJKSTRA / 'summary', connections, leave_hour, elapsed_time, solution_cost, change_time)
        print(f'Total trip time is {sec_to_time(solution_cost)}', file=f)
        print(f'Algorithm took {elapsed_time:.2f}s to execute\n', file=f)
    return graph, connections