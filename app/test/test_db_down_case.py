from app.test.base import TestCase_db_down
from app.test.utils import * 
from app.main.utils import * 

class Ip_address_get_db_down_test_case(TestCase_db_down):
    
    def test_get_single_ip_with_db_down(self):
        tested_with_ip = "123.123.123.123"
        with self.client:
            response = get_obj_by_ip(self, tested_with_ip)
            response_data = json.loads(response.data.decode())  
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_data["ip"], tested_with_ip)

    def test_get_multiple_ips_with_db_down(self):
        testing_ips = ["114.204.250.125", "134.201.250.155", "110.204.250.125"]
        with self.client:
            response = get_multiple_objs_by_ips(self, testing_ips)
            response_data = json.loads(response.data.decode())  
            self.assertEqual(response.status_code, 200)
        
            response_ips = [resp_obj['ip'] for resp_obj in response_data['response']]
            
            for ip in testing_ips:
                self.assertIn(ip, response_ips)


class Ip_address_update_db_down_test_case(TestCase_db_down):
    def test_update_ip_address_obj(self):
        tested_with_ip = "123.123.123.113"
        with self.client:
            response_update = update_obj(self, tested_with_ip, type='ipv4', continent_code='US')
            response_data = json.loads(response_update.data.decode())  
            self.assertEqual(response_update.status_code, 503)
            self.assertEqual(response_data["message"], "Database system is not available")


class Ip_address_add_test_case_db_down(TestCase_db_down):
    def test_add_new_ip_address_obj_with_ip_as_string(self):
        tested_with_ip = "123.123.123.123"
        with self.client:
            response = add_new_obj_by_ip(self, tested_with_ip)
            response_data = json.loads(response.data.decode())  
            self.assertEqual(response.status_code, 503)
            self.assertEqual(response_data["message"], "Database system is not available")
    
    def test_add_multiple_ip_addresses_with_valid_strings(self):
        testing_ips = ["123.123.123.113", "123.123.123.111", "555.123.123.113"]        
        with self.client:
            response_add = add_multiple_objs(self, testing_ips)
            response_data = json.loads(response_add.data.decode())
            self.assertEqual(response_add.status_code, 503)
            self.assertEqual(response_data["message"], "Database system is not available")
    
    