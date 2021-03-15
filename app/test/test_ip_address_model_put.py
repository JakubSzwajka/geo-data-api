from app.test.base import BaseTestCase
from app.main.utils import get_ip_of_url
import json

from app.test.utils import * 

class Ip_address_updateing_test_case(BaseTestCase):
    def test_update_ip_address_obj(self):
        tested_with_ip = "123.123.123.113"
        with self.client:
            response_add = add_new_obj_by_ip(self, tested_with_ip)
            response_update = update_obj(self, tested_with_ip, type='ipv4', continent_code='US')
            response_data = json.loads(response_update.data.decode())  
            self.assertEqual(response_update.status_code, 200)
            self.assertEqual(response_data["ip"], tested_with_ip)
            self.assertEqual(response_data["continent_code"], 'US')

    def test_update_ip_address_obj_not_in_db(self):
        tested_with_ip = "123.123.123.113"
        with self.client:
            response_update = update_obj(self, tested_with_ip, type='ipv4', continent_code='US')
            response_data = json.loads(response_update.data.decode())  
            self.assertEqual(response_update.status_code, 404)
            self.assertEqual('there is no ip : 123.123.123.113', response_data["message"])
    
    def test_update_multiple_ip_address_objs(self):
        testing_ips = ["123.123.123.113", "123.123.123.111", "122.123.123.113"]

        with self.client:
            response_add = add_multiple_objs(self, testing_ips)
            response_update = update_multiple_ip_obj(self, testing_ips, type='ipv4', continent_code='US')
            response_data = json.loads(response_update.data.decode())
            self.assertEqual(response_update.status_code, 200)
            
            updated_ips_and_cont_codes = [[obj['ip'], obj["continent_code"]] for obj in response_data]
            
            for ip, continent_code in updated_ips_and_cont_codes:
                self.assertIn(ip, testing_ips)
                self.assertEqual(continent_code, 'US')

            
