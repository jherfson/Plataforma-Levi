import os.path


basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig():
    DEBUG = False
    TESTING = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class TestingConfig(BaseConfig):
    TESTING = True

class ProductionConfig(BaseConfig):
    pass
