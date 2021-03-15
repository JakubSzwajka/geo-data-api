from app.test.base import BaseTestCase
from app.main.utils import get_ip_of_url
import json

from app.test.utils import * 

class Ip_address_objs_adding_test_case(BaseTestCase):
    def test_add_new_ip_address_obj_with_ip_as_string(self):
        tested_with_ip = "123.123.123.123"
        with self.client:
            response = add_new_obj_by_ip(self, tested_with_ip)
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response_data["ip"], tested_with_ip)

    def test_add_new_ip_address_obj_with_ip_as_invalid_string(self):
        tested_with_ip = "89.151a.32.123"
        with self.client:
            response = add_new_obj_by_ip(self, tested_with_ip)
            response_data = json.loads(response.data.decode())  
            self.assertEqual(response.status_code, 400)
            self.assertTrue(message_contains(tested_with_ip,dict(response_data)["message"] ))

    def test_add_multiple_ip_addresses_with_valid_strings(self):
        testing_ips = ["123.123.123.113", "123.123.123.111", "555.123.123.113"]        
        with self.client:
            response_add = add_multiple_objs(self, testing_ips)
            response_data = json.loads(response_add.data.decode())
            response_ips = [ resp_obj["ip"] for resp_obj in response_data["response"]]

            for test_ip in testing_ips:
                self.assertIn(test_ip, response_ips)


    def test_add_multiple_ip_addresses_with_one_invalid_string(self):
        testing_ips = ["123.123.123.113", "123.123.a123.111", "555.123.123.113"]
        
        with self.client:
            response_add = add_multiple_objs(self, testing_ips)
            response_data = json.loads(response_add.data.decode())
            response_ips = [ resp_obj["ip"] for resp_obj in response_data["response"]]

            # assertion for good responses 
            for test_ip in ["123.123.123.113", "555.123.123.113"]:
                self.assertIn(test_ip, response_ips)

            # assertion for bad  
            self.assertIn('Wrong ip provided: 123.123.a123.111', response_ips)


    def test_add_multiple_ip_addresses_with_one_already_in_db(self):
        testing_ips = ["123.123.123.113", "555.123.123.113"]

        with self.client:
            response_add_first = add_new_obj_by_ip(self, testing_ips[0])
            
            response_add_with_duplicated = add_multiple_objs(self, testing_ips)
            response_data = json.loads(response_add_with_duplicated.data.decode())
            response_ips = [ resp_obj["ip"] for resp_obj in response_data["response"]]
            print(response_data)
            self.assertIn("555.123.123.113", response_ips)
            self.assertIn("Object with ip:123.123.123.113 already exists", response_ips)

