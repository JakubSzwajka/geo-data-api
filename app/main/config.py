import os

SECRET_KEY = 'my_secret_key'
IP_STACK_KEY = os.getenv('IPSTACK_KEY') or '25ec023778973eab89dd449ea092898a'

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../../db/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
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
