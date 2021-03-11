from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, marshal
from flask_sqlalchemy import SQLAlchemy

import json

DATABASE_PATH = 'db/database.db'


def create_app():
    
    app = Flask(__name__)
    api = Api(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
    
    db = SQLAlchemy(app)
        
    single_ip_model = {
        'id': fields.Integer,
        'ip': fields.String,
        'type':fields.String,
        'continent_code': fields.String,
        # 'continent_name': fields.String,
        # 'country_code': fields.String,
        # 'country_name': fields.String,
        # 'region_code': fields.String,
        # 'region_name': fields.String,
        # 'city': fields.String,
        # 'zip': fields.String,
        # 'latitude' : fields.Float, 
        # 'longitude' : fields.Float,
    }

    class IP_Model(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        ip = db.Column(db.String(45), nullable=False) #45 brecause of ipv4 mapped to ipv6

        # some other fields
        type = db.Column(db.String(4), nullable=False) #ipv4 / ipv6
        continent_code = db.Column(db.String(4), nullable=True)
        # continent_name = db.Column(db.String(30))
        # country_code = db.Column(db.String(5))
        # country_name = db.Column(db.String(30))
        # region_code = db.Column(db.String(30))
        # region_name = db.Column(db.String(30))
        # city = db.Column(db.String(30))
        # zip = db.Column(db.String(5))
        # latitude = db.Column(db.Float) # 14 digits precision needed 
        # longitude = db.Column(db.Float) # 14 digits precision needed

        def toJson(self):
            return json.dumps(self, default= lambda o: o.__dict__, sort_keys=True, indent=4)

        def __repr__(self):
            return f"ID: {self.id}, ip: {self.ip} - {self.type} - {self.continent_code}"

    ip_address_put_args = reqparse.RequestParser()
    ip_address_put_args.add_argument("ip", type=str, help="Ip address needed", required=True)
    ip_address_put_args.add_argument("type", type=str, help="Ip type needed", required=True)
    ip_address_put_args.add_argument("continent_code", type=str, help="Continent code needed")
    # ip_address_put_args.add_argument("region_name", type=str, help="Send me the region_name!")
    # ip_address_put_args.add_argument("country", type=str, help="Send me the country!")

    ip_address_update_args = reqparse.RequestParser()
    ip_address_update_args.add_argument("ip", type=str, help="Ip address needed")
    ip_address_update_args.add_argument("type", type=str, help="Ip type needed")
    ip_address_update_args.add_argument("continent_code", type=str, help="Continent code needed")


    return app