from pathlib import Path
from datetime import datetime
from typing import Tuple

Stop = Tuple[str, float, float]

DATA_DIR = Path('../data')
DIJKSTRA_FILE = Path('../data/dijkstra_runs') / f"dijkstra-{datetime.now().strftime('%Y%m%d-%H%M')}"
A_STAR_FILE = Path('../data/a_star_runs')
