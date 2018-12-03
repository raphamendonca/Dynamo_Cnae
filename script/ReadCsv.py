import pandas as pd
from unicodedata import normalize
import json

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII').upper()

def limpa_codigo(codigo):
    if type(codigo) is str:
        if '-' in codigo:
            codigo = codigo.replace('-','')
        if '/' in codigo:
            codigo = codigo.replace('/','')
    return codigo

df = pd.read_excel('../clean_cnae.xlsx')

df['Descricao-BUSCA']= df.apply(lambda row: remover_acentos(row['Descricao']), axis=1)
df['Codigo'] = df.apply(lambda row: limpa_codigo(row['Codigo']), axis=1)

#print(df)

class Item:
    Codigo = 0
    Descricao = 'Teste'
    Descricao_BUSCA = 'TESTE'
    def __init__(self, cod, desc, descB):
        self.Codigo = cod
        self.Descricao = desc
        self.Descricao_BUSCA = descB

class PutRequest:
    Item 
    def __init__(self, valor):
        self.Item = valor


p = PutRequest(Item(1,"Asced", "ASCED"))
print(p.Item.Codigo)
print(p.Item.Descricao)
print(p.Item.Descricao_BUSCA)

#json.encoder(p)


