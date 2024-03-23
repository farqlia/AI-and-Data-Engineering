import os
from pathlib import Path
from datetime import datetime
from typing import Tuple

Stop = Tuple[str, float, float]

DEBUG = True

DATA_DIR = Path('../data')
DIJKSTRA_DIR = Path('../data/dijkstra_results')
os.makedirs(DIJKSTRA_DIR, exist_ok=True)
DIJKSTRA_FILE = DIJKSTRA_DIR / f"dijkstra-{datetime.now().strftime('%Y%m%d-%H%M')}"
A_STAR_FILE = Path('../data/a_star_results') / f"a-star-{datetime.now().strftime('%Y%m%d-%H%M')}"
A_STAR_RUNS = Path('../data/a_star_runs')
os.makedirs(A_STAR_RUNS, exist_ok=True)