import requests

url = 'https://sheet.best/api/sheets/9bdcf020-003f-4843-a14d-7f3e11db6070/'

produto = 'camiseta azul'
print(url + f'/search?PRODUTO=*{produto}*')
r = requests.get(f'{url}/search?PRODUTO=*camiseta azul*')

print(r.json())