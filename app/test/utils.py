import json

def get_token(self):
    token_resp =  self.client.get(
        '/login',
        data=json.dumps(dict(
            user = "admin",
            password = "admin"
        )),
        content_type='application/json',
    )
    
    token_data = json.loads(token_resp.data.decode())  
    return token_data["token"]

def add_new_obj_by_ip(self, ip, type = 'ipv4', continent_code = 'EU'):
    return self.client.put(
        f'/ip_data?token={get_token(self)}',
        data=json.dumps(dict(
            ip = ip,
            type = type,
            continent_code = continent_code
        )),
        content_type='application/json'
    )

def add_multiple_objs(self, list_ips ):
    return self.client.put(
        f'/ip_data?token={get_token(self)}',
        data=json.dumps(dict(
            data = [ dict( ip = ip, type = 'ipv4', continent_code = 'EU' ) for ip in list_ips ]
        )),
        content_type='application/json'
    )

def get_obj_by_ip(self, ip ):
    return self.client.get(
        f'/ip_data?token={get_token(self)}',
        data=json.dumps(dict(
           ip = ip 
        )),
        content_type='application/json'
    )

def get_multiple_objs_by_ips(self, ips):
    return self.client.get(
        f'/ip_data?token={get_token(self)}',
        data=json.dumps(dict(
            ip = ips
        )),
        content_type='application/json'
    )

def get_multiple_objs_by_urls(self, urls):
    return self.client.get(
        f'/ip_data?token={get_token(self)}',
        data=json.dumps(dict(
            url = urls
        )),
        content_type='application/json'
    )

def get_obj_by_url(self, url ):
    return self.client.get(
        f'/ip_data?token={get_token(self)}',
        data=json.dumps(dict(
           url = url
        )),
        content_type='application/json'
    )

def update_obj(self, ip, type, continent_code):
    return self.client.patch(
        f'/ip_data?token={get_token(self)}',
        data=json.dumps(dict(
            ip = ip,
            type = type,
            continent_code = continent_code 
        )),
        content_type='application/json'
    )

def message_contains( phrase, message ):
    return phrase in message


def delete_obj(self, ip):
    return self.client.delete(
        f'/ip_data?token={get_token(self)}',
        data=json.dumps(dict(
            ip = ip,
        )),
        content_type='application/json'
    )