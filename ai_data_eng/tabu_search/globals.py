import os
from pathlib import Path

DATA_DIR = Path('../data')
TABU_SEARCH_DIR = DATA_DIR / 'tabu-search'
TABU_SEARCH_2_DIR = DATA_DIR / 'tabu-search-2'
os.makedirs(TABU_SEARCH_DIR, exist_ok=True)
os.makedirs(TABU_SEARCH_2_DIR, exist_ok=True)
