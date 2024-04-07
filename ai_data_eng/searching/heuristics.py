import math
from abc import ABC, abstractmethod

import pandas as pd

from ai_data_eng.searching.graph import Stop
from ai_data_eng.searching.searchning import OptimizationType, TIME_AND_CHANGE_HEURISTIC
from ai_data_eng.searching.utils import distance_m, diff, rename_stop, stop_as_tuple


class Heuristic(ABC):

    def __init__(self, criterion: OptimizationType):
        self.criterion = criterion

    @abstractmethod
    def compute(self, start_stop: Stop, goal_stop: Stop, prev_conn: pd.Series, next_conn: pd.Series,
                cost: int = None) -> int:
        return -1

    @abstractmethod
    def check(self, start_stop: Stop, goal_stop: Stop, actual_time: int):
        pass


class MockHeuristic(Heuristic):

    def __init__(self):
        super().__init__(OptimizationType.CHANGES)

    def compute(self, start_stop: Stop, goal_stop: Stop, prev_conn: pd.Series, next_conn: pd.Series,
                cost: int = None) -> int:
        return 0

    def check(self, start_stop: Stop, goal_stop: Stop, actual_time: int):
        pass


class MaxVelocityTimeHeuristic(Heuristic):
    def __init__(self):
        super().__init__(OptimizationType.TIME)
        self.max_vel = 1

    def compute(self, start_stop: Stop, goal_stop: Stop,
                prev_conn: pd.Series, next_conn: pd.Series, cost: int = None) -> int:
        stop_from = stop_as_tuple(rename_stop(prev_conn))
        stop_to = stop_as_tuple(rename_stop(next_conn))
        if next_conn.arrival_sec > next_conn.departure_sec:
            self.max_vel = max(self.max_vel,
                               distance_m(stop_from, stop_to) / diff(next_conn.arrival_sec, next_conn.departure_sec))
        return distance_m(goal_stop, stop_to) / self.max_vel

    def check(self, start_stop: Stop, goal_stop: Stop, actual_time: int):
        return (distance_m(goal_stop, start_stop) / self.max_vel) <= actual_time


class WeightedAverageTimeHeuristic(Heuristic):

    def __init__(self, alpha=0.01, velocity=10, epsilon=0.1):
        super().__init__(OptimizationType.TIME)
        self.alpha = alpha
        self.velocity = velocity
        self.epsilon = epsilon

    def compute(self, start_stop: Stop, goal_stop: Stop,
                prev_conn: pd.Series, next_conn: pd.Series, cost: int = None) -> int:
        stop_from = stop_as_tuple(rename_stop(prev_conn))
        stop_to = (next_conn.end_stop, next_conn.end_stop_lat, next_conn.end_stop_lon)
        dist_from_prev = distance_m(stop_from, stop_to)
        # not sure which times to take here
        time_from_prev = diff(next_conn.arrival_sec, next_conn.departure_sec)
        if time_from_prev > 0:
            self.velocity = self.alpha * (dist_from_prev / time_from_prev) + (1 - self.alpha) * self.velocity
        if cost > 0 and self.is_close_to_real_value(start_stop, prev_conn, cost):
            self.velocity *= 2
        heuristic_time = math.floor(distance_m(stop_to, goal_stop) / self.velocity)
        return heuristic_time

    def is_close_to_real_value(self, start_stop: Stop, prev_conn: pd.Series, cost: int = None):
        stop_from = stop_as_tuple(rename_stop(prev_conn))
        prev_dist = distance_m(start_stop, stop_from)
        heuristic_time = prev_dist / self.velocity
        return (heuristic_time - cost) / cost > self.epsilon

    def check(self, start_stop: Stop, goal_stop: Stop, actual_time: int):
        pass


class TimeAndChangeHeuristic(Heuristic):

    def __init__(self):
        super().__init__(OptimizationType.TIME_AND_CHANGES)
        self.a = TIME_AND_CHANGE_HEURISTIC['a']
        self.b = TIME_AND_CHANGE_HEURISTIC['b']
        self.time_heurists = WeightedAverageTimeHeuristic()
        self.change_heuristic = ChangeHeuristic()

    def compute(self, start_stop: Stop, goal_stop: Stop,
                prev_conn, next_conn, cost: int = None) -> int:
        return self.a * self.time_heurists.compute(start_stop, goal_stop, prev_conn, next_conn,
                                                   cost) + self.b * self.change_heuristic.compute(start_stop, goal_stop,
                                                                                                  prev_conn, next_conn,
                                                                                                  cost)

    def check(self, start_stop: Stop, goal_stop: Stop, actual_time: int):
        pass


class ChangeHeuristic(Heuristic):

    def __init__(self, alpha=0.01):
        super().__init__(OptimizationType.CHANGES)
        self.N = 1
        self.alpha = alpha
        self.mean_time_between_stops = 300

    def compute(self, start_stop: Stop, goal_stop: Stop,
                prev_conn, next_conn, cost: int = None) -> int:
        stop_to = (next_conn.end_stop, next_conn.end_stop_lat, next_conn.end_stop_lon)
        is_first_stop = prev_conn.line == ''
        heuristic_cost = 0
        time_diff = diff(next_conn.departure_sec, prev_conn.arrival_sec)
        if is_first_stop:
            heuristic_cost += time_diff / (3 * 3600)
        heuristic_cost += distance_m(stop_to, goal_stop) / distance_m(start_stop, goal_stop) * max(cost, self.N)
        return heuristic_cost

    def check(self, start_stop: Stop, goal_stop: Stop, actual_time: int):
        pass
