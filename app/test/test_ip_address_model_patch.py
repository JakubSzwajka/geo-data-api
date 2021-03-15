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
