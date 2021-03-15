import json
from flask import make_response, Response
from flask.globals import request
from flask_restful import Resource, marshal_with, abort, reqparse, marshal
from flask_testing.utils import ContextVariableDoesNotExist
from ..model.ip_address import Ip_address, single_ip_model 
from ..service.ip_address_service import * 
from app.main.utils import token_required
import collections

class Ip_address_controller(Resource):
    @token_required
    def get(self):
        args = request.json 

        try:
            ip_obj = get_ip_address(args)
            
            if type(ip_obj) == list: 
                response_obj_list = { "response" : [ marshal(obj, single_ip_model) for obj in ip_obj] } 
                return response_obj_list, 200
            else:
                return marshal(ip_obj, single_ip_model), 200
                
        except NotFoundError as error: 
            abort(error.error_code, message = str(error))

    @token_required
    def patch(self):

        try:
            args = request.json
            updated_obj = marshal(update_ip_address(data= args), single_ip_model) 

        except NotFoundError as error:
            abort(error.error_code, message = str(error))
        except Database_error as db_error:
            abort(db_error.error_code, message = str(db_error))
        
        return updated_obj, 200

    @token_required
    def put(self):
        args = request.json 
        
        # multiple objs
        if "data" in args.keys():

            try: 
                new_ip_obj = create_new_ip_addresses(data=args)
                # response_list = []
                # for i, new_obj in enumerate(new_ip_obj):
                #     dict_obj = dict(marshal(new_obj, single_ip_model))
                #     filtered = { key: value for key, value in dict_obj.items() if value is not None}
                #     response_list.append(filtered)
                    
                message = json.dumps({ "response": marshal(new_ip_obj, single_ip_model)}) 
                return Response(message, status = 201, mimetype = 'application/json')
            except Database_error as error:
                abort(error.error_code, message = str(error))
                
        # single obj
        else:
            try:
                new_ip_obj = create_new_ip_address(data=args)
                return marshal(new_ip_obj,single_ip_model) , 201
                    
            except DataError as error:
                abort( error.error_code , message=str(error))
                
            except Database_error as error:
                abort(error.error_code, message = str(error))

    @token_required                
    def delete(self): 
        args = request.json 
        try:
            result = delete_ip_address(args)
        except Database_error as error:
            abort(error.error_code, message=str(error))
            
        except NotFoundError as error:
            abort(error.error_code, message=str(error))

        return {"message":f"{ip_address} deleted"}, 204
