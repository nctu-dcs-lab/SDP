from models import *


# Generic setting
ORIGIN_BASE_PATH = ['..', 'origin_data']
ARFF_BASE_PATH = ['..', 'data']
REPORT_PATH = ['..', 'report']
OUTPUT_PREFIX = None

DATASET = ['PROMISE']
MODELS = [*m]

ARFF_TYPE_MAP = {'int64': 'NUMERIC', 'float64': 'NUMERIC', 'object': 'STRING'}

# Parallel setting
PARALLEL_BACKEND = 'threading'
## -1 use all thread
PARALLEL_NUMBER_THREAD = {
    'AEEEM': -1,
    'NASA': 1,
    'PROMISE': -1
}

# For AEEEM
AEEEM_PROJECT = ['eclipse', 'equinox', 'lucene', 'mylyn', 'pde']
AEEEM_FILE = ['bug-metrics.csv', 'change-metrics.csv', 'complexity-code-change.csv', 'single-version-ck-oo.csv']
## 5 type: ['churn.csv', 'exp-churn.csv', 'lin-churn.csv', 'log-churn.csv', 'weighted-churn.csv']
AEEEM_CHURN_FILE = ['lin-churn.csv']
## 5 type: ['ent.csv', 'exp-ent.csv', 'lin-ent.csv', 'log-ent.csv', 'weighted-ent.csv']
AEEEM_ENTROPY_FILE = ['weighted-ent.csv']

# For NASA
NASA_SUBPATH = ['figshare', 'D\'\'']
NASA_METRIC = [
    'BRANCH_COUNT',
    'LOC_CODE_AND_COMMENT',
    'LOC_COMMENTS',
    'CYCLOMATIC_COMPLEXITY',
    'DESIGN_COMPLEXITY',
    'ESSENTIAL_COMPLEXITY',
    'LOC_EXECUTABLE',
    'HALSTEAD_CONTENT',
    'HALSTEAD_DIFFICULTY',
    'HALSTEAD_EFFORT',
    'HALSTEAD_ERROR_EST',
    'HALSTEAD_LENGTH',
    'HALSTEAD_LEVEL',
    'HALSTEAD_PROG_TIME',
    'HALSTEAD_VOLUME',
    'NUM_OPERANDS',
    'NUM_OPERATORS',
    'NUM_UNIQUE_OPERANDS',
    'NUM_UNIQUE_OPERATORS',
    'LOC_TOTAL'
]
# For PROMISE
PROMISE_SUBPATH = ['zenodo']
PROMISE_METRIC = [
    'wmc',
    'dit',
    'noc',
    'cbo',
    'rfc',
    'lcom',
    'ca',
    'npm',
    'lcom3',
    'loc',
    'dam',
    'moa',
    'mfa',
    'cam',
    'ic',
    'cbm',
    'amc',
    'max_cc',
    'avg_cc',
    'bug'
]
