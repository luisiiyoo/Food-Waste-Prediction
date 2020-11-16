MONGO_USER = 'luisiiyoo'
MONGO_PASSWORD = 'Hola1234'
MONGO_DB_NAME = 'FoodWastePrediction'


class MongoCollections:
    MENUS = 'Menus'
    REGISTERS = 'Registers'
    MAINTAINERS = 'Maintainers'


MONGO_STR_CONNECTION = f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.1vcd2.mongodb.net/{MONGO_DB_NAME}' \
                       f'?retryWrites=true&w=majority'
