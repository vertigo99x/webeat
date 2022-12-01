nae=["Eri",'man']
import requests


response=requests.get('http://127.0.0.1:8000/api/v1/user/vendordata/admin/')

print(response.json())