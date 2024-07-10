# importing the requests library
import requests
 
# api-endpoint
URL = "http://cloud-subscriptions.test:90/api/testing"
APIKEY = "Durian season 2024"
 
# defining a params dict for the parameters to be sent to the API
PARAMS = {'x-api-key':APIKEY}
 
# sending get request and saving the response as response object
response = requests.get(url = URL, headers=PARAMS)
 
# extracting data in json format
data = response.json()
print(data[0]);
