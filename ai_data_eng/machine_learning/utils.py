import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support

def randomly_mask(df, fraction):
   mask = np.random.random(df.shape) < fraction
   df = pd.DataFrame(df)
   df[mask] = np.nan
   return df


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


def has_better_metrics(X, y, alg1, alg2, metric):
    m1 = np.array(metric(y, alg1.predict(X)))
    m2 = np.array(metric(y, alg2.predict(X)))
    arr = np.ones_like(m1)
    arr[m1 == m2] = 0
    arr[m1 < m2] = -1
    return arr