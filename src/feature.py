import numpy as np
from common import *


def drop_useless_feature(x, f):
    # dropping features that has same value among all entities
    origin = set(x.columns)
    useless_feature = np.where(x.nunique().values == 1)[0].tolist()
    x = x.drop(x.columns[useless_feature], axis=1)
    diff = list(origin - set(x.columns))
    if diff:
        warning("{} informationless features dropping in {}: {}\n\t Please make sure this is expected".format(len(diff), f, ', '.join(diff)))
    return x

def get_feature_cc(feature, y):
    return np.array([np.corrcoef(feature.iloc[:,i], y.T)[0][1] for i in range(len(feature.columns))])

def all_feature(x, y):
    return x

def abs_cc_above_mean_cc(x, y):
    cc = get_feature_cc(x, y)
    return x.iloc[:,np.where(np.absolute(cc) > np.mean(cc))[0]]

def abs_cc_above_median_cc(x, y):
    cc = get_feature_cc(x, y)
    return x.iloc[:,np.where(np.absolute(cc) > np.median(cc))[0]]

feature_selection_method = [
    all_feature,
    abs_cc_above_mean_cc,
    abs_cc_above_median_cc
]
