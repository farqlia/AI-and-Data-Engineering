import numpy as np
from matplotlib import pyplot as plt


def bar_plot_compare(algorithms, names, col_idx, title, formatter, display_annotation=False):
    fig, ax = plt.subplots(figsize=(16, 15))
    bar_width = 0.25
    spacing = 0.3
    n = len(algorithms[0])

    for i, (alg, name) in enumerate(zip(algorithms, names)):
        # Horizontal Bar Plot
        x = i * spacing + np.arange(len(alg))
        ax.barh(x, alg.iloc[:, col_idx].apply(formatter), bar_width,
                label=f'{name}')

    x = bar_width + np.arange(n)
    plt.yticks(x, algorithms[0]['start_stop'] + ' -> ' + (algorithms[0]['goal_stop']))

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=5)
    ax.yaxis.set_tick_params(pad=10)

    # Add x, y gridlines
    ax.grid(color='grey',
            linestyle='-.', linewidth=0.5,
            alpha=0.2)

    # Show top values
    ax.invert_yaxis()

    # Add annotation to bars
    if display_annotation:
        for j, i in enumerate(ax.patches):
            plt.text(i.get_width() + 0.5, i.get_y() + bar_width,
                     algorithms[j // n].iloc[j % n, col_idx],
                     fontsize=10, fontweight='bold',
                     color='grey')

    # Add Plot Title
    ax.set_title(title)

    plt.legend()
    # Show Plot
    plt.show()
