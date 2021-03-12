import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.main.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///../../db/database.db'
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.main.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)

class TestTesingConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app 

    def test_app_is_testing(self):
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue(app.config['TESTING'] is True)


if __name__ == '__main__':
    unittest.main()