from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from ai_data_eng.searching.globals import DATA_DIR
from ai_data_eng.searching.graph import Graph, add_constant_change_time, is_changing, add_const_change_time, is_conn_change
from ai_data_eng.searching.utils import time_to_normalized_sec
from ai_data_eng.searching.heuristics import MaxVelocityTimeHeuristic

@pytest.fixture
def g():
    connection_graph = pd.read_csv(DATA_DIR / 'connection_graph.csv', 
                               usecols=['line', 'departure_time', 'arrival_time', 'start_stop',
       'end_stop', 'start_stop_lat', 'start_stop_lon', 'end_stop_lat',
       'end_stop_lon'])
    return Graph(connection_graph, add_const_change_time)


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



def test_outgoing_from(g):
    unique_conns = g.conn_graph.loc[g.conn_graph['start_stop'] == 'PL. GRUNWALDZKI', ['start_stop',
       'end_stop', 'start_stop_lat', 'start_stop_lon', 'end_stop_lat',
       'end_stop_lon']].drop_duplicates()
    print(unique_conns[['start_stop',
       'end_stop']])


def test_is_changing(g):
    stop = g.stop_as_tuple(g.rename_stop(g.conn_at_index(14027)))
    print(g.conn_at_index(14027))
    print(is_changing(g.conn_graph.loc[14025:14028], stop, 'D'))


def test_outgoing_from(g):
    index = 1
    print(g.rename_stop(g.conn_at_index(index)))
    conns = g.get_earliest_from(time_to_normalized_sec('08:00:00'), g.stop_as_tuple(g.rename_stop(g.conn_at_index(index))), '')
    print([conn for conn in conns])


def test_outgoing_from_2(g):
    # ('PL. GRUNWALDZKI', 51.11114106, 17.0611933)
    print(g.get_neighbour_stops_t(('PL. GRUNWALDZKI', 51.11114106, 17.0611933)))
    conns = g.get_earliest_from(time_to_normalized_sec('20:32:00'), ('PL. GRUNWALDZKI', 51.11114106, 17.0611933), '')
    print([(conn.line, conn.departure_time) for conn in conns.itertuples()])


def test_different_approach(g):
    conns = g.conn_graph.loc[g.conn_graph['start_stop'] == 'PL. GRUNWALDZKI']
    grouped = conns.groupby(['start_stop', 'end_stop', 'start_stop_lat',
                             'start_stop_lon', 'end_stop_lat',  'end_stop_lon'])
    first_rows = grouped.head(1)
    print(first_rows)

    for row in first_rows.itertuples():
        print(row.Index)


def test_heuristic(g):
    s1 = ('PL. GRUNWALDZKI', 51.111452, 17.060529)
    s2 = ('Kliniki - Politechnika Wrocławska', 51.10920637, 17.06641438)
    s3 = ('BISKUPIN', 51.10125726, 17.10914151)
    conn = g.conn_at_index(550448)
    print(MaxVelocityTimeHeuristic().__class__.__name__)
    print(MaxVelocityTimeHeuristic().compute(s1, s2, s3, conn))


def test_change_cost(g):
    stop = g.stop_as_tuple(g.rename_stop(g.conn_at_index(14027)))
    print(g.conn_at_index(14027))
    print(g.get_earliest_from(time_to_normalized_sec('23:01:00'), stop))
    print(g.change_cost_between_conns(g.conn_at_index(14028), stop, 'D'))
    print(g.change_cost_between_conns(g.conn_at_index(319982), stop, '19'))


def test_neigh_lines(g):
    print(g.get_possible_stops_t('PL. GRUNWALDZKI'))
    print(g.get_neighbour_lines('PL. GRUNWALDZKI'))
    print(g.compute_stop_coords('PL. GRUNWALDZKI'))

def test_is_conn_changed(g):
    subconn = g.conn_graph.loc[14555:14559]
    print(subconn.loc[~is_conn_change(g.conn_graph.loc[14557], subconn)])

def test_add_change_conn_time(g):
    subconn = g.conn_graph.loc[14555:14559]
    print(add_const_change_time(subconn, g.conn_graph.loc[14557]))

def test_get_earliest_line_cont(g):
    print(g.get_earliest_from_with_and_without_change(g.conn_graph.loc[14557]))

def test_possible_stop_names(g):
    print(g.get_neighbour_stops('PL. GRUNWALDZKI'))