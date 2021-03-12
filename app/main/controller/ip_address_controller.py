
from flask.globals import request
from flask_restful import Resource, marshal_with, abort, reqparse
from ..model.ip_address import Ip_address, single_ip_model 
from ..service.ip_address_service import * 


class Ip_address_controller(Resource):
    @marshal_with(single_ip_model)
    def get(self):
        args = request.json 
        ip_obj = get_ip_address(args)
        if not ip_obj: 
            abort(404, message=f"There is not obj with given ip: {args['ip']}")
        return ip_obj

    @marshal_with(single_ip_model)
    def patch(self):
        args = request.json
        updated_obj = update_ip_address(data= args)
        if not updated_obj:
            abort(404, message=f"There is not obj with given ip: {args['ip']}")
            
        return updated_obj

    @marshal_with(single_ip_model)
    def put(self):
        args = request.json 
        
        new_ip_obj = create_new_ip_address(data=args)
        if not new_ip_obj:
            abort(409, message=f"Ip_address with ip {args['ip']} already exist.")
      
        return new_ip_obj, 201

    def delete(self,ip_address): 

        result = delete_ip_address(ip_address)
        if result == 1: 
            abort(404, message=f"There is not obj with given ip: {ip_address}")

        return {"message":f"{ip_address} deleted"}, 204
