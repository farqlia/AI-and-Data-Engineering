from pathlib import Path

import numpy as np
import pandas as pd

from ai_data_eng.searching.utils import time_to_normalized_sec, diff

pd.options.mode.chained_assignment = None

DATA_DIR = Path('../data')

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

    def get_start_idx(self):
        return -1

    def add_conn(self, dep_time: int, conn: pd.Series, index: int):
         self.conn_graph.loc[index] = pd.Series({'line': '', 'start_stop': conn['stop'], 'end_stop': conn['stop'], 'departure_sec': dep_time, 'arrival_sec': dep_time,
                                                               'start_stop_lat': conn['stop_lat'], 'start_stop_lon': conn['stop_lon'],
                                                               'end_stop_lat': conn['stop_lat'], 'end_stop_lon': conn['stop_lon']})

    def get_possible_stops(self, stop: str):
        end_stops = self.rename_stop(self.conn_graph[self.conn_graph['end_stop'] == stop].loc[:, END_STOP_COLS])
        start_stops = self.rename_stop(self.conn_graph[self.conn_graph['start_stop'] == stop].loc[:, START_STOP_COLS], 'start')
        return pd.concat([end_stops, start_stops]).drop_duplicates()

    # We could take as the initial stop the closest stop to the goal stop
    def compute_stop_coords(self, stop: str):
        stops = self.get_possible_stops(stop)
        return stops.iloc[0][['stop_lat', 'stop_lon']]
    
    def get_end_stop(self, stop: str):
        coords = self.compute_stop_coords(stop)
        return pd.Series({'end_stop': stop, 'end_stop_lat': coords['end_stop_lat'], 'end_stop_lon': coords['end_stop_lon']})
    
    def get_stop_names(self):
        '''? this may not make sense because sometimes the routes are different'''
        return self.conn_graph['start_stop'].unique()
    
    def stop_as_tuple(self, stop):
        return (stop['stop'], stop['stop_lat'], stop['stop_lon'])
    
    def is_start_equal_to(self, stop: pd.Series) -> pd.Series:
        return ((self.conn_graph['start_stop'] == stop['stop']) &
                (self.conn_graph['start_stop_lat'] == stop['stop_lat']) &
                (self.conn_graph['start_stop_lon'] == stop['stop_lon']))

    def is_end_equal_to(self, stop: pd.Series) -> pd.Series:
        return ((self.conn_graph['end_stop'] == stop['stop']) &
                (self.conn_graph['end_stop_lat'] == stop['stop_lat']) &
                (self.conn_graph['end_stop_lon'] == stop['stop_lon']))

    def is_line_valid(self):
        return self.conn_graph['line'] != ''

    def rename_stop(self, stop, prefix='end'):
        if isinstance(stop, pd.DataFrame):
            return stop.rename({f'{prefix}_stop_lat': 'stop_lat', 
                                        f'{prefix}_stop_lon': 'stop_lon', f'{prefix}_stop': 'stop'}, axis=1)
        else: 
            return stop.rename({f'{prefix}_stop_lat': 'stop_lat', 
                                        f'{prefix}_stop_lon': 'stop_lon', f'{prefix}_stop': 'stop'})

    def get_neighbour_stops(self, prev_conn: pd.Series) -> pd.Series:
        '''Returns neighbouring end stops'''
        # return self.conn_graph[self.conn_graph['start_stop'] == start_stop][['line', 'end_stop']].drop_duplicates()
        return self.rename_stop(self.conn_graph[self.is_start_equal_to(prev_conn)][END_STOP_COLS]).drop_duplicates()

    
    def get_conn_valid_time_arrivals(self, prev_stop: pd.Series, next_stop: pd.Series) -> pd.Series:
        conn = self.conn_graph[self.is_start_equal_to(prev_stop)
                               & self.is_end_equal_to(next_stop) & self.is_line_valid()]
 
        time_arrv_diff = diff(conn['arrival_sec'], prev_stop['arrival_sec'])
        time_dep_diff = diff(conn['departure_sec'], self.change_time_compute(conn, prev_stop))
        
        differences = (time_arrv_diff - time_dep_diff) >= 0
        valid_time_arrv_diff = time_arrv_diff[differences]

        return valid_time_arrv_diff

    def get_earliest_conn(self, start_stop: pd.Series, end_stop: pd.Series) -> pd.Series:
        '''Returns the earliest connection between two stops'''
        valid_time_arrv_diff = self.get_conn_valid_time_arrivals(start_stop, end_stop)

        return self.conn_graph.loc[valid_time_arrv_diff.idxmin()] if len(valid_time_arrv_diff) > 0 else pd.Series()
    
    def get_earliest_from(self, start_stop: pd.Series):
        '''Returns all earliest connections to all neighbouring stops'''
        start_stop = self.rename_stop(start_stop)
        possible_conns = [self.get_earliest_conn(start_stop, end_stop) for 
                (i, end_stop) in self.get_neighbour_stops(start_stop).iterrows()]
        return [conn for conn in possible_conns if len(conn) > 0]

    def time_cost_between_conns(self, next_idx: int, curr_idx: int = None) -> int:
        cost = diff(self.conn_graph.loc[next_idx, 'arrival_sec'], self.conn_graph.loc[curr_idx, 'arrival_sec'])
        return cost
    
    def conn_at_index(self, index: int) -> pd.Series:
        return self.conn_graph.loc[index] 
    

def add_constant_change_time(conns, stop):
    line_cont = ((stop['line'] == '') | (conns['line'] == stop['line']))
    dept_times = pd.Series(data=stop['arrival_sec'], index=conns.index)
    dept_times.loc[~line_cont] = (dept_times.loc[~line_cont] + 60) % (24 * 3600)
    return dept_times