#!/usr/bin/env python

import sys
from optparse import OptionParser

import numpy as np
from sklearn import cross_validation
from sklearn import svm

def _read_mfcc_df(csvpath):
    return pd.read_csv(csvpath,
                       header=None,
                       sep=',',
                       names=['mfcc%d' % x for x in range(13)] + ['class'])

def xfold(df, k=10):
    X = df[['mfcc%d' % x for x in range(13)]]
    y = df['class']

    clf = svm.SVC(kernel='linear', C=1)
    scores = cross_validation.cross_val_score(clf, X, y, cv=k)
    return scores

def main():
    """main function for standalone usage"""
    usage = "usage: %prog [options] mfcc.csv"
    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        return 2

    # do stuff
    print(xfold(_read_mfcc_df(args[0])))

if __name__ == '__main__':
    sys.exit(main())
