import os
from pathlib import Path

DATA_DIR = Path('../data')
TABU_SEARCH_DIR_TIME = DATA_DIR / 'tabu-search-t'
TABU_SEARCH_DIR_TIME_LS = DATA_DIR / 'tabu-search-t-ls'
TABU_SEARCH_DIR_CHANGES = DATA_DIR / 'tabu-search-p'
os.makedirs(TABU_SEARCH_DIR_TIME, exist_ok=True)
os.makedirs(TABU_SEARCH_DIR_TIME_LS, exist_ok=True)
os.makedirs(TABU_SEARCH_DIR_CHANGES, exist_ok=True)
