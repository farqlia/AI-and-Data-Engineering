import os
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd


def plot_compare_two_players(df1, df2, var, colors=('orange', 'blue'), line_styles=('solid', 'dashed')):
    fig, ax1 = plt.subplots(figsize=(10, 5))

    moves = np.arange(len(df1))

    plt.title(f'Compare {var} for {df1.player} vs {df2.player}')

    ax1.plot(moves, df1[var], color=colors[0], linestyle=line_styles[0], label=df1.player)
    ax1.set_xlabel('Move')
    ax1.set_ylabel(f"{var} ({df1.player})")

    moves = np.arange(len(df2))
    ax2 = ax1.twinx()
    ax2.plot(moves, df2[var], color=colors[1], linestyle=line_styles[1], label=df2.player)
    ax2.set_ylabel(f"{var} ({df2.player})")

    fig.legend()

    plt.show()


def plot_compare_two_variables(df, var1, var2, colors=('orange', 'blue'), line_styles=('solid', 'dashed')):
    fig, ax1 = plt.subplots(figsize=(10, 5))

    moves = np.arange(len(df))

    plt.title(
        f'Compare {var1} vs {var2} for {df.player} player with strategy {df.strategy}, {df.algorithm}, d={df.depth}')

    ax1.plot(moves, df[var1], color=colors[0], linestyle=line_styles[0], label=var1)
    ax1.set_xlabel('Move')
    ax1.set_ylabel(var1)

    ax2 = ax1.twinx()
    ax2.plot(moves, df[var2], color=colors[1], linestyle=line_styles[1], label=var2)
    ax2.set_ylabel(var2)

    fig.legend()

    plt.show()


def compare_matches(df, stat, var):
    _df = df.loc[stat].sort_values(by=['match', 'player'])
    positions = np.arange(len(_df) // 2)  # number of matches to compare
    bar_width = 0.35

    black_players = _df.loc[_df['player'] == 'Black']
    white_players = _df.loc[_df['player'] == 'White']

    bars1 = plt.barh(positions - bar_width / 2, black_players[var], bar_width, color='skyblue', label=f'Black')
    bars2 = plt.barh(positions + bar_width / 2, white_players[var], bar_width, color='salmon', label='White')

    plt.xlabel(var)

    def create_annotation(row):
        return f'{row["strategy"]}, {row["algorithm"]}, d={row["depth"]}'

    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        plt.text(bar1.get_width(), bar1.get_y() + bar1.get_height() / 2, create_annotation(black_players.iloc[i]),
                 ha='left', va='center', color='black', fontsize=10)
        plt.text(bar2.get_width(), bar2.get_y() + bar2.get_height() / 2, create_annotation(white_players.iloc[i]),
                 ha='left', va='center', color='black', fontsize=10)

    plt.yticks(positions, black_players['winner'])

    plt.title(f'Compare {stat} of {var} across matches')
    plt.legend()


def compare_algorithms(df, stat, var, depths, names):
    vars = ['depth', 'algorithm']
    _df = df.loc[stat, [var, *vars]].groupby(vars).mean().reset_index().sort_values(by=['algorithm', 'depth'])
    _df = _df.loc[_df['depth'].isin(depths)]
    positions = np.arange(len(_df))  # number of matches to compare
    bar_width = 0.35

    bars1 = plt.bar(positions - bar_width / 2, _df.loc[_df['algorithm'] == names[0], var], bar_width,
                    color='skyblue', label=names[0])
    bars2 = plt.bar(positions + bar_width / 2, _df[_df['algorithm'] == names[1], var], bar_width, color='salmon',
                    label=names[1])

    plt.xticks(positions, depths)
    plt.xlabel('Depth')
    plt.ylabel('Compute time')

    plt.title(f'Compare {stat} of {var} across matches')
    plt.legend()