import os
import unittest
from flask import request, make_response, jsonify
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_restful import Api
import jwt
import datetime 

from app.main.config import SECRET_KEY
from app.main import create_app, db
from app.main.controller.ip_address_controller import Ip_address_controller 
from app.main.utils import return_all_objs, token_required

app = create_app(os.getenv('CONFIG_TYPE') or 'dev')
app.app_context().push()

api = Api(app)
api.add_resource(Ip_address_controller, "/ip_data")

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@app.route('/')
def hello():
    return 'Visit repo page for more info: https://github.com/JakubSzwajka/geo_data_rest_api' 

@app.route('/all')
@token_required
def return_all_obj():
    return return_all_objs()

@app.route('/login')
def login():
    credentials = request.get_json()

    if not credentials and request.authorization:
        auth = request.authorization
        credentials = {
            "user": auth.username,
            "password":auth.password
        }
    
    if credentials and credentials["user"] == 'admin' and credentials['password'] == 'admin':
        token = jwt.encode({
            "user": "admin",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            }, key= str(SECRET_KEY) )
        
        return jsonify({'token': token})

    else: 
        return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required'})


@manager.command
def run():
    app.run(host='0.0.0.0', port = int(os.environ.get("PORT", 5000)))

@manager.command
def test():
    tests = unittest.TestLoader().discover('app/test', pattern='test_ip*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()