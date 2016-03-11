#!/usr/bin/env python

import sys
from optparse import OptionParser

import pandas as pd
import numpy as np
from sklearn import cross_validation
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import normalize

models = {'svm': svm.SVC(kernel='linear', C=1),
          'sgd': SGDClassifier(loss="hinge", penalty="l2"),
          'rf':  RandomForestClassifier(),
}


def _read_mfcc_df(csvpath):
    return pd.read_csv(csvpath,
                       header=None,
                       sep=',',
                       names=['mfcc%d' % x for x in range(13)] + ['class'])

def xfold(df, classifier, k=10):
    X = df[['mfcc%d' % x for x in range(13)]]
    normalize(X, copy=False)
    y = df['class']

    clf = models[classifier]
    scores = cross_validation.cross_val_score(clf, X, y, cv=k)
    return scores

def main():
    """main function for standalone usage"""
    usage = "usage: %prog [options] mfcc.csv"
    parser = OptionParser(usage=usage)
    parser.add_option('-m', '--model', default='svm',
                      help='Model to use. One of: %s' % ', '.join(models.keys()))

    (options, args) = parser.parse_args()

    if len(args) != 1 or options.model not in models:
        parser.print_help()
        return 2

    # do stuff
    print(xfold(_read_mfcc_df(args[0]), options.model))

if __name__ == '__main__':
    sys.exit(main())
