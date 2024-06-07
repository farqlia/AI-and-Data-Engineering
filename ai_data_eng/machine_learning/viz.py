import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, precision_score, recall_score, \
    precision_recall_fscore_support, confusion_matrix, ConfusionMatrixDisplay

fontdict = {'family' : 'Calibri',
    'weight' : 'bold',
    'size' : 22}

def visualize_classification_metrics(y_true, y_pred, labels, name=None, ax=None):
    metrics = ['precision', 'recall', 'fscore', 'support']
    values = np.array(precision_recall_fscore_support(y_true, y_pred, labels=labels))

    values[-1, :] = values[-1, :] / np.sum(values[-1, :])

    if ax is None:
        _, ax = plt.subplots(figsize=(5, 5))
    ax.pcolormesh(values,
                  cmap='GnBu')

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(labels)) + 0.5, labels=labels)
    ax.set_yticks(np.arange(len(metrics)) + 0.5, labels=metrics)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(metrics)):
        for j in range(len(labels)):
            ax.text(j + 0.5, i + 0.5, np.round(values[i, j], 2),
                    ha="center", va="center", color="w",
                    fontdict=fontdict)

    ax.set_title(f"Classification metrics {' - ' + name if name else ''}")


def visualize_confusion_matrix(y_true, y_pred, labels, name=None):
    values = confusion_matrix(y_true, y_pred, labels=labels)

    disp = ConfusionMatrixDisplay(values, display_labels=labels)
    disp.plot()

    plt.title(f"Confusion Matrix {' - ' + name if name else ''}")
    plt.tight_layout()
    plt.show()


def visualize_compare_algorithms(X, y, algorithms, names):
    results = [precision_recall_fscore_support(y, alg.predict(X), average='micro') for alg in algorithms]
    values = np.array([res[:3] for res in results])
    accuracy = [accuracy_score(y, alg.predict(X)) for alg in algorithms]

    metrics = ['precision', 'recall', 'fscore', 'accuracy']

    values = np.c_[values, np.array(accuracy)]

    fig, ax = plt.subplots()
    ax.pcolormesh(values, cmap='GnBu')

    # Show all ticks and label them with the respective list entries
    ax.set_yticks(np.arange(len(names)) + 0.5, labels=names)
    ax.set_xticks(np.arange(len(metrics)) + 0.5, labels=metrics)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(names)):
        for j in range(len(metrics)):
            ax.text(j + 0.5, i + 0.5, np.round(values[i, j], 2),
                    ha="center", va="center", color="w",
                    fontdict=fontdict)

    ax.set_title(f"Algoritms Comparison")
    fig.tight_layout()
    plt.show()


def visualize_compare_algorithms(X, y, algorithms, names):
    results = []
    for alg in algorithms:
        y_pred = alg.predict(X)
        values = [precision_score(y, y_pred, average='macro'),
                  recall_score(y, y_pred, average='macro'),
                  f1_score(y, y_pred, average='macro'),
                  accuracy_score(y, y_pred)]
        results.append(values)

    results = np.array(results)

    metrics = ['precision', 'recall', 'fscore', 'accuracy']

    fig, ax = plt.subplots()
    ax.pcolormesh(results, cmap='cool')

    # Show all ticks and label them with the respective list entries
    ax.set_yticks(np.arange(len(names)) + 0.5, labels=names)
    ax.set_xticks(np.arange(len(metrics)) + 0.5, labels=metrics)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(names)):
        for j in range(len(metrics)):
            ax.text(j + 0.5, i + 0.5, np.round(results[i, j], 2),
                    ha="center", va="center", color="w", fontdict={'family': 'Calibri',
                                                                   'weight': 'bold',
                                                                   'size': 22})

    ax.set_title(f"Algoritms Comparison")
    fig.tight_layout()
    plt.show()

    return values