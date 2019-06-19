import igraph
from scipy.io import arff
from scipy.stats import zscore
import pandas as pd
import glob
from random import choice
from copy import deepcopy
from sklearn.metrics import confusion_matrix, roc_auc_score
import numpy as np
from networkx.algorithms import community
from networkx.convert_matrix import from_numpy_array
import rpy2.robjects as robjects
from warnings import warn


def get_defective_cluster(feature, group):
    g1 = pd.DataFrame(group)
    g2 = pd.DataFrame(list(map(lambda x: 1 if x == 0 else 0, group)))
    rs = pd.DataFrame(feature.sum(axis=1)).T
    sum_of_g1 = rs.dot(g1).at[0, 0] / g1.sum()[0]
    sum_of_g2 = rs.dot(g2).at[0, 0] / g2.sum()[0]

    if sum_of_g1 > sum_of_g2:
        return g1
    else:
        return g2

def Newman_with_corrcoef(data):
    norm = (data-data.mean())/data.std()
    matrix = np.corrcoef(norm)
    matrix = matrix - np.diag(np.diag(matrix))

    matrix[matrix > 0 ] = 1
    matrix[matrix < 0 ] = 0

    graph = igraph.Graph.Adjacency(matrix.tolist(), mode=igraph.ADJ_UNDIRECTED)
    try:
        cluster = graph.community_leading_eigenvector(clusters = 2)
    except Exception as e:
        warn(e)
        return None
    if len(cluster) != 2:
        return None

    group = [None for _ in range(len(matrix))]
    for i in cluster[0]:
        group[i] = 0
    for i in cluster[1]:
        group[i] = 1

    return get_defective_cluster(data, group)

def Newman_with_dot(data):
    norm = (data-data.mean())/data.std()
    matrix = norm.dot(norm.T)
    matrix = matrix - np.diag(np.diag(matrix))

    matrix[matrix > 0 ] = 1
    matrix[matrix < 0 ] = 0

    graph = igraph.Graph.Adjacency(matrix.values.tolist(), mode=igraph.ADJ_UNDIRECTED)
    try:
        cluster = graph.community_leading_eigenvector(clusters = 2)
    except Exception as e:
        warn(e)
        return None
    if len(cluster) != 2:
        return None

    group = [None for _ in range(len(matrix))]
    for i in cluster[0]:
        group[i] = 0
    for i in cluster[1]:
        group[i] = 1

    return get_defective_cluster(data, group)

def Asyn_fluidc_with_corrcoef(data):
    norm = (data-data.mean())/data.std()
    matrix = np.corrcoef(norm)
    matrix = matrix - np.diag(np.diag(matrix))

    matrix[matrix > 0 ] = 1
    matrix[matrix < 0 ] = 0

    graph = from_numpy_array(matrix)
    try:
        cluster = list(community.asyn_fluidc(graph, 2, max_iter=1000))
    except Exception as e:
        warn(e)
        return None

    if len(cluster) != 2:
        return None

    group = [None for _ in range(len(matrix))]
    for i in cluster[0]:
        group[i] = 0
    for i in cluster[1]:
        group[i] = 1

    return get_defective_cluster(data, group)

def Asyn_fluidc_with_dot(data):
    norm = (data-data.mean())/data.std()
    matrix = norm.dot(norm.T)
    matrix = matrix - np.diag(np.diag(matrix))

    matrix[matrix > 0 ] = 1
    matrix[matrix < 0 ] = 0

    graph = from_numpy_array(matrix.values)
    try:
        cluster = list(community.asyn_fluidc(graph, 2, max_iter=1000))
    except Exception as e:
        warn(e)
        return None
    if len(cluster) != 2:
        return None

    group = [None for _ in range(len(matrix))]
    for i in cluster[0]:
        group[i] = 0
    for i in cluster[1]:
        group[i] = 1

    return get_defective_cluster(data, group)

def Modularity_with_corrcoef(data):
    norm = (data-data.mean())/data.std()
    matrix = np.corrcoef(norm)
    matrix = matrix - np.diag(np.diag(matrix))

    matrix[matrix > 0 ] = 1
    matrix[matrix < 0 ] = 0

    graph = from_numpy_array(matrix)
    try:
        cluster = list(community.greedy_modularity_communities(graph))
    except Exception as e:
        warn(e)
        return None

    if len(cluster) != 2:
        return None

    group = [None for _ in range(len(matrix))]
    for i in cluster[0]:
        group[i] = 0
    for i in cluster[1]:
        group[i] = 1

    return get_defective_cluster(data, group)

def Modularity_with_dot(data):
    norm = (data-data.mean())/data.std()
    matrix = norm.dot(norm.T)
    matrix = matrix - np.diag(np.diag(matrix))

    matrix[matrix > 0 ] = 1
    matrix[matrix < 0 ] = 0

    graph = from_numpy_array(matrix.values)
    try:
        cluster = list(community.greedy_modularity_communities(graph))
    except Exception as e:
        warn(e)
        return None

    if len(cluster) != 2:
        return None

    group = [None for _ in range(len(matrix))]
    for i in cluster[0]:
        group[i] = 0
    for i in cluster[1]:
        group[i] = 1

    return get_defective_cluster(data, group)

r_source = robjects.r['source']("../R/sc.R")

def sc_cc(data):
    nr, nc = data.shape
    xvec = robjects.FloatVector(data.values.transpose().reshape(data.size))
    xr = robjects.r.matrix(xvec, nrow=nr, ncol=nc)
    try:
        res = robjects.globalenv['sc2'](xr)
    except Exception as e:
        warn(e)
        return None
    if res:
        return pd.DataFrame(np.array(res))
    else:
        return None

def sc_origin(data):
    nr, nc = data.shape
    xvec = robjects.FloatVector(data.values.transpose().reshape(data.size))
    xr = robjects.r.matrix(xvec, nrow=nr, ncol=nc)
    try:
        res = robjects.globalenv['sc1'](xr)
    except Exception as e:
        warn(e)
        return None
    if res:
        return pd.DataFrame(np.array(res))
    else:
        return None


m = [
    Newman_with_dot,
    Asyn_fluidc_with_dot,
    Modularity_with_dot,
    sc_origin
]

m_cc = [
    Newman_with_corrcoef,
    Asyn_fluidc_with_corrcoef,
    Modularity_with_corrcoef,
    sc_cc
]

if __name__ == "__main__":
    for f in glob.iglob("../data/NASA/KC1.arff"):
        minlist = []
        print('Running with: ', f)
        data = arff.loadarff(f)
        df = pd.DataFrame(data[0])
        feature = df[df.columns[:-1]]
        label = df[df.columns[-1:]]
        y = pd.DataFrame([int(l == b'Y') for l in label.iloc[:,0]], dtype='int')

        pred = Newman_with_corrcoef(feature)
        pred = pred.T.values.tolist()[0]
        print(roc_auc_score(pred, y))
