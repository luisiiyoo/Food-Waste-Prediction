from App.Util.constants import DatasetFields

TARGET_COLUMN = DatasetFields.ATTEND
EXCLUDE_COLS = [DatasetFields.DATE]

TEST_SIZE_PROPORTION = 1 / 5
RANDOM_STATE = 1
SCORING = 'r2'
NUM_FOLDS = 10
NUM_REPEATS = 10
PREDICT_SAMPLES = True

MODELS = ['GradientBoostingRegressor']
MAX_CARDINALITY = 10
ESTIMATORS = [100]
SVR_KERNEL = ['rbf']
POLY_DEGREE = [2]
MAX_DEPTH = [1]
