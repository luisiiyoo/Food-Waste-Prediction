from App.Util.constants import DatasetFields

TARGET_COLUMN = DatasetFields.ATTEND
EXCLUDE_COLS = [DatasetFields.DATE]

TEST_SIZE_PROPORTION = 1 / 5
RANDOM_STATE = 2

MODELS = ['GradientBoostingRegressor']
MAX_CARDINALITY = 10
ESTIMATORS = [100]
SVR_KERNEL = ['rbf']
POLY_DEGREE = [2]
MAX_DEPTH = [1]
