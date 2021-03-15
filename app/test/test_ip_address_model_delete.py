
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
            self.assertEqual(response_del.status_code, 204)