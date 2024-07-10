# importing the requests library
import requests
 
# api-endpoint
URL = "http://cloud-subscriptions.test:90/api/auth/login"
APIKEY = "Durian season 2024"
 
# defining a params dict for the parameters to be sent to the API
HEADERS = {'x-api-key':APIKEY, 'Accept':'application/json'}
PARAMS = {'email':'admin@example.com', 'password':'password'}
 
# sending get request and saving the response as response object
response = requests.post(url = URL, headers=HEADERS, data=PARAMS)
 
# extracting data in json format
data = response.json()
print(data);
