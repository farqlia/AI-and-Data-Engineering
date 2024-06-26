from enum import Enum
from enum import Enum
from functools import partial

import numpy as np
import pandas as pd

from ai_data_eng.searching.globals import DATA_DIR
from ai_data_eng.searching.graph import Graph, is_conn_change, \
    add_const_change_time
from ai_data_eng.searching.utils import sec_to_time, diff, time_to_normalized_sec

pd.options.mode.chained_assignment = None
from timeit import default_timer as timer

from dataclasses import dataclass, field
from typing import Any, Callable

TIME_AND_CHANGE_HEURISTIC = {
    'a': 0.01, 'b': 0.5
}


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


def a_star_print_info(formatter: Callable):
    def func(conn, cost, heuristic, file=None):
        print(
            f"[{formatter(cost)}/{formatter(heuristic)}] {conn.line} goes from {conn.start_stop} to {conn.end_stop} and leaves at {conn.departure_time}, arrives at {conn.arrival_time} [{conn.Index}]",
            file=file)

    return func


def print_info(conn, cost, file=None):
    print(
        f"[{sec_to_time(cost)}] {conn.line} goes from {conn.start_stop}"
        f" to {conn.end_stop} and leaves at {conn.departure_time}, arrives at {conn.arrival_time}",
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


def connections_idx(connections):
    return tuple(int(conn.name) for conn in connections)


def print_path(connections, print_to=None):
    for i, conn in enumerate(connections):
        print(
            f'({i}) {conn["start_stop"]} [{sec_to_time(conn["departure_sec"])}] --- {conn["line"]} ---> {conn["end_stop"]} [{sec_to_time(conn["arrival_sec"])}] [{conn.name}]',
            file=print_to)


def print_path_mark_stops(connections, mark_stops, print_to=None):
    mark_stops = set(mark_stops)
    for i, conn in enumerate(connections):
        is_in_to_marked = conn["start_stop"] in mark_stops
        print(
            f'({i}) {"**" if is_in_to_marked else ""} {conn["start_stop"]} [{sec_to_time(conn["departure_sec"])}] --- {conn["line"]} ---> {conn["end_stop"]} [{sec_to_time(conn["arrival_sec"])}] [{conn.name}]',
            file=print_to)
        if is_in_to_marked:
            mark_stops.remove(conn["start_stop"])


def get_number_of_line_changes(connections):
    line_changes = int(np.sum([1 for (c1, c2) in zip(connections[:-1], connections[1:]) if is_conn_change(c1, c2)]))
    return line_changes


def write_solution_to_file(filename, connections, leave_hour, elapsed_time, solution_cost, change_time):
    with open(str(filename) + f'{change_time}', mode='a', encoding='utf-8') as file:
        conn_time = diff(connections[-1]['arrival_sec'], time_to_normalized_sec(leave_hour))
        line_changes = get_number_of_line_changes(connections)
        file.write(
            f'{connections[0]["start_stop"]},{connections[-1]["end_stop"]},{sec_to_time(conn_time)},{line_changes},{round(elapsed_time, 2)},{solution_cost},{change_time}\n')


def assert_connection_path(dept_time, start_stop, goal_stop, connections):
    assert connections[0]['departure_sec'] >= dept_time, f"{connections[0]['departure_sec']} is before {dept_time}!"
    assert connections[0][
               'start_stop'] == start_stop, f"start stop {connections[0]['start_stop']} is not the desired {start_stop}"

    for i in range(len(connections) - 1):
        time_diff = diff(connections[i + 1]['departure_sec'], connections[i]['arrival_sec'])
        assert time_diff >= 0, f"[{i}] connection has invalid time! {time_diff}"
        assert (connections[i + 1]['start_stop'] == connections[i][
            'end_stop']), f"{[i]} has different start and end stops! ends at {connections[i]['end_stop']}, starts at {connections[i + 1]['start_stop']}"
    assert connections[-1][
               'end_stop'] == goal_stop, f"goal stop {connections[-1]['end_stop']} is not the desired {goal_stop}"


class OptimizationType(Enum):
    TIME = 1,
    CHANGES = 2,
    TIME_AND_CHANGES = 3


def get_cost_func(graph: Graph, criterion: OptimizationType):
    if criterion == OptimizationType.TIME:
        return graph.time_cost_between_conns
    elif criterion == OptimizationType.CHANGES:
        return graph.change_cost_between_conns
    else:
        return graph.averaged_cost


def get_neighbours_gen(graph: Graph, criterion: OptimizationType):
    return graph.get_earliest_from if criterion == OptimizationType.TIME else graph.get_earliest_lines_from


def run_solution(find_path_function, start_stop: str, goal_stop: str, leave_hour: str, change_time,
                 criterion: OptimizationType = OptimizationType.TIME):
    start = timer()
    connection_graph = pd.read_csv(DATA_DIR / 'connection_graph.csv',
                                   usecols=['line', 'departure_time', 'arrival_time', 'start_stop',
                                            'end_stop', 'start_stop_lat', 'start_stop_lon', 'end_stop_lat',
                                            'end_stop_lon'])
    graph = Graph(connection_graph, partial(add_const_change_time, change_time=change_time))

    goal, came_from, costs = find_path_function(graph=graph, start_stop=start_stop,
                                                goal_stop=goal_stop, leave_hour=leave_hour,
                                                cost_func=get_cost_func(graph, criterion),
                                                neighbours_gen=get_neighbours_gen(graph, criterion))
    end = timer()
    elapsed_time = (end - start)
    # solution_cost = costs[graph.stop_as_tuple(graph.rename_stop(graph.conn_at_index(goal_index)))]
    return graph, goal, came_from, costs, elapsed_time
