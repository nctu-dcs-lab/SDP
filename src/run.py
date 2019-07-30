import os
import pandas as pd
import numpy as np
from joblib import Parallel, delayed
from scipy.io import arff
from sklearn.metrics import roc_auc_score
import tqdm

import setting
import dataset
import feature
from common import *


def compare_models(ds, f, filter, pBar):
    result = [os.path.splitext(f)[0]]
    fpath = os.path.join(*setting.ARFF_BASE_PATH, ds, f)
    data = arff.loadarff(fpath)
    df = pd.DataFrame(data[0])
    x = df[df.columns[:-1]]
    label = df[df.columns[-1:]]
    y = pd.DataFrame([int(l == b'Y') for l in label.iloc[:,0]], dtype='int')

    x = feature.drop_useless_feature(x, f)
    x = filter(x, y)
    # May contain all zero column when using KPCA and NMF
    useless_feature = np.where(x.nunique().values == 1)[0].tolist()
    x = x.drop(x.columns[useless_feature], axis=1)

    for M in setting.MODELS:
        pred = M(x)
        if pred is not None:
            pred = pred.T.values.tolist()[0]
            invert = list(map(lambda x: 1 if x == 0 else 0, pred))
            try:
                result.extend([roc_auc_score(pred, y), roc_auc_score(invert, y)])
            except Exception as e:
                result.extend([None, None])
                warning("AUC evaluation error in {} with {}".format(os.path.splitext(f)[0], M.__name__))
        else:
            result.extend([None, None])
    pBar.update(1)
    return result

def to_csv(result, ds, filter_used, prefix=None):
    df = pd.DataFrame(result)
    files = df.iloc[:,0].values.tolist()

    df = pd.DataFrame(df.iloc[:, 1:].values, index=files)
    name = '{}_{}.csv'.format(ds, filter_used)
    if prefix:
        name = '{}_{}'.format(prefix, name)
    df.to_csv(os.path.join(*setting.REPORT_PATH, name))

def run():
    dataset.generate_dataset()
    for fs in feature.feature_selection_method:
        for ds in setting.DATASET:
            path = os.path.join(*setting.ARFF_BASE_PATH, ds)
            number_thread = setting.PARALLEL_NUMBER_THREAD.get(ds, -1)
            for (dirpath, dirnames, filenames) in os.walk(path):
                fnames = filter_arff(filenames)
                bar = tqdm.tqdm(total=len(fnames), desc="{} with {}".format(ds, fs.__name__), ascii=True)
                result = Parallel(
                    n_jobs=number_thread,
                    backend=setting.PARALLEL_BACKEND)(
                        delayed(compare_models)(ds, f, fs, bar) for f in fnames
                    )
                to_csv(result, ds, fs.__name__, setting.OUTPUT_PREFIX)
                bar.close()

if __name__ == "__main__":
    run()
