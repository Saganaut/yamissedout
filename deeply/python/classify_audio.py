#!/usr/bin/env python

import sys
from optparse import OptionParser

import pandas as pd
import numpy as np
from sklearn import cross_validation
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import normalize
from sklearn.metrics import confusion_matrix
from sklearn.feature_selection import SelectKBest, f_classif

models = {'svm':  SVC(kernel='linear', C=1),
          'sgd':  SGDClassifier(loss="hinge", penalty="l2"),
          'rf':   RandomForestClassifier(),
          'dt':   DecisionTreeClassifier(),
          'lr':   LogisticRegression(class_weight='balanced'),
}

def _feature_names(n):
    return ['f%d' % x for x in range(n)]

def _read_mfcc_df(csvpath):
    with open(csvpath) as f:
        numfeatures = len(f.readline().strip().split(',')) - 1
        return pd.read_csv(csvpath,
                           header=None,
                           sep=',',
                           names=_feature_names(numfeatures) + ['class'])

def xfold(X, y, classifier, k=10):
    normalize(X, copy=False)

    clf = models[classifier]
    scores = cross_validation.cross_val_score(clf, X, y, cv=k)
    return scores

def _confusion_matrix(X, y, classifier):
    normalize(X, copy=False)
    labels = list(np.unique(y))

    clf = models[classifier]
    clf.fit(X, y)
    pred_y = clf.predict(X)

    return confusion_matrix(y, pred_y, labels=labels), labels

def main():
    """main function for standalone usage"""
    usage = "usage: %prog [options] mfcc.csv"
    parser = OptionParser(usage=usage)
    parser.add_option('-m', '--model', default='svm',
                      help='Model to use. One of: %s' % ', '.join(models.keys()))
    parser.add_option('-k', default=10, type='int',
                      help='Number of CV folds [default: %default]')
    parser.add_option('-f', '--feature-selection', default=0, type='int')

    (options, args) = parser.parse_args()

    if len(args) != 1 or options.model not in models:
        parser.print_help()
        return 2

    # do stuff
    df = _read_mfcc_df(args[0])
    X, y = df[_feature_names(len(df.columns) - 1)], df['class']

    if options.feature_selection > 0:
        X = SelectKBest(f_classif, k=options.feature_selection).fit_transform(X, y)

    scores = xfold(X, y, options.model, k=options.k)
    print(scores)
    print('average accuracy: %f' % (sum(scores) / float(len(scores))))
    cmatrix, labels = _confusion_matrix(X, y, options.model)
    print('%s%s' % (' ' * 15, ' '.join(labels)))
    for label, row in zip(labels, cmatrix):
        print('%15s %s' % (label, str(row)))

if __name__ == '__main__':
    sys.exit(main())
