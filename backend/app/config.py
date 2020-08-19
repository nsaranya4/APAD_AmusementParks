class BaseConfig(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    MONGODB_HOST = 'mongodb://127.0.0.1/funtech'


class ProductionConfig(BaseConfig):
    DEBUG = False
    MONGODB_HOST = '<MONGODB_URL>'
