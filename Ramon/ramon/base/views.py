from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests 
import pandas as pd

df = pd.read_csv('assets/Ramon.csv')

print(df)
print()
print()
df_aux = df.loc[df['PRODUTO'] == 'camiseta']
preço = df_aux['PRECO'][0]
print(f'O preço é R$ {preço} reais')
print()
print()

url = 'https://sheet.best/api/sheets/9bdcf020-003f-4843-a14d-7f3e11db6070/'

@api_view(['GET']) 
def home(request):
      return HttpResponse('Hello World!')

@csrf_exempt
@api_view(['POST']) 
def webhook(request):
   
    req = json.loads(request.body)
    action = req.get('queryResult').get('action')
    produto = req.get('queryResult').get('parameters').get('produto')
   
    if action == 'preco':
        # r = requests.get(url + f'search?PRODUTO=*{produto}*')
  
        df_aux = df.loc[df['PRODUTO'] == 'camiseta']
        preço = df_aux['PRECO'][0]

        if preço:
            # response = r.json()[0]
            # preço = response['PRECO']
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
            output += '--' + i['PRODUTO'] + '\n'
        
        output += '\n' + 'Aproveite!'

        if len(response):
            fulfillmentText = {'fulfillmentText': output}
        else:
            fulfillmentText = {'fulfillmentText': 'Não encontrei nenhum produto em promoção.'}

        return JsonResponse(fulfillmentText, safe=False)    