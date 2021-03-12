from warnings import resetwarnings
from app.main import db
from app.main.model import ip_address
from app.main.model.ip_address import Ip_address, single_ip_model
from app.main.utils import get_ip_of_url
from flask_restful import marshal

def create_new_ip_address(data):
    result_obj = Ip_address.query.filter_by(ip=data["ip"]).first()
    if result_obj:
        return 

    ip_obj = Ip_address(
        ip = data['ip'],
        type = data['type'],
        continent_code = data['continent_code']
    )    
    save_changes(ip_obj)
    return ip_obj 

def update_ip_address(data):
    result_obj = Ip_address.query.filter_by(ip=data['ip']).first()
    if not result_obj:
        return 

    for key, value in data.items():
        setattr(result_obj, key, value)

    save_changes(result_obj)
    return result_obj

def get_ip_address(args):
    if 'ip' in args.keys():
        return Ip_address.query.filter_by(ip=args['ip']).first()
    elif 'url' in args.keys():
        return Ip_address.query.filter_by(ip=get_ip_of_url(args['url'])).first()

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
    