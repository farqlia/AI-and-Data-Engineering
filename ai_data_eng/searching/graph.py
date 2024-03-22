from pathlib import Path
from typing import Tuple, List

import numpy as np
import pandas as pd
from pandas import DataFrame

from ai_data_eng.searching.globals import Stop
from ai_data_eng.searching.utils import time_to_normalized_sec, diff

pd.options.mode.chained_assignment = None

END_STOP_COLS = ['end_stop', 'end_stop_lat', 'end_stop_lon']
START_STOP_COLS = ['start_stop', 'start_stop_lat', 'start_stop_lon']


class Graph:

    def __init__(self, conn_graph, add_change_time):
        self.conn_graph = conn_graph
        self.change_time_compute = add_change_time
        self.stops = None
        self.transform()

    def transform(self):
        '''Applies time transformation functions to departure and arrival times - the results are available in new columns'''
        self.conn_graph = self.conn_graph.drop_duplicates()
        self.conn_graph.loc[:, 'line'] = self.conn_graph.loc[:, 'line'].astype(str)
        self.conn_graph.loc[:, 'departure_sec'] = self.conn_graph['departure_time'].apply(time_to_normalized_sec)
        self.conn_graph.loc[:, 'arrival_sec'] = self.conn_graph['arrival_time'].apply(time_to_normalized_sec)


    def add_conn(self, dep_time: int, stop: Stop, index: int):
         self.conn_graph.loc[index] = pd.Series({'line': '', 'start_stop': stop[0], 'end_stop': stop[0], 'departure_sec': dep_time, 'arrival_sec': dep_time,
                                                               'start_stop_lat': stop[1], 'start_stop_lon': stop[2],
                                                               'end_stop_lat': stop[1], 'end_stop_lon': stop[2]})

    def get_possible_stops(self, stop: str):
        end_stops = self.rename_stop(self.conn_graph[self.conn_graph['end_stop'] == stop].loc[:, END_STOP_COLS])
        start_stops = self.rename_stop(self.conn_graph[self.conn_graph['start_stop'] == stop].loc[:, START_STOP_COLS], 'start')
        return pd.concat([end_stops, start_stops]).drop_duplicates()

    def get_possible_stops_t(self, stop: str):
        s_df = self.get_possible_stops(stop)
        return [self.stop_as_tuple(s) for (i, s) in s_df.iterrows()]

    # We could take as the initial stop the closest stop to the goal stop
    def compute_stop_coords(self, stop: str):
        stops = self.get_possible_stops(stop)
        return stops[['stop_lat', 'stop_lon']].mean()

    def stop_as_tuple(self, stop):
        return (stop['stop'], stop['stop_lat'], stop['stop_lon'])
    
    def is_start_equal_to(self, stop: Stop) -> pd.Series:
        return ((self.conn_graph['start_stop'] == stop[0]) &
                (self.conn_graph['start_stop_lat'] == stop[1]) &
                (self.conn_graph['start_stop_lon'] == stop[2]))

    def is_end_equal_to(self, stop: Stop) -> pd.Series:
        return ((self.conn_graph['end_stop'] == stop[0]) &
                (self.conn_graph['end_stop_lat'] == stop[1]) &
                (self.conn_graph['end_stop_lon'] == stop[2]))

    def is_line_valid(self):
        return self.conn_graph['line'] != ''

    def rename_stop(self, stop, prefix='end'):
        if isinstance(stop, pd.DataFrame):
            return stop.rename({f'{prefix}_stop_lat': 'stop_lat', 
                                        f'{prefix}_stop_lon': 'stop_lon', f'{prefix}_stop': 'stop'}, axis=1)
        else: 
            return stop.rename({f'{prefix}_stop_lat': 'stop_lat', 
                                        f'{prefix}_stop_lon': 'stop_lon', f'{prefix}_stop': 'stop'})

    def get_neighbour_stops(self, stop: Stop) -> pd.Series:
        '''Returns neighbouring end stops'''
        # return self.conn_graph[self.conn_graph['start_stop'] == start_stop][['line', 'end_stop']].drop_duplicates()
        return self.rename_stop(self.conn_graph[self.is_start_equal_to(stop)][END_STOP_COLS]).drop_duplicates()

    def get_neighbour_stops_t(self, stop: Stop) -> List[Stop]:
        n_df = self.get_neighbour_stops(stop)
        return [self.stop_as_tuple(s) for (i, s) in n_df.iterrows()]

    def get_earliest_from(self, dep_time: int, start_stop: Stop, line: str=None):
        '''Returns all earliest connections to all neighbouring stops'''
        possible_conns = self.conn_graph[(self.conn_graph['start_stop'] == start_stop[0]) & self.is_line_valid()]

        time_arrv_diff = diff(possible_conns['arrival_sec'], dep_time)
        time_dep_diff = diff(possible_conns['departure_sec'],
                             self.change_time_compute(possible_conns, start_stop, dep_time, line))

        differences = (time_arrv_diff - time_dep_diff) >= 0
        valid_time_arrv_diff = time_arrv_diff[differences].sort_values()

        first_conns = ((possible_conns.loc[valid_time_arrv_diff.index]
                       .groupby(['start_stop', 'end_stop', 'start_stop_lat', 'start_stop_lon', 'end_stop_lat', 'end_stop_lon']))
                       .head(1))

        return first_conns

    def time_cost_between_conns(self, next_idx: int, curr_idx: int = None) -> int:
        cost = diff(self.conn_graph.loc[next_idx, 'arrival_sec'], self.conn_graph.loc[curr_idx, 'arrival_sec'])
        return cost
    
    def conn_at_index(self, index: int) -> pd.Series:
        return self.conn_graph.loc[index]


def is_changing(conns, stop: Stop, line: str) -> pd.DataFrame:
    return (conns['start_stop_lat'] != stop[1]) | (conns['start_stop_lon'] != stop[2]) | ((line != '') & (conns['line'] != line))


def add_constant_change_time(conns, stop: Stop, dep_time: int, line: str=None, change_time=60):
    dept_times = pd.Series(data=dep_time, index=conns.index)
    is_change = is_changing(conns, stop, line)
    dept_times.loc[is_change] = (dept_times.loc[is_change] + change_time) % (24 * 3600)
    return dept_times