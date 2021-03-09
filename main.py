from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort 

from test_db import DATABASE_TMP

import os

app = Flask(__name__)
api = Api(app)

ip_address_put_args = reqparse.RequestParser()
ip_address_put_args.add_argument("region_name", type=str, help="Send me the region_name!")
ip_address_put_args.add_argument("country", type=str, help="Send me the country!")

ip_database = {}

def abort_if_ip_not_in_db(ip_data_id):
    if ip_data_id not in ip_database:
        abort(404, message=f"Given ip with id:{ip_data_id} is not stored in db.")

def abort_if_ip_exists(ip_data_id):
    if ip_data_id in ip_database:
        abort(409, message=f"Given ip with id:{ip_data_id} already exists... ")

class Ip_address(Resource):
    
    def get(self,ip_data_id):
        abort_if_ip_not_in_db(ip_data_id)
        return ip_database[ip_data_id]

    def put(self, ip_data_id):
        abort_if_ip_exists(ip_data_id)
        args = ip_address_put_args.parse_args()
        ip_database[ip_data_id] = args   
        return {ip_data_id: args}

    def delete(self,ip_data_id): 
        abort_if_ip_not_in_db(ip_data_id)
        del ip_database[ip_data_id]
        return {"message":f"{ip_data_id} deleted"}, 204

api.add_resource(Ip_address, "/ip/<string:ip_data_id>")

if __name__ == "__main__":

    # for testing online 
    for i in range(len(DATABASE_TMP)):
        ip_database[str(i)] = DATABASE_TMP[i]
    
    app.run(debug=True,host='0.0.0.0') 

