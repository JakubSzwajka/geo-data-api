from .. import db
from flask_restful import fields

import json


single_ip_model = {
    # 'id': fields.Integer,
    'ip': fields.String,
    'type':fields.String,
    'continent_code': fields.String,
    'continent_name': fields.String,
    'country_code': fields.String,
    'country_name': fields.String,
    'region_code': fields.String,
    'region_name': fields.String,
    'city': fields.String,
    'zip': fields.String,
    'latitude' : fields.Float, 
    'longitude' : fields.Float,
}

class Ip_address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(45), nullable=False) #45 brecause of ipv4 mapped to ipv6

    # some other fields
    type = db.Column(db.String(4), nullable=False) #ipv4 / ipv6
    continent_code = db.Column(db.String(4), nullable=True)
    continent_name = db.Column(db.String(30))
    country_code = db.Column(db.String(5))
    country_name = db.Column(db.String(30))
    region_code = db.Column(db.String(30))
    region_name = db.Column(db.String(30))
    city = db.Column(db.String(30))
    zip = db.Column(db.String(5))
    latitude = db.Column(db.Float) # 14 digits precision needed 
    longitude = db.Column(db.Float) # 14 digits precision needed

    def toJson(self):
        return json.dumps(self, default= lambda o: o.__dict__, sort_keys=True, indent=4)

    def __repr__(self):
        return f"ID: {self.id}, ip: {self.ip} - {self.type} - {self.continent_code}"
    