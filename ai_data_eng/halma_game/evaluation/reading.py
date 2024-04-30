import os
from pathlib import Path

import pandas as pd

from ai_data_eng.halma_game.evaluation.computation import jump_size


def match_name(match_dir):
    return '_'.join(str(match_dir).split('\\')[-3:])


def get_configuration(match_dir, date_prefix):
    elements = str(match_dir).split('\\')
    strategies, depths, algorithms = elements[-1].split('-'), elements[-2].split('-'), elements[-3].split('-')
    if len(algorithms) > 2:
        algorithms = ['-'.join(algorithms[:2]), '-'.join(algorithms[2:])]
    if os.path.exists(match_dir / f'{date_prefix}-stats'):
        match_results = pd.read_csv(match_dir / f'{date_prefix}-stats', sep=';', names=['Total moves', 'Winner'])
    else:
        match_results = pd.DataFrame(data={'Total moves': [0], 'Winner': ['None']})
    config = {
        'black': {
            'strategy': strategies[0].split('.')[1].lower(), 'depth': depths[0], 'algorithm': algorithms[0]
        },
        'white': {
            'strategy': strategies[1].split('.')[1].lower(), 'depth': depths[1], 'algorithm': algorithms[1]
        },
        'match': match_name(match_dir),
        'winner': match_results.loc[0, 'Winner']
    }

    return config


def add_metadata(dfs, players, match_dir, date_prefix):
    config = get_configuration(match_dir, date_prefix)
    for (df, player) in zip(dfs, players):
        df.player = player
        df.strategy = config[player]['strategy']
        df.depth = config[player]['depth']
        df.algorithm = config[player]['algorithm']
        df.match = config['match']
        df.winner = config['winner']


def read_match(match_dir: Path, date_prefix: str=None):
    header = ['Move from', 'Move to', 'Compute time', 'Tree size', 'Eval value']
    if not date_prefix:
        date_prefix = '-'.join(str(os.listdir(match_dir)[0]).split('-')[:2])
    player_black = pd.read_csv(match_dir / f'{date_prefix}-PLAYER.BLACK',
                                       names=header, sep=';')
    player_white = pd.read_csv(match_dir / f'{date_prefix}-PLAYER.WHITE',
                                       names=header, sep=';')
    for df in [player_black, player_white]:
        df['Jump size'] = df.apply(lambda x: jump_size(x.iloc[0], x.iloc[1]), axis=1)
    add_metadata([player_black, player_white], ['black', 'white'], match_dir, date_prefix)
    return player_black, player_white