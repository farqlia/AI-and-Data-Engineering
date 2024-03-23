from abc import ABC, abstractmethod

import pandas as pd

from ai_data_eng.searching.graph import Stop
from ai_data_eng.searching.searchning import OptimizationType
from ai_data_eng.searching.utils import distance_m, diff


class Heuristic(ABC):

    def __init__(self, criterion: OptimizationType):
        self.criterion = criterion

    @abstractmethod
    def compute(self, start_stop: Stop, stop_from: Stop, stop_to: Stop, goal_stop: Stop,
                prev_conn: pd.Series, next_conn: pd.Series, cost: int = None) -> int:
        return -1

    @abstractmethod
    def check(self, start_stop: Stop, goal_stop: Stop, actual_time: int):
        pass


class MaxVelocityTimeHeuristic(Heuristic):
    def __init__(self):
        super().__init__(OptimizationType.TIME)
        self.max_vel = 1

    def compute(self, start_stop: Stop, stop_from: Stop, stop_to: Stop, goal_stop: Stop,
                prev_conn: pd.Series, next_conn: pd.Series, cost: int = None) -> int:
        if next_conn.arrival_sec > next_conn.departure_sec:
            self.max_vel = max(self.max_vel,
                               distance_m(stop_from, stop_to) / diff(next_conn.arrival_sec, next_conn.departure_sec))
        return distance_m(goal_stop, stop_to) / self.max_vel

    def check(self, start_stop: Stop, goal_stop: Stop, actual_time: int):
        return (distance_m(goal_stop, start_stop) / self.max_vel) <= actual_time


class WeightedAverageTimeHeuristic(Heuristic):

    def __init__(self, alpha=0.01, velocity=10):
        super().__init__(OptimizationType.TIME)
        self.alpha = alpha
        self.velocity = velocity

    def compute(self, start_stop: Stop, stop_from: Stop, stop_to: Stop, goal_stop: Stop,
                prev_conn: pd.Series, next_conn: pd.Series, cost: int = None) -> int:
        dist_from_prev = distance_m(stop_from, stop_to)
        # not sure which times to take here
        time_from_prev = diff(next_conn.arrival_sec, next_conn.departure_sec)
        if time_from_prev > 0:
            self.velocity = self.alpha * (dist_from_prev / time_from_prev) + (1 - self.alpha) * self.velocity
        heuristic_time = distance_m(stop_to, goal_stop) / self.velocity
        return heuristic_time

    def check(self, start_stop: Stop, goal_stop: Stop, actual_time: int):
        return (distance_m(goal_stop, start_stop) / self.velocity) <= actual_time


class ChangeHeuristic(Heuristic):

    def __init__(self, alpha=0.01):
        super().__init__(OptimizationType.CHANGES)
        self.N = 1
        self.alpha = alpha
        self.mean_time_between_stops = 300

    def compute(self, start_stop: Stop, stop_from: Stop, stop_to: Stop, goal_stop: Stop,
                prev_conn, next_conn, cost: int = None) -> int:
        are_stops_different = stop_from != stop_to
        is_first_stop = prev_conn.line == ''
        are_lines_different = (not is_first_stop) & (prev_conn.line != next_conn.line)
        is_change = not is_first_stop and (are_lines_different or are_stops_different)
        heuristic_cost = 0
        time_diff = diff(next_conn.departure_sec, prev_conn.arrival_sec)
        if is_first_stop:
            heuristic_cost += time_diff / (3 * 3600)
        # elif is_change:
            # this should be mean
            # heuristic_cost += time_diff / self.mean_time_between_stops
        # approximate number of changes
        # self.N = self.alpha * cost + (1 - self.alpha) * self.N
        heuristic_cost += distance_m(stop_to, goal_stop) / distance_m(start_stop, goal_stop) * max(cost, self.N)
        return heuristic_cost

    def check(self, start_stop: Stop, goal_stop: Stop, actual_time: int):
        pass