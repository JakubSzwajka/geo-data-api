from re import search
from warnings import resetwarnings

import sqlalchemy
from app.main import db
from app.main.model import ip_address
from app.main.model.ip_address import Ip_address, single_ip_model
from app.main.utils import get_ip_of_url, ip_ver4_validator, ip_ver6_validator
from flask_restful import marshal

from app.main.service.ip_stack_service import Ipstack_service

class IPStack_error(Exception):
    def __init__(self, data):
        self.data = data
    def __str__(self):
        return str(self.data['info'])

class Database_error(Exception):
    def __init__(self, message):
        self.message = message
        self.error_code = 503
    def __str__(self):
        return self.message

class DataError(Exception):
    def __init__(self, error_data, error_element, message, error_code = 400 ):
        self.error_data = error_data
        self.error_element = error_element
        self.error_code = error_code
        self.error_element_value = error_data[error_element]
        self.message = message
    
    def __str__(self):
        return str(self.message)

class NotFoundError(Exception):
    def __init__(self, search_for_key, search_for_value, error_code = 404):
        self.search_for_key = search_for_key 
        self.search_for_value = search_for_value
        self.error_code = error_code
        
    def __str__(self):
        return f"there is no {self.search_for_key} : {self.search_for_value}"
    
def parse_dict_to_ip_obj_constructor(dict):

    if "success" in dict.keys() and dict["success"] == False: 
        raise IPStack_error( dict['error'] )

    return Ip_address(
        ip = dict["ip"],
        type = dict["type"],
        continent_code = dict["continent_code"],
        continent_name = dict["continent_name"],
        country_code = dict["country_code"],
        country_name = dict["country_name"],
        region_code = dict["region_code"],
        region_name = dict["region_name"],
        city = dict["city"],
        zip = dict["zip"],
        latitude = dict["latitude"],
        longitude = dict["longitude"]
    )

def validate_data(data):
    if data["type"] == 'ipv4': 
        ip_valid = ip_ver4_validator(data["ip"])
    else:
        ip_valid = ip_ver6_validator(data["ip"]) 

    if not ip_valid:
        return 400 #wrong data
    else:
        return 200

def wrong_data_provided(status, data, message = "wrong data provided"):
    response = {
        "status_code" : status,
        "message" : message,
        "data": data        
    }
    return response

def create_new_ip_address(data):
    
    data_status = validate_data(data)
    if data_status != 200: 
        raise DataError(data,'ip', f"Wrong ip provided: {data['ip']}",  data_status)

    try:
        result_obj = get_ip_by_ip(data['ip'])
        raise DataError(data,'ip', f"Object with ip:{data['ip']} already exists", 409)
    
    except NotFoundError as error:
        ip_obj = Ip_address(
            ip = data['ip'],
        )    
        for key, value in data.items():
            setattr(ip_obj, key, value)

        save_changes(ip_obj)

    except sqlalchemy.exc.OperationalError as error:
        raise Database_error("Database system is not available")
    
    return ip_obj 

def create_new_ip_addresses(data):
    new_obj_list = []

    for obj in data["data"]:
        try:
            new_address_obj = create_new_ip_address(obj)
            new_obj_list.append(new_address_obj)
        except DataError as error:
            ip_obj = Ip_address(
                ip = str(error),
                )
            new_obj_list.append(ip_obj)

    return new_obj_list

def get_ip_by_ip(ip):

    obj = Ip_address.query.filter_by(ip=ip).first()
    if not obj: 
        raise NotFoundError( search_for_key='ip', search_for_value=ip)
    
    return obj 

def get_ip_by_url(url):
    ip = get_ip_of_url(url)
    obj = Ip_address.query.filter_by(ip=ip).first()
    if not obj: 
        raise NotFoundError( search_for_key='ip', search_for_value=ip)
    return obj 

def update_ip_address(data):

    if 'data' in data.keys():
        result_list = []
        for ip_obj in data['data']:
            try:
                result_list.append(update_ip_address(ip_obj))
            except NotFoundError as error:
                result_list.append(Ip_address(ip = str(error)))

        return result_list
    else: 
        try:
            result_obj = get_ip_by_ip(data['ip'])
        except sqlalchemy.exc.OperationalError as error:
            raise Database_error("Database system is not available")

        for key, value in data.items():
            setattr(result_obj, key, value)
        db.session.commit()

        try:
            result_obj = get_ip_by_ip(data['ip'])
        except sqlalchemy.exc.OperationalError as error:
            raise Database_error("Database system is not available")

    return result_obj

    
def get_ip_address(args):
    
    total_objs_found = []
    
    if 'ip' in args.keys() and type(args['ip']) != list:    
        try:
            total_objs_found.append(get_ip_by_ip(args['ip']))
        except sqlalchemy.exc.OperationalError as error:
            # database is down
            return parse_dict_to_ip_obj_constructor(Ipstack_service.single_query(args['ip']))

    elif 'ip' in args.keys() and type(args['ip']) == list:

        for query_ip in args['ip']:
            try:
                total_objs_found.append(get_ip_by_ip(query_ip))
            except NotFoundError as error:
                total_objs_found.append(Ip_address(ip = str(error)))
            except sqlalchemy.exc.OperationalError as error:
                total_objs_found.append(parse_dict_to_ip_obj_constructor(Ipstack_service.single_query(query_ip)))
    
        
    if 'url' in args.keys() and type(args['url']) != list:
        try:
            total_objs_found.append((get_ip_by_url(args['url'])))
        except sqlalchemy.exc.OperationalError as error:
            return parse_dict_to_ip_obj_constructor(Ipstack_service.single_query(args['url']))

    elif 'url' in args.keys() and type(args['url'] == list):

        for query_url in args['url']:
            try:
                total_objs_found.append(get_ip_by_url(query_url))
            except NotFoundError as error:
                total_objs_found.append(Ip_address(ip = str(error)))
            except sqlalchemy.exc.OperationalError as error:
                total_objs_found.append(parse_dict_to_ip_obj_constructor(Ipstack_service.single_query(query_url)))
    
    if len(total_objs_found) == 1:
        return total_objs_found[0]
    return total_objs_found
        

def delete_ip_address(data):
    try:
        deleted_ips = []
        
        if type(data['ip']) == list: 
        
            for ip in data['ip']:
                try:
                    obj = get_ip_by_ip(ip)
                    db.session.delete(obj)
                    deleted_ips.append(obj)
        
                except NotFoundError as error:
                    deleted_ips.append(Ip_address(ip = str(error)))

        else: 
            obj = get_ip_by_ip(data['ip'])
            db.session.delete(obj)
            deleted_ips.append(obj)

        db.session.commit()

    except sqlalchemy.exc.OperationalError as error:
        raise Database_error("Database system is not available")
        
    except NotFoundError as error:
        raise error

    return deleted_ips
    

def get_all_ip_addresses(data): 
    objs = Ip_address.query.all()
    ord_dict_list = [marshal(obj, single_ip_model) for obj in objs]
    return {"result": [dict(ord_dict) for ord_dict in ord_dict_list ]}

def save_changes(data):
    db.session.add(data)
    db.session.commit()
    