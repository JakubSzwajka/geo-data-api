import requests

from app.main.config import IP_STACK_KEY

class Ipstack_service:
    root_url = 'http://api.ipstack.com/'

    def single_query(ip):
        response = requests.get(f"{Ipstack_service.root_url}{ip}?access_key={IP_STACK_KEY}")
        return response.json()
