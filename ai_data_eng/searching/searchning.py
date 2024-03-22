from enum import Enum

import pandas as pd

from ai_data_eng.searching.graph import Graph, add_constant_change_time
from ai_data_eng.searching.utils import sec_to_time, diff
from ai_data_eng.searching.globals import DATA_DIR

pd.options.mode.chained_assignment = None
from timeit import default_timer as timer


def a_star_p_print_info(prev, next, line, changes, heuristic, file=None):
    print(
        f"[{changes}/{heuristic}] {line} goes from {prev} to {next}", file=file)


def a_star_print_info(conn, cost, heuristic, file=None):
    print(
        f"[{sec_to_time(cost)}/{sec_to_time(heuristic)}] {conn.line} goes from {conn.start_stop} to {conn.end_stop} and leaves at {conn.departure_time}, arrives at {conn.arrival_time}",
        file=file)


def print_info(conn, cost, file=None):
    print(
        f"[{sec_to_time(cost)}] {conn['line']} goes from {conn['start_stop']} to {conn['end_stop']} and leaves at {conn['departure_time']}, arrives at {conn['arrival_time']}",
        file=file)


def path_to_list(node: str, connections: dict):
    path = [node]
    while node:
        node = connections[node]
        path.append(node)
    path.reverse()
    return path[1:]


def idxs_to_nodes(graph: Graph, goal_idx: int, conn_idxs: dict):
    idx_path = path_to_list(goal_idx, conn_idxs)
    return [graph.conn_at_index(idx) for idx in idx_path[1:]]


def print_path(connections: dict, print_to=None):
    for conn in connections:
        print(
            f'{conn["start_stop"]} [{sec_to_time(conn["departure_sec"])}] --- {conn["line"]} ---> {conn["end_stop"]} [{sec_to_time(conn["arrival_sec"])}]',
            file=print_to)


def assert_connection_path(dept_time, connections):
    if connections[0]['departure_sec'] < dept_time:
        return False
    for i in range(len(connections) - 1):
        if diff(connections[i + 1]['departure_sec'], connections[i + 1]['arrival_sec']) < 0:
            return False
    return True


class OptimizationType(Enum):
    TIME = 1,
    CHANGES = 2


def get_cost_func(graph: Graph, criterion: OptimizationType):
    return graph.time_cost_between_conns if criterion == OptimizationType.TIME else graph.change_cost_between_conns


def run_solution(find_path_function, start_stop: str, goal_stop: str, leave_hour: str,
                 criterion: OptimizationType = OptimizationType.TIME):
    start = timer()
    connection_graph = pd.read_csv(DATA_DIR / 'connection_graph.csv',
                                   usecols=['line', 'departure_time', 'arrival_time', 'start_stop',
                                            'end_stop', 'start_stop_lat', 'start_stop_lon', 'end_stop_lat',
                                            'end_stop_lon'])
    graph = Graph(connection_graph, add_constant_change_time)

    goal_index, came_from, costs = find_path_function(graph=graph, start_stop=start_stop,
                                                      goal_stop=goal_stop, leave_hour=leave_hour,
                                                      cost_func=get_cost_func(graph, criterion))
    end = timer()
    elapsed_time = (end - start)
    solution_cost = costs[graph.stop_as_tuple(graph.rename_stop(graph.conn_at_index(goal_index)))]
    return graph, goal_index, came_from, solution_cost, elapsed_time
