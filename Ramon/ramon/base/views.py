from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

url = 'https://sheet.best/api/sheets/9bdcf020-003f-4843-a14d-7f3e11db6070/'

@csrf_exempt
@api_view(['POST']) 
def webhook(request):
   
    req = json.loads(request.body)
    action = req.get('queryResult').get('action')
    produto = req.get('queryResult').get('parameters').get('produto')
 
    if action == 'preco':
        r = requests.get(url + f'search?PRODUTO=*{produto}*')
        preço = r.json()[0]['PRECO']
        fulfillmentText = {'fulfillmentText': f'O preço do produto é R$ {preço}'}

        return JsonResponse(fulfillmentText, safe=False)
    
    if action == 'informacao':
        r = requests.get(url + f'search?PRODUTO=*{produto}*')
        print('r.json()------------' * 5)
        print(r.json())
        descrição = r.json()[0]['DESCRICAO']
        print(descrição)
        fulfillmentText = {'fulfillmentText': f'{descrição}'}

        return JsonResponse(fulfillmentText, safe=False)