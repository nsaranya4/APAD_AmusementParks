class BaseConfig(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    BACKEND_URL = 'http://127.0.0.1:8080'


class ProductionConfig(BaseConfig):
    DEBUG = False
    BACKEND_URL = '<BACKEND_URL>'
