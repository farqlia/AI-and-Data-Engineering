from typing import Union

import pandas as pd


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