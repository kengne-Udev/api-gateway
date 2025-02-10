from rest_framework.views import APIView
from rest_framework.response import Response
import requests


class UserMicroserviceView(APIView):
    def get(self, request):
        headers = request.headers.copy()
        response = requests.get('http://localhost:8001/api/users', headers=headers)
        return Response(response.json())
    

class ProductMicroserviceView(APIView):

    def get(self, request):
        headers = request.headers.copy()
        print("headers: ", headers["token"])
        response = requests.get('http://localhost:8002/api/products', headers=headers)
        response.raise_for_status()
        return Response(response.json())
