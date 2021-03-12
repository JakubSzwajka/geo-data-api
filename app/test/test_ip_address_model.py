from werkzeug.wrappers import Response
from manage import test
from app.test.base import BaseTestCase
from app.main.utils import get_ip_of_url
import unittest
import json

def add_new_obj_by_ip(self, ip, type = 'ipv4', continent_code = 'EU'):
    return self.client.put(
        '/ip_data',
        data=json.dumps(dict(
            ip = ip,
            type = type,
            continent_code = continent_code
        )),
        content_type='application/json'
    )

def add_multiple_objs(self, list_ips ):
    return self.client.put(
        '/ip_data',
        data=json.dumps(dict(
            data = [ dict( ip = ip, type = 'ipv4', continent_code = 'EU' ) for ip in list_ips ]
        )),
        content_type='application/json'
    )
    

def get_obj_by_ip(self, ip ):
    return self.client.get(
        '/ip_data',
        data=json.dumps(dict(
           ip = ip 
        )),
        content_type='application/json'
    )

def get_obj_by_url(self, url ):
    return self.client.get(
        '/ip_data',
        data=json.dumps(dict(
           url = url
        )),
        content_type='application/json'
    )

def update_obj(self, ip, type, continent_code):
    return self.client.patch(
        '/ip_data',
        data=json.dumps(dict(
            ip = ip,
            type = type,
            continent_code = continent_code 
        )),
        content_type='application/json'
    )

class Ip_address_test_case(BaseTestCase):
    def test_add_new_ip_address_obj_with_ip(self):
        tested_with_ip = "123.123.123.123"
        with self.client:
            response = add_new_obj_by_ip(self, tested_with_ip)
            response_data = json.loads(response.data.decode())  
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response_data["ip"], tested_with_ip)
    
    def test_get_data_by_url_adress(self):
        tested_with_url = "www.google.com" 
        ip_of_tested_url = get_ip_of_url(tested_with_url)
        with self.client:
            response_add = add_new_obj_by_ip(self, ip_of_tested_url)
            response_get = get_obj_by_url(self, tested_with_url)
            response_data = json.loads(response_get.data.decode())  
            self.assertEqual(response_get.status_code, 200)
            self.assertEqual(response_data["ip"], ip_of_tested_url)

    def test_get_ip_address_obj_from_db(self):
        tested_with_ip = "123.123.123.113"
        with self.client:
            response_add = add_new_obj_by_ip(self, tested_with_ip)
            response_get = get_obj_by_ip(self, tested_with_ip)
            response_data = json.loads(response_get.data.decode())  
            self.assertEqual(response_get.status_code, 200)
            self.assertEqual(response_data["ip"], tested_with_ip)

    def test_add_multiple_ip_addresses(self):
        testing_ips = ["123.123.123.113", "123.123.123.111", "555.123.123.113", "www.google.com"]

        with self.client:
            response_add = add_multiple_objs(self, testing_ips)
            response_data = json.loads(response_add.data.decode())
            response_ips = []

            for resp_obj in response_data:
                response_ips.append(resp_obj["ip"])

            for test_ip in testing_ips:
                self.assertIn(test_ip, response_ips)
                
    def test_update_ip_address_obj(self):
        tested_with_ip = "123.123.123.113"
        with self.client:
            response_add = add_new_obj_by_ip(self, tested_with_ip)
            response_update = update_obj(self, tested_with_ip, type='ipv4', continent_code='US')
            response_data = json.loads(response_update.data.decode())  
            self.assertEqual(response_update.status_code, 200)
            self.assertEqual(response_data["ip"], tested_with_ip)
            self.assertEqual(response_data["continent_code"], 'US')