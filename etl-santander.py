import requests
import json
import pandas as pd
import openai

openai_api_key = '###########'
#Utilizando uma instância local do JSON-SERVER (https://github.com/typicode/json-server)
string_api = 'http://localhost:3000/result'

openai.api_key = openai_api_key

df = pd.read_csv('SantanderDesafio.csv')
user_ids = df['UserId'].tolist()

print(user_ids)

def getBank(code):
    response = requests.get(f'{string_api}/{code}')
    return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := getBank(1)) is not None]

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "Você é um corretor imobiliário."},
      {"role": "user", "content": f"Crie uma mensagem para {user['Nome']} sobre novo lançamento em empreendimento (máximo de 100 caracteres)"}
    ]
  )
  return completion.choices[0].message.content.strip('\"')

for user in users:
  mensagem = generate_ai_news(user)
  user['Mensagem'].append({"description": mensagem})

##print (json.dumps(users, indent=2))

def update_user(user):
  response = requests.put(f"{string_api}/{user['id']}", json=user)
  return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"Usuário {user['Nome']} atualizado? {success}")