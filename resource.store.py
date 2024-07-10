# importing the requests library
import requests
 
# api-endpoint
URL = "http://cloud-subscriptions.test:90/api/resources/store"
APIKEY = "Durian season 2024"
 
# defining a params dict for the parameters to be sent to the API
HEADERS = {'x-api-key':APIKEY, 'Accept':'application/json'}
PARAMS = {'name':'admin@example.com', 
          'model_id':1000,
          'serial':'test',
          'purchase_date':'2024-01-01',
          'purchase_cost':100.50,
          'assign_to':1,
          'notes':'test',
          'is_physical':1
          }
 
# sending get request and saving the response as response object
response = requests.post(url = URL, headers=HEADERS, data=PARAMS)
 
# extracting data in json format
data = response.json()
print(data);
