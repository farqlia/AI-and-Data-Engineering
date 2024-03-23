import os
from datetime import datetime
from pathlib import Path
from typing import Tuple

Stop = Tuple[str, float, float]

DEBUG = True

DATA_DIR = Path('../data')
RESULTS = DATA_DIR / 'results'
os.makedirs(RESULTS, exist_ok=True)
DIJKSTRA_FILE = RESULTS / "dijkstra"
A_STAR_RUNS_T_FILE = RESULTS / 'a-star-t'
A_STAR_RUNS_P_FILE = RESULTS / 'a-star-p'