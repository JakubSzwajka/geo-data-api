import os

SECRET_KEY = str(os.getenv('SECRET_KEY'))
IP_STACK_KEY = str(os.getenv('IP_STACK_KEY'))

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../../db/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') 

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../../db/database_test.db'
    
config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig,
    test=TestingConfig
)
