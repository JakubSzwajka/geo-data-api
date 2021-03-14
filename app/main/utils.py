import socket
from app.main.model.ip_address import Ip_address, single_ip_model
from flask_restful import marshal
import re

def get_ip_of_url(url):
    return socket.gethostbyname(url)

def get_url_from_ip(ip):
    return socket.gethostbyaddr(ip)

def return_all_objs():
    objs = Ip_address.query.all()
    ord_dict_list = [marshal(obj, single_ip_model) for obj in objs]
    return {"result": [dict(ord_dict) for ord_dict in ord_dict_list ]}

def ip_ver4_validator(ip):
    pattern =  re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    if  type(ip) == str and pattern.match(ip):
        return True
    else: 
        return False

def ip_ver6_validator(ip):
    if type(ip) != str: return False 
    
    try:
        socket.inet_pton(socket.AF_INET6, ip)
    except socket.error:  # not a valid address
        return False
    return True