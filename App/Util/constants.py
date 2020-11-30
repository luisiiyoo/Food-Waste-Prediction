NUM_DAYS_SERVICE = 5
NO_SERVICE_TAGS = ['labor day', 'no service', 'holiday', 'wfh']
BREAKFAST = 'breakfast'
LUNCH = 'lunch'
CATERINGS = [BREAKFAST, LUNCH]
DATE_FORMAT = "%Y-%m-%d"  # "%m/%d/%Y"

DIETS = ["regular", "light", "vegan", "vegetarian"]
EXTRA_TAG = ' + Extras'

COLOR_BREAKFAST = 'green'
COLOR_LUNCH = 'blue'


class MenuFields:
    DATE = 'date'
    DAY = 'day'
    IS_SERVICE_DAY = 'is_service_day'
    REGULAR = 'regular'
    LIGHT = 'light'
    VEGAN = 'vegan'
    VEGETARIAN = 'vegetarian'


class RegisterFields:
    DATE = 'date'
    PERSON = 'person'
    DIET = 'diet'
    ATTEND = 'attend'
    REQUEST = 'request'
    EXTRA = 'extra'


class DataGroupedFields:
    DATE = 'date'
    DAY = 'day'
    DIET = 'diet'
    TOTAL_PEOPLE = 'total_people'
    TOTAL_REQUESTS = 'total_requests'
    REQUEST = 'request'
    ATTEND = 'attend'


BOW_MAX_FEATURES = 50
BOW_FILE_PATH = './App/Server/Preprocessor/BagOfWords/models/'
