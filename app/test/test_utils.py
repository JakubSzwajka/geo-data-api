import unittest
from app.main.utils import * 
from app.test.base import BaseTestCase

class utils_test_case(BaseTestCase):
    
    def test_ip_ver4_valid_string(self):
        self.assertTrue(ip_ver4_validator('89.151.32.233'))
        
    def test_ip_ver4_invalid_string(self):
        self.assertFalse(ip_ver4_validator('89.151.32.1233'))
    
    def test_ip_ver4_number(self):
        self.assertFalse(ip_ver4_validator(12343))
    
    def test_ip_ver6_valid_string(self):
        self.assertTrue(ip_ver6_validator("2607:f8b0:4004:805::2004"))

    def test_ip_ver6_invalid_string(self):
        self.assertFalse(ip_ver6_validator("260712:f8b0:04004:805::2004"))

    def test_ip_ver6_number(self):
        self.assertFalse(ip_ver6_validator(2607120040048052004))