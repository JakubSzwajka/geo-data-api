from manage import test
from app.test.base import BaseTestCase
import unittest
import json

def add_new_obj(self, ip, type = 'ipv4', continent_code = 'EU'):
    return self.client.put(
        '/ip',
        data=json.dumps(dict(
            ip = ip,
            type = type,
            continent_code = continent_code
        )),
        content_type='application/json'
    )

def get_obj_by_ip(self, ip ):
    return self.client.get(
        '/ip',
        data=json.dumps(dict(
           ip = ip 
        )),
        content_type='application/json'
    )

def update_obj(self, ip, type, continent_code):
    return self.client.patch(
        '/ip',
        data=json.dumps(dict(
            ip = ip,
            type = type,
            continent_code = continent_code 
        )),
        content_type='application/json'
    )

class Ip_address_test_case(BaseTestCase):

    def test_add_new_obj(self):
        tested_with_ip = "123.123.123.123"
        with self.client:
            response = add_new_obj(self, tested_with_ip)
            response_data = json.loads(response.data.decode())  
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response_data["ip"], tested_with_ip)

    
    def test_get_obj_from_db(self):
        tested_with_ip = "123.123.123.113"
        with self.client:
            response_add = add_new_obj(self, tested_with_ip)
            response_get = get_obj_by_ip(self, tested_with_ip)
            response_data = json.loads(response_get.data.decode())  
            self.assertEqual(response_get.status_code, 200)
            self.assertEqual(response_data["ip"], tested_with_ip)

    def test_update_obj(self):
        tested_with_ip = "123.123.123.113"
        with self.client:
            response_add = add_new_obj(self, tested_with_ip)
            response_update = update_obj(self, tested_with_ip, type='ipv4', continent_code='US')
            response_data = json.loads(response_update.data.decode())  
            self.assertEqual(response_update.status_code, 200)
            self.assertEqual(response_data["ip"], tested_with_ip)
            self.assertEqual(response_data["continent_code"], 'US')
