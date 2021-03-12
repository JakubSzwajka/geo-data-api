import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../../db/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'postgres://bvahrjumxffaet:fb698577cefb50b44f549bfb6ec3106736ae71219d2c3f69aeae7b8e361caf05@ec2-54-155-87-214.eu-west-1.compute.amazonaws.com:5432/d38t2r3sfa67np'
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
