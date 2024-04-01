import os
from datetime import datetime
from pathlib import Path
from typing import Tuple

Stop = Tuple[str, float, float]
UPPER_BOUND_CONN_TIME = 240.0

DEBUG = True

DATA_DIR = Path('../data')
if DEBUG:
    RESULTS = DATA_DIR / 'debug-tabu'
else:
    RESULTS = DATA_DIR / 'results'
os.makedirs(RESULTS, exist_ok=True)
DIJKSTRA = RESULTS / "dijkstra"
os.makedirs(DIJKSTRA, exist_ok=True)
A_STAR_RUNS_T = RESULTS / 'a-star-t'
os.makedirs(A_STAR_RUNS_T, exist_ok=True)
A_STAR_RUNS_P = RESULTS / 'a-star-p'
os.makedirs(A_STAR_RUNS_P, exist_ok=True)
A_STAR_RUNS_CUSTOM = RESULTS / 'a-star-custom'
os.makedirs(A_STAR_RUNS_CUSTOM, exist_ok=True)
