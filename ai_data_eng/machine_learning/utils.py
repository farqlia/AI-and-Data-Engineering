import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support


def class_accuracy(y_true, y_pred, labels):
    matrix = confusion_matrix(y_true, y_pred, labels=labels)
    return matrix.diagonal() / matrix.sum(axis=1)


def results_df(X, y, labels, algorithms, names):
    results = []
    metrics = ['precision', 'recall', 'fscore', 'accuracy']

    for alg in algorithms:
        y_pred = alg.predict(X)
        values = np.array(precision_recall_fscore_support(y_pred, y, labels=labels))
        values[-1] = class_accuracy(y_pred, y, labels)
        results.append(np.array(values))  # without support

    df = pd.DataFrame(np.concatenate(results), columns=labels)
    df['metrics'] = np.tile(np.array(metrics), len(algorithms))
    df['algorithms'] = np.array(names).repeat(4)
    return df


def long_form_results(X, y, labels, algorithms, names):
    res = results_df(X, y, labels, algorithms, names)
    melted = pd.melt(res, value_vars=labels, id_vars=['metrics', 'algorithms'])
    melted = melted.rename({'variable': 'label'}, axis=1)
    return melted