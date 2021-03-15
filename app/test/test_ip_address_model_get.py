from app.test.base import BaseTestCase
from app.main.utils import get_ip_of_url
import json

from app.test.utils import * 

class Ip_address_getting_test_case(BaseTestCase):
    def test_get_data_by_url_adress(self):
        tested_with_url = "www.google.com" 
        ip_of_tested_url = get_ip_of_url(tested_with_url)
        with self.client:
            response_add = add_new_obj_by_ip(self, ip_of_tested_url)
            response_get = get_obj_by_url(self, tested_with_url)
            response_data = json.loads(response_get.data.decode())  
            self.assertEqual(response_get.status_code, 200)
            self.assertEqual(response_data["ip"], ip_of_tested_url)

    def test_get_data_by_url_adress_from_empty_db(self):
        tested_with_url = "www.google.com" 
        ip_of_tested_url = get_ip_of_url(tested_with_url)
        with self.client:
            response_get = get_obj_by_url(self, tested_with_url)
            response_data = json.loads(response_get.data.decode())  
            self.assertEqual(response_get.status_code, 404)

    def test_get_ip_address_obj_from_db(self):
        tested_with_ip = "123.123.123.113"
        with self.client:
            response_add = add_new_obj_by_ip(self, tested_with_ip)
            response_get = get_obj_by_ip(self, tested_with_ip)
            response_data = json.loads(response_get.data.decode())  
            self.assertEqual(response_get.status_code, 200)
            self.assertEqual(response_data["ip"], tested_with_ip)

    def test_get_ip_address_obj_from_empty_db(self):
        tested_with_ip = "123.123.123.113"
        with self.client:
            response_get = get_obj_by_ip(self, tested_with_ip)
            response_data = json.loads(response_get.data.decode())  
            self.assertEqual(response_get.status_code, 404)

    def test_get_multiple_ip_address_obj(self):
        testing_ips = ["123.123.123.113", "123.123.123.111", "555.123.123.113"]
        
        with self.client:
            response_add = add_multiple_objs(self, testing_ips)
            response_get = get_multiple_objs_by_ips(self, testing_ips)
            response_data = json.loads(response_get.data.decode())
            
            response_ips_list = [ obj["ip"] for obj in response_data["response"]]

            self.assertNotEqual(response_ips_list, [])
            for ip in response_ips_list:
                self.assertIn(ip, testing_ips)    
    
    def test_get_multiple_ip_address_obj_by_urls(self):
        testing_urls = ["www.google.com", "www.facebook.com"]
        testing_ips = [ get_ip_of_url(url) for url in testing_urls]

        with self.client:
            response_add = add_multiple_objs(self, testing_ips)
            response_get = get_multiple_objs_by_urls(self, testing_urls)
            response_data = json.loads(response_get.data.decode())
            
            response_ips_list = [ obj["ip"] for obj in response_data["response"]]
            self.assertNotEqual(response_ips_list, [])

            for ip in response_ips_list:
                self.assertIn(ip, testing_ips)    

    
    def test_get_multiple_ip_address_obj_by_urls_lack_of_one(self):
        testing_urls = ["www.google.com", "www.google.pl", "www.youtube.com"]
        testing_ips = [ get_ip_of_url(url) for url in testing_urls]

        with self.client:
            response_add = add_multiple_objs(self, testing_ips[:2])
            response_get = get_multiple_objs_by_urls(self, testing_urls)
            response_data = json.loads(response_get.data.decode())
            
            response_ips_list = [ obj["ip"] for obj in response_data["response"]]
            self.assertNotEqual(response_ips_list, [])

            for ip in response_ips_list[:2]:
                self.assertIn(ip, testing_ips[:2])    
            self.assertIn(testing_ips[2],response_ips_list[2])

    def test_get_multiple_ip_address_obj_with_lack_of_one(self):
        testing_ips = ["123.123.123.113", "123.123.123.111", "555.123.123.113"]
        
        with self.client:
            response_add = add_multiple_objs(self, testing_ips[0:1])
            response_get = get_multiple_objs_by_ips(self, testing_ips)
            response_data = json.loads(response_get.data.decode())
            
            response_ips_list = [ obj["ip"] for obj in response_data["response"]]

            for ip in testing_ips[0:1]:
                self.assertIn(ip, response_ips_list)    
            self.assertIn('there is no ip : 555.123.123.113', response_ips_list)


    def test_get_multiple_ip_address_obj_by_url_and_ips(self):
        testing_ips = ["123.123.123.113", "123.123.123.111", "555.123.123.113"]
        testing_urls = ["www.google.com", "www.google.pl", "www.youtube.com"]
        testing_ips_from_urls = [ get_ip_of_url(url) for url in testing_urls]
        
        with self.client:
            response_add = add_multiple_objs(self, testing_ips + testing_ips_from_urls)
            response_get = get_multiple_by_ip_and_url(self, testing_ips, testing_urls)
            response_data = json.loads(response_get.data.decode())
            response_ips_list = [ obj["ip"] for obj in response_data["response"]]

            for ip in testing_ips + testing_ips_from_urls:
                self.assertIn(ip, response_ips_list)    
            