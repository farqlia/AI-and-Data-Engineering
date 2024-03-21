from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from ai_data_eng.searching.graph import Graph, add_constant_change_time
from ai_data_eng.searching.utils import time_to_normalized_sec

DATA_DIR = Path('../data')

@pytest.fixture
def g():
    connection_graph = pd.read_csv(DATA_DIR / 'connection_graph.csv', 
                               usecols=['line', 'departure_time', 'arrival_time', 'start_stop',
       'end_stop', 'start_stop_lat', 'start_stop_lon', 'end_stop_lat',
       'end_stop_lon'])
    return Graph(connection_graph, add_constant_change_time)


def test_get_possible_stops(g):
    print(g.get_possible_stops('Zabrodzie - pętla'))


def test_get_neighbour_stops(g):
    # Shows difference if we don't consider all start and end stops of a given name
    g.add_conn('19:52:00', g.get_possible_stops('Zabrodzie - pętla').iloc[1], -3)
    print(g.get_neighbour_stops(g.rename_stop(g.conn_at_index(-3))))


def test_departure_time(g):
    dep_time = time_to_normalized_sec('08:02:00')
    g.add_conn(dep_time, g.rename_stop(g.conn_at_index(64785)), -1)
    print(add_constant_change_time(g.conn_graph.loc[71820:71821], g.conn_at_index(-1)))

def test_null(g):
    data = {'set_of_numbers': [1, 2, 3, 4, 5, np.nan, 6, 7, np.nan, 8, 9, 10, np.nan]}
    df = pd.DataFrame(data)
    print(df['set_of_numbers'].isnull())

def test_null(g):
    data = {'set_of_numbers': ['1', '2', '', '']}
    df = pd.DataFrame(data)
    print(df['set_of_numbers'] == '')

def test_outgoing_conn(g):
    dep_time = time_to_normalized_sec('08:02:00')
    g.add_conn(dep_time, g.rename_stop(g.conn_at_index(64785)), -1)
    # g.conn_graph.loc[-1, 'line'] = 4
    for row in g.get_earliest_from(g.conn_at_index(-1)):
        print(row)



