import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_restful import Api

from app.main import create_app, db
from app.main.controller.ip_address_controller import Ip_address_controller 

app = create_app(os.getenv('CONFIG_TYPE') or 'dev')
app.app_context().push()

api = Api(app)
api.add_resource(Ip_address_controller, "/ip")

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@app.route('/')
def hello():
    return 'hello'

@manager.command
def run():
    app.run()

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()