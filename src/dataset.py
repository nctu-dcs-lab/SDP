from scipy.io import arff as arff_
import pandas as pd
import os
import arff
import setting
import sys
from common import *


def gen_AEEEM():
    for p in setting.AEEEM_PROJECT:
        path = os.path.join(*setting.ORIGIN_BASE_PATH, "AEEEM", p)
        churn_path = os.path.join(path, 'churn')
        entropy_path = os.path.join(path, 'entropy')
        fixeds = list(map(lambda x: pd.read_csv(os.path.join(path, x), sep='\s*;\s*', engine='python'), setting.AEEEM_FILE))
        churns = list(map(lambda x: pd.read_csv(os.path.join(churn_path, x), sep='\s*;\s*', engine='python'), setting.AEEEM_CHURN_FILE))
        entropys = list(map(lambda x: pd.read_csv(os.path.join(entropy_path, x), sep='\s*;\s*', engine='python'), setting.AEEEM_ENTROPY_FILE))

        # drop empty column
        for i in fixeds:
            i.drop(i.columns[[-1,]], axis=1, inplace=True)
        for i in churns:
            i.drop(i.columns[[-1,]], axis=1, inplace=True)
        for i in entropys:
            i.drop(i.columns[[-1,]], axis=1, inplace=True)

        # common metrics among files
        join_column = [fixeds[0].columns[0], *fixeds[0].columns[-1:-6:-1]]

        # fix = pd.merge(fixeds[0], fixeds[1], how='left', left_on=join_column, right_on=join_column)
        # fix = pd.merge(fix, fixeds[2], how='left', left_on=join_column[0], right_on=join_column[0])
        # fix = pd.merge(fix, fixeds[3], how='left', left_on=join_column, right_on=join_column)
        fix = pd.merge(fixeds[0], fixeds[2], how='left', left_on=join_column[0], right_on=join_column[0])
        fix = pd.merge(fix, fixeds[3], how='left', left_on=join_column, right_on=join_column)

        for i in range(len(churns)):
            for j in range(len(entropys)):
                f = pd.merge(fix, churns[i], how='left', left_on=join_column, right_on=join_column, suffixes=('', '_churn'))
                f = pd.merge(f, entropys[j], how='left', left_on=join_column, right_on=join_column, suffixes=('', '_ent'))
                f = f.assign(Defective=lambda f:f.bugs + f.nonTrivialBugs + f.majorBugs + f.criticalBugs + f.highPriorityBugs)
                f['Defective'] = list(map(lambda x: 'Y' if x > 0 else 'N', f['Defective']))
                f = f.drop(columns=['classname', 'bugs', 'nonTrivialBugs', 'majorBugs', 'criticalBugs', 'highPriorityBugs'])

                dtype = list(map(lambda x: (x[0], setting.ARFF_TYPE_MAP[x[1].name] if x[0] != 'Defective' else ['Y', 'N']), f.dtypes.iteritems()))
                obj = {
                    'description': 'SDP data',
                    'relation': 'data',
                    'attributes': dtype,
                    'data':f.values
                }
                arff_path = os.path.join(*setting.ARFF_BASE_PATH, "AEEEM", p + '_' + setting.AEEEM_CHURN_FILE[i][:3] + '_' + setting.AEEEM_ENTROPY_FILE[j][:3] + '.arff')
                output = open(arff_path, 'w')
                arff.dump(obj, output)

def gen_NASA():
    path = os.path.join(*setting.ORIGIN_BASE_PATH, "NASA")
    if setting.NASA_SUBPATH:
        path = os.path.join(path, *setting.NASA_SUBPATH)

    for (dirpath, dirnames, filenames) in os.walk(path):
        fnames = filter_arff(filenames)
        for f in fnames:
            data = arff_.loadarff(os.path.join(dirpath, f))
            df = pd.DataFrame(data[0])
            df = pd.concat([df[setting.NASA_METRIC], df[df.columns[-1:]]], axis=1)
            df.iloc[:, -1] = df.iloc[:, -1].str.decode('utf-8')

            dtype = list(map(lambda x: (x[0], setting.ARFF_TYPE_MAP[x[1].name] if x[0] != 'Defective' and x[0] != 'label' else ['Y', 'N']), df.dtypes.iteritems()))
            obj = {
                'description': 'SDP data',
                'relation': 'data',
                'attributes': dtype,
                'data':df.values
            }
            output = open(os.path.join(*setting.ARFF_BASE_PATH, "NASA", f), 'w')
            arff.dump(obj, output)

def gen_PROMISE():
    path = os.path.join(*setting.ORIGIN_BASE_PATH, "PROMISE")
    if setting.PROMISE_SUBPATH:
        path = os.path.join(path, *setting.PROMISE_SUBPATH)

    common_metric = set(setting.PROMISE_METRIC)
    for (dirpath, dirnames, filenames) in os.walk(path):
        fnames = filter_arff(filenames)
        for f in fnames:
            df = pd.read_csv(os.path.join(dirpath, f))
            if common_metric.issubset(set(df.columns)):
                df = df[setting.PROMISE_METRIC]
                df['Defective'] = list(map(lambda x: 'Y' if x > 0 else 'N', df['bug']))
                df.drop(columns=['bug'], inplace=True)

                dtype = list(map(lambda x: (x[0], setting.ARFF_TYPE_MAP[x[1].name] if x[0] != 'Defective' else ['Y', 'N']), df.dtypes.iteritems()))
                obj = {
                    'description': 'SDP data',
                    'relation': 'data',
                    'attributes': dtype,
                    'data':df.values
                }
                arff_path = os.path.join(*setting.ARFF_BASE_PATH, "PROMISE", os.path.splitext(f)[0] + '.arff')
                output = open(os.path.join(arff_path), 'w')
                arff.dump(obj, output)

def gen_dataset_info(dataset):
    path = os.path.join(*setting.ARFF_BASE_PATH, dataset)
    stat = []
    files = []
    metrics = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        fnames = filter_arff(filenames)
        for f in fnames:
            files.append(os.path.splitext(f)[0])
            data = arff_.loadarff(os.path.join(dirpath, f))
            df = pd.DataFrame(data[0])
            count = len(df.index)
            defective = df.iloc[:,-1].value_counts().to_dict()
            stat.append([count, defective[b'Y'], round(defective[b'Y'] / count * 100, 2)])
            metrics.append([len(df.columns), *df.columns])
        df = pd.DataFrame(stat, index=files, columns=['entities', 'defective_entities', 'defect_percentage'])
        df.to_csv(os.path.join(*setting.REPORT_PATH, "{}_dataset_info.csv".format(dataset)))
        df = pd.DataFrame(metrics, index=files)
        df.to_csv(os.path.join(*setting.REPORT_PATH, "{}_metrics_info.csv".format(dataset)))

def consistency_check(dataset):
    path = os.path.join(*setting.ARFF_BASE_PATH, dataset)
    pf, n, t = None, None, None
    for (dirpath, dirnames, filenames) in os.walk(path):
        fnames = filter_arff(filenames)
        for f in fnames:
            data = arff_.loadarff(os.path.join(dirpath, f))
            df = pd.DataFrame(data[0])
            if n and t:
                if n == data[1].names() and t == data[1].types():
                    continue
                elif len(n) != len(data[1].names()):
                    raise InconsistentError("Dataset {}: {} and {} have different number of metrics".format(dataset, pf, f))
                else:
                    warning("Dataset {}: {} and {} may have inconsistent metrics due to different metrics name or type".format(dataset, pf, f))
            else:
                n = data[1].names()
                t = data[1].types()
                pf = f

def generate_dataset():
    print("Generating Dataset: {}".format(", ".join(setting.DATASET)))
    for d in setting.DATASET:
        if d == 'AEEEM':
            gen_AEEEM()
        elif d == 'NASA':
            gen_NASA()
        elif d == 'PROMISE':
            gen_PROMISE()
        consistency_check(d)
        gen_dataset_info(d)
    print("Complete")

if __name__ == "__main__":
    generate_dataset()
