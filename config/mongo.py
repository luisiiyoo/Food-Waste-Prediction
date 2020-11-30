MONGO_USER = 'luisiiyoo'
MONGO_PASSWORD = 'Hola1234'
MONGO_DB_NAME = 'FoodWastePrediction'


class MongoCollections:
    MENUS_LUNCH = 'menus_lunch'
    MENUS_BREAKFAST = 'menus_breakfast'
    REGISTERS_LUNCH = 'registers_lunch'
    REGISTERS_BREAKFAST = 'registers_breakfast'
    DATASET_BREAKFAST = 'dataset_breakfast'
    DATASET_LUNCH = 'dataset_lunch'
    MAINTAINERS = 'maintainers'


MONGO_STR_CONNECTION = f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.1vcd2.mongodb.net/{MONGO_DB_NAME}' \
                       f'?retryWrites=true&w=majority'
