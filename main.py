from __future__ import absolute_import
from re import T
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, marshal
from flask_sqlalchemy import SQLAlchemy

from test_db import DATABASE_TMP

import os
import json

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.db'
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
    
# do it only for the first go 
# db.create_all()

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

class Ip_address(Resource):
    
    @marshal_with(single_ip_model)
    def get(self,ip_address):
        result = IP_Model.query.filter_by(ip=ip_address).first()
        if not result: 
            abort(404, message=f"There is not obj with given ip: {ip_address}")
        return result

    @marshal_with(single_ip_model)
    def put(self, ip_address):

        # check if there is already a obj with given id 
        result = IP_Model.query.filter_by(ip=ip_address).first()
        if result:
            abort(409, message=f"Ip_address with ip {ip_address} already exist.")
        
        args = ip_address_put_args.parse_args()
        ip_obj = IP_Model(
            ip = args['ip'],
            type = args['type'],
            continent_code = args['continent_code']
        )
        db.session.add(ip_obj)
        db.session.commit()
        
        return ip_obj, 201

    @marshal_with(single_ip_model)
    def patch(self, ip_address):
        arg = ip_address_put_args.parse_args()
        result_obj = IP_Model.query.filter_by(id=ip_address).first()
        if not result_obj:
            abort(404, message=f"There is not obj with given ip: {ip_address}")
        
        for key, value in arg.items():
            setattr(result_obj, key, value)

        db.session.add(result_obj)
        db.session.commit()

        return result_obj

    def delete(self,ip_address): 
        to_delete = IP_Model.query.filter_by(ip=ip_address).all()
        if len(to_delete) == 0: 
            abort(404, message=f"There is not obj with given ip: {ip_address}")

        for obj in to_delete:
            db.session.delete(obj)
        db.session.commit()
        return {"message":f"{ip_address} deleted"}, 204


api.add_resource(Ip_address, "/ip/<string:ip_address>")

@app.route('/all')
def get_all_ip_obj():
    objs = IP_Model.query.all()
    ord_dict_list = [marshal(obj, single_ip_model) for obj in objs]
    return {"result": [dict(ord_dict) for ord_dict in ord_dict_list ]}

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port = int(os.environ.get('PORT',5000))) 

