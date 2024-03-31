import math
from typing import Union
import re

import geopy.distance
import pandas as pd

from ai_data_eng.searching.globals import Stop


def join_stop_names(s1, s2):
    return re.sub(r"\W+", "", s1) + '-' + re.sub(r"\W+", "", s2)

def separate_time(time):
    return [int(tp) for tp in time.split(':')]

def to_seconds(time: str) -> int:
    h, m, s = separate_time(time)
    return int(h * 3600 + m * 60 + s)

def time_to_normalized_sec(time: str) -> int:
    return to_seconds(time) % (3600 * 24)

def diff(ts: Union[pd.Series, int], td: int) -> Union[int, pd.Series]:
    '''Function that returns difference between ts and td times expressed as seconds 
        - note that this will never be a negative value'''
    d = ts - td 
    if isinstance(ts, pd.Series):
        d[d < 0] += 24 * 3600
    elif d < 0:
        d += 24 * 3600
    return d 

def sec_to_time(seconds: int) -> str:
    seconds = int(seconds)
    hour = (seconds // 3600)
    minutes = (seconds % 3600) // 60 
    secs = (seconds % 3600) % 60 
    return f'{hour:02d}:{minutes:02d}:{secs:02d}'


def distance_m(stop_from: Stop, stop_to: Stop):
    return (geopy.distance.geodesic((stop_from[1], stop_from[2]), (stop_to[1], stop_to[2])).m)

def distance_round(stop_from: Stop, stop_to: Stop):
    straight_dis = distance_m(stop_from, stop_to)
    return round(math.pi * straight_dis / 2, 2)

def approximate_velocity(stop_from: Stop, stop_to: Stop, conn_time: float):
    return distance_m(stop_from, stop_to) / conn_time

def approximate_velocity_round(stop_from: Stop, stop_to: Stop, conn_time: float):
    return distance_round(stop_from, stop_to) / conn_time


def rename_stop(stop, prefix='end'):
    if isinstance(stop, pd.DataFrame):
        return stop.rename({f'{prefix}_stop_lat': 'stop_lat',
                            f'{prefix}_stop_lon': 'stop_lon', f'{prefix}_stop': 'stop'}, axis=1, errors='ignore')
    else:
        return stop.rename({f'{prefix}_stop_lat': 'stop_lat',
                            f'{prefix}_stop_lon': 'stop_lon', f'{prefix}_stop': 'stop'}, errors='ignore')

def stop_as_tuple(stop, prefix='end'):
    stop = rename_stop(stop, prefix)
    return (stop['stop'], stop['stop_lat'], stop['stop_lon'])