from re import search
from warnings import resetwarnings
from app.main import db
from app.main.model import ip_address
from app.main.model.ip_address import Ip_address, single_ip_model
from app.main.utils import get_ip_of_url, ip_ver4_validator, ip_ver6_validator
from flask_restful import marshal

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

    result_obj = Ip_address.query.filter_by(ip=data["ip"]).first()
    if result_obj:
        raise DataError(data,'ip', f"Object with ip:{data['ip']} already exists", 409)

    ip_obj = Ip_address(
        ip = data['ip'],
        type = data['type'],
        continent_code = data['continent_code']
    )    

    save_changes(ip_obj)
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

def update_ip_address(data):
    result_obj = Ip_address.query.filter_by(ip=data['ip']).first()
    if not result_obj:
        return 

    for key, value in data.items():
        setattr(result_obj, key, value)

    save_changes(result_obj)
    return result_obj

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

    
def get_ip_address(args):
    if 'ip' in args.keys() and type(args['ip']) != list:    
        return get_ip_by_ip(args['ip'])

    elif 'ip' in args.keys() and type(args['ip']) == list:
        found_objs = []
        for query_ip in args['ip']:
            try:
                found_objs.append(get_ip_by_ip(query_ip))
            except NotFoundError as error:
                found_objs.append(Ip_address(ip = str(error)))
        return found_objs
        
    elif 'url' in args.keys() and type(args['url']) != list:
        return get_ip_by_url(args['url'])

    elif 'url' in args.keys() and type(args['url'] == list):
        found_objs = []
        for query_url in args['url']:
            try:
                found_objs.append(get_ip_by_url(query_url))
            except NotFoundError as error:
                found_objs.append(Ip_address(ip = str(error)))
        return found_objs
        
def delete_ip_address(ip):
    obj = get_ip_address(ip)
    if not obj: 
        return 1 
    else:
        db.session.delete(obj)
    db.session.commit()
    return 0

def get_all_ip_addresses(data): 
    objs = Ip_address.query.all()
    ord_dict_list = [marshal(obj, single_ip_model) for obj in objs]
    return {"result": [dict(ord_dict) for ord_dict in ord_dict_list ]}

def save_changes(data):
    db.session.add(data)
    db.session.commit()
    