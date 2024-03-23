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
                prev_conn: pd.Series, next_conn: pd.Series) -> int:
        return -1

    @abstractmethod
    def check(self, start_stop: Stop, goal_stop: Stop, actual_time: int):
        pass


class MaxVelocityTimeHeuristic(Heuristic):
    def __init__(self):
        super().__init__(OptimizationType.TIME)
        self.max_vel = 1

    def compute(self, start_stop: Stop, stop_from: Stop, stop_to: Stop, goal_stop: Stop,
                prev_conn: pd.Series, next_conn: pd.Series) -> int:
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
                prev_conn: pd.Series, next_conn: pd.Series) -> int:
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

    def __init__(self):
        super().__init__(OptimizationType.CHANGES)
        self.N = 2

    def compute(self, start_stop: Stop, stop_from: Stop, stop_to: Stop, goal_stop: Stop,
                prev_conn, next_conn) -> int:
        return distance_m(stop_to, goal_stop) / distance_m(start_stop, goal_stop) * self.N

    def check(self, start_stop: Stop, goal_stop: Stop, actual_time: int):
        pass