class BaseConfig(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    MONGODB_DB = 'funtech'
    MONGODB_HOST = '127.0.0.1'


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = True