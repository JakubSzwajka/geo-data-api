
# GEO IP DATA
Aim was to build REST api, which stores geological data based on IP. You can add/get/modify ora delete data from db. Api is deployed on Heroku [here](https://geo-data-rest-api.herokuapp.com/).

In case of database error, data can still be provided by ```http://api.ipstack.com/```. Just remember to set your IP_STACK_KEY env var. 

## Authorization 
Api requires JWT authorization. To obrain token use: 
```
  http://localhost:5000/login
```
User is hardcoded so far. User: *admin* , Password: *admin*

After you get a token, request url should look like: 
```
  http://localhost:5000/ip_data?token={your_token_here}
```

## Requests

### GET method 
To obtain data you can use Ip or url address. Url will be converted to ip address by ```socket.gethostbyname()``` method. 
Request json for single ip or url is: 
```json 
{
  "ip": "134.201.250.155"
}

{
  "url": "www.google.com"
}
```
and for multiple addresses: 
```json 
{
  "ip": ["134.201.250.155", "74.125.193.147"]
}

{
  "url": ["www.google.com", "www.facebook.com"]
}
```
Response obj structure for single and multiple address query: 
```json
{
    "ip":"114.201.250.155",
    "type":"ipv4",
    "continent_code":"AS",
    "continent_name":"Asia",
    "country_code":"KR",
    "country_name":"South Korea",
    "region_code":"11",
    "region_name":"Seoul",
    "city":"Seoul",
    "zip":"1-011",
    "latitude":37.56100082397461,
    "longitude":126.98265075683594
}

{
  "data": [
    {
      "city": "Los Angeles", 
      "continent_code": "NA", 
      "continent_name": "North America", 
      "country_code": "US", 
      "country_name": "United States", 
      "id": 2, 
      "ip": "134.201.250.155", 
      "latitude": 34.0655517578125, 
      "longitude": -118.24053955078125, 
      "region_code": "CA", 
      "region_name": "California", 
      "type": "ipv4", 
      "zip": "90012"
    }, 
    {
      "city": "Herndon", 
      "continent_code": "NA", 
      "continent_name": "North America", 
      "country_code": "US", 
      "country_name": "United States", 
      "id": 3, 
      "ip": "2607:f8b0:4004:809::2004", 
      "latitude": 38.98371887207031, 
      "longitude": -77.38275909423828, 
      "region_code": "VA", 
      "region_name": "Virginia", 
      "type": "ipv6", 
      "zip": "22095"
    }
  ]
}
```

### POST method
To add data use **POST** request. You can send two types of Json data. First is for posting single object and the second is for multiple. Success response will be the same structure. 
```json
{
    "ip":"114.201.250.155",
    "type":"ipv4",
    "continent_code":"AS",
    "continent_name":"Asia",
    "country_code":"KR",
    "country_name":"South Korea",
    "region_code":"11",
    "region_name":"Seoul",
    "city":"Seoul",
    "zip":"1-011",
    "latitude":37.56100082397461,
    "longitude":126.98265075683594
}

{
  "data": [
    {
      "city": "Los Angeles", 
      "continent_code": "NA", 
      "continent_name": "North America", 
      "country_code": "US", 
      "country_name": "United States", 
      "id": 2, 
      "ip": "134.201.250.155", 
      "latitude": 34.0655517578125, 
      "longitude": -118.24053955078125, 
      "region_code": "CA", 
      "region_name": "California", 
      "type": "ipv4", 
      "zip": "90012"
    }, 
    {
      "city": "Herndon", 
      "continent_code": "NA", 
      "continent_name": "North America", 
      "country_code": "US", 
      "country_name": "United States", 
      "id": 3, 
      "ip": "2607:f8b0:4004:809::2004", 
      "latitude": 38.98371887207031, 
      "longitude": -77.38275909423828, 
      "region_code": "VA", 
      "region_name": "Virginia", 
      "type": "ipv6", 
      "zip": "22095"
    }
  ]
}
```
### PUT method
To update ip data use put requests. The structure is the same as **POST** method but with corrected data. 

### DELETE method 
To delete ip data objs from database use DELETE method. The structure is the same as **GET** method but only for ip numbers.

### List all in db 
You can use ```http://localhost:5000/all?token={your_token}``` to list all data in db

# Run local 
After cloning the repo:
```
  pip install -r requirements.txt
  python manage.py run 
```
or if you want to use docker:
```
  docker build -t {your_tag} .
  docker run -p 5000:5000 {your_tag}
```
Then you should be able to access api on http://localhost:5000/ 

Local db is ready to go and filled with some data. Look at ```sampledata.json``` 

## Env variables 

If you run local, default setting is development. Remember to setup env variables like: 
* IP_STACK_KEY -if db is unaccessible it is used to access ```http://api.ipstack.com/``` API.


# Notes 
Run tests  ```python manage.py test```

Run local  ```python manage.py run```

### For db init and migrations 
```
python manage.py db init
python manage.py db migrate --message 'message'
python manage.py db upgrade
```