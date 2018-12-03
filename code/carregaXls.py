import pandas as pd
from unicodedata import normalize

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII').upper()

def limpa_codigo(codigo):
    if type(codigo) is str:
        if '-' in codigo:
            codigo = codigo.replace('-','')
        if '/' in codigo:
            codigo = codigo.replace('/','')
    return codigo

def add_to_Dynamo_json(campo):
    return "{\"S\", \"%s\"}" % campo,

def lerExcel():
    df = pd.read_excel('source/clean_cnae.xlsx')

    df['Descricao-BUSCA'] = df['Descricao']
    df['Descricao-BUSCA'] = df.apply(lambda row: remover_acentos(row['Descricao-BUSCA']), axis=1)
    df['Codigo'] = df.apply(lambda row: limpa_codigo(row['Codigo']), axis=1)

    df['Descricao'] = df.apply(lambda row: add_to_Dynamo_json(row['Descricao']), axis=1)
    df['Descricao-BUSCA'] = df.apply(lambda row: add_to_Dynamo_json(row['Descricao-BUSCA']), axis=1)
    df['Codigo'] = df.apply(lambda row: add_to_Dynamo_json(row['Codigo']), axis=1)

    return df

cnaes = lerExcel()
#print(cnaes)

print(cnaes.to_json())
