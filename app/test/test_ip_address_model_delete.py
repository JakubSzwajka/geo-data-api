
from app.test.base import BaseTestCase
from app.main.utils import get_ip_of_url
import json

from app.test.utils import * 



class Ip_address_delete_test_case(BaseTestCase):
    def test_delete_ip_address_obj(self):
        tested_with_ip = "123.123.123.113"
        with self.client:
            response_add = add_new_obj_by_ip(self, tested_with_ip)
            response_del = delete_obj(self, tested_with_ip)
            self.assertEqual(response_del.status_code, 200)

    def test_delete_multiple_addresses_from_db(self):
        tested_with_ips = ["123.123.123.113", "123.123.123.103"]
        with self.client:
            response_add = add_multiple_objs(self, tested_with_ips)
            response_del = delete_multiple_obj(self, tested_with_ips)
            response_data = json.loads(response_del.data.decode())
            self.assertEqual(response_del.status_code, 200)

            response_ips = [resp['ip'] for resp in response_data['deleted']]
            for ip in tested_with_ips:
                self.assertIn(ip, response_ips)

    def test_delete_ip_address_which_is_not_in_db(self):
        tested_with_ip = "123.123.123.113"
        with self.client:
            response_del = delete_obj(self, tested_with_ip)
            response_data = json.loads(response_del.data.decode())
            self.assertIn('there is no ip : 123.123.123.113', response_data['message'])
            self.assertEqual(response_del.status_code, 404)

    def test_delete_ip_addresses_which_one_is_not_in_db(self):
        tested_with_ips = ["123.123.123.113", "123.123.123.103"]
        with self.client:
            response_add = add_new_obj_by_ip(self, tested_with_ips[0])
            response_del = delete_multiple_obj(self, tested_with_ips)
            response_data = json.loads(response_del.data.decode())

            self.assertEqual(response_del.status_code, 200)

            response_ips = [resp['ip'] for resp in response_data['deleted']]
            self.assertIn(tested_with_ips[0], response_ips)
            self.assertIn('there is no ip : 123.123.123.103', response_ips)
            