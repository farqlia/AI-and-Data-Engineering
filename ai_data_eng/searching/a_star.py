import re
from pathlib import Path
from queue import PriorityQueue
from abc import ABC, abstractmethod
from typing import NamedTuple, Callable
from enum import Enum
from functools import partial

import pandas as pd

from ai_data_eng.searching.globals import A_STAR_FILE, DATA_DIR
from ai_data_eng.searching.graph import Graph, Stop
from ai_data_eng.searching.searchning import a_star_print_info, run_solution, assert_connection_path, idxs_to_nodes, \
    print_path, OptimizationType, get_cost_func
from ai_data_eng.searching.utils import time_to_normalized_sec, sec_to_time, distance_m, diff

pd.options.mode.chained_assignment = None


class Heuristic(ABC):

    @abstractmethod
    def compute(self, stop_from: Stop, stop_to: Stop, goal_stop: Stop, conn) -> int:
        return -1

    @abstractmethod
    def check(self, start_stop: Stop, goal_stop: Stop, actual_time: int):
        pass


class MaxVelocityTimeHeuristic(Heuristic):
    def __init__(self):
        super().__init__()
        self.max_vel = 1

    def compute(self, stop_from: Stop, stop_to: Stop, goal_stop: Stop, conn) -> int:
        if conn.arrival_sec > conn.departure_sec:
            self.max_vel = max(self.max_vel,
                               distance_m(stop_from, stop_to) / diff(conn.arrival_sec, conn.departure_sec))
        return distance_m(goal_stop, stop_to) / self.max_vel

    def check(self, start_stop: Stop, goal_stop: Stop, actual_time: int):
        return (distance_m(goal_stop, start_stop) / self.max_vel) <= actual_time


class WeightedAverageTimeHeuristic(Heuristic):

    def __init__(self, alpha=0.01, velocity=10):
        self.alpha = alpha
        self.velocity = velocity

    def compute(self, stop_from: Stop, stop_to: Stop, goal_stop: Stop, conn) -> int:
        dist_from_prev = distance_m(stop_from, stop_to)
        time_from_prev = diff(conn.arrival_sec, conn.departure_sec)
        if time_from_prev > 0:
            self.velocity = self.alpha * (dist_from_prev / time_from_prev) + (1 - self.alpha) * self.velocity
        heuristic_time = distance_m(stop_to, goal_stop) / self.velocity
        return heuristic_time

    def check(self, start_stop: Stop, goal_stop: Stop, actual_time: int):
        return (distance_m(goal_stop, start_stop) / self.velocity) <= actual_time


class ChangeHeuristic(Heuristic):

    def __init__(self):
        pass


def find_path(graph: Graph, heuristic: Heuristic, cost_func: Callable,
              start_stop: str, goal_stop: str, leave_hour: str):
    frontier = PriorityQueue()
    dep_time = time_to_normalized_sec(leave_hour)

    cost_so_far = {}
    # if commuting A -> B, then this will be came_from_conn[B] = A so we can recreate the path
    came_from_conn = {}
    stop_conn = {}
    goal_stop_coords = graph.compute_stop_coords(goal_stop)
    goal_stop = (goal_stop, goal_stop_coords['stop_lat'], goal_stop_coords['stop_lon'])
    # given only stop name consider all possible start stops??
    j = -1
    for candidate_start_stop in graph.get_possible_stops_t(start_stop):
        cost_so_far[candidate_start_stop] = 0
        graph.add_conn(dep_time, candidate_start_stop, j)
        came_from_conn[j] = None
        stop_conn[candidate_start_stop] = j
        frontier.put((cost_so_far[candidate_start_stop], candidate_start_stop))
        j -= 1

    with open(DATA_DIR / ('a_star_runs/' + re.sub(r"\W+", "", start_stop) + '-' + re.sub(r"\W+", "", goal_stop[0])),
              mode='w', encoding='utf-8') as f:

        i = 0
        while not frontier.empty():
            # get the stop with the lowest cost
            _, current = frontier.get()

            conn = graph.conn_at_index(stop_conn[current])

            # consider all possible end stops
            if current[0] == goal_stop[0]:
                goal_stop_index = conn.name
                # theory - first found is the best
                break

            print(f'[{i}]', file=f)
            cost = cost_so_far[current]
            for next_conn in graph.get_earliest_from(dep_time + cost, current, conn['line']).itertuples():
                # cost of commuting start --> current and current --> next
                next_stop = (next_conn.end_stop, next_conn.end_stop_lat, next_conn.end_stop_lon)
                new_cost = cost + cost_func(next_conn.Index, conn.name)
                heuristic_cost = heuristic.compute(current, next_stop, goal_stop, next_conn)
                approx_goal_cost = new_cost + heuristic_cost
                if next_stop not in cost_so_far or new_cost < cost_so_far[next_stop]:
                    a_star_print_info(next_conn, new_cost, heuristic_cost, file=f)
                    cost_so_far[next_stop] = new_cost
                    frontier.put((approx_goal_cost, next_stop))
                    came_from_conn[next_conn.Index] = conn.name
                    stop_conn[next_stop] = next_conn.Index
            i += 1

    return goal_stop_index, came_from_conn, cost_so_far


def a_star(start_stop: str, goal_stop: str, leave_hour: str, heuristic: Heuristic, criterion: OptimizationType):
    with open(A_STAR_FILE / heuristic.__class__.__name__, mode='a', encoding='utf-8') as f:
        print(f'Testcase: {start_stop} -> {goal_stop}\nStart time: {leave_hour}\nRoute', file=f)
        graph, goal_index, came_from, solution_cost, elapsed_time = run_solution(
            partial(find_path, heuristic=heuristic),
            start_stop, goal_stop, leave_hour, criterion)
        # assert heuristic.check(graph.compute_stop_coords(start_stop), graph.compute_stop_coords(goal_stop), solution_cost)
        connections = idxs_to_nodes(graph, goal_index, came_from)
        assert assert_connection_path(time_to_normalized_sec(leave_hour), connections)
        print_path(connections, f)
        print(f'Total trip time is {sec_to_time(solution_cost)}', file=f)
        print(f'Algorithm took {elapsed_time:.2f}s to execute\n', file=f)
