import numpy as np
import pandas as pd

from ai_data_eng.halma_game.utils import split


def jump_size(move_from, move_to):
    y_f, x_f = split(move_from)
    y_t, x_t = split(move_to)
    return abs(y_f-y_t) + abs(x_f - x_t)


def get_match_stats(player_black, player_white):
    total_stats = []
    for (df, player) in zip([player_black, player_white], ['Black', 'White']):
        stats_df = df[['Compute time', 'Tree size', 'Eval value', 'Jump size']].agg([np.mean, np.sum, np.max, np.min])
        stats_df['player'] = player
        stats_df['strategy'] = df.strategy
        stats_df['algorithm'] = df.algorithm
        stats_df['depth'] = df.depth
        stats_df['match'] = df.match
        stats_df['winner'] = df.winner
        total_stats.append(stats_df)
    return pd.concat(total_stats).apply(lambda x: np.round(x, 2))