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
        if len(r.json()):
            response = r.json()[0]
            preço = response['PRECO']
            fulfillmentText = {'fulfillmentText': f'O preço do produto é R$ {preço}'}
        else:
            fulfillmentText = {'fulfillmentText': 'Não encontrei o produto'}

        return JsonResponse(fulfillmentText, safe=False)
    
    if action == 'informacao':
        r = requests.get(url + f'search?PRODUTO=*{produto}*')
        if len(r.json()):
            response = r.json()[0] 
            descrição = response['DESCRICAO']
            fulfillmentText = {'fulfillmentText': f'{descrição}'}
        else:
            fulfillmentText = {'fulfillmentText': 'Não encontrei a descrição deste produto.'}

        return JsonResponse(fulfillmentText, safe=False)

    if action == 'promocao':
        r = requests.get(url + f'query?PROMOCAO=1') 
         
        response = r.json()
         
        output = '''Os seguintes produtos estão em promoção em nossa loja: \n'''
        for i in response:
            output += '--' + i['PRODUTO'] + '\n\n\n\n\n'
        
        output += 'Aproveite!'

        if len(response):
            fulfillmentText = {'fulfillmentText': output}
        else:
            fulfillmentText = {'fulfillmentText': 'Não encontrei nenhum produto em promoção.'}

        return JsonResponse(fulfillmentText, safe=False)    