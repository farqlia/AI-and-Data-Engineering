from functools import partial

import pandas as pd

from ai_data_eng.searching.globals import DATA_DIR
from ai_data_eng.searching.graph import add_const_change_time, Graph
from ai_data_eng.searching.searchning import OptimizationType
from ai_data_eng.tabu_search.tabu_search import tabu_search

vis_stops = ['Krucza', 'Trzebnicka', 'Renoma', 'most Grunwaldzki']
start_stop = 'PL. GRUNWALDZKI'
leave_hour = '08:00:00'

if __name__ == "__main__":
    connection_graph = pd.read_csv(DATA_DIR / 'connection_graph.csv',
                                   usecols=['line', 'departure_time', 'arrival_time', 'start_stop',
                                            'end_stop', 'start_stop_lat', 'start_stop_lon', 'end_stop_lat',
                                            'end_stop_lon'])
    g = Graph(connection_graph, partial(add_const_change_time, change_time=0))

    new_sol = tabu_search(g, OptimizationType.TIME, start_stop, vis_stops, leave_hour)