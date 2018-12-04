import pandas as pd
from unicodedata import normalize

#remove os ascentos e transforma em UpperCase
def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII').upper()

#remove os caracteres - e / do campo codigo
def limpa_codigo(codigo):
    if type(codigo) is str:
        if '-' in codigo:
            codigo = codigo.replace('-','')
        if '/' in codigo:
            codigo = codigo.replace('/','')
    return codigo

#Leitura do arquivo em xls, carregando os dados em um DataFrame
def lerExcel():
    df = pd.read_excel('../source/clean_cnae.xlsx')

    df['Descricao-BUSCA'] = df['Descricao']
    df['Descricao-BUSCA'] = df.apply(lambda row: remover_acentos(row['Descricao-BUSCA']), axis=1)
    df['Codigo'] = df.apply(lambda row: limpa_codigo(row['Codigo']), axis=1)

    return df

def formata_items_json(df):
    df['Descricao'] = df.apply(lambda row: " {\"S\" : \"%s\"} " % row['Descricao'], axis=1)
    df['Descricao-BUSCA'] = df.apply(lambda row: " {\"S\" : \"%s\"} " %row['Descricao-BUSCA'], axis=1)
    df['Codigo'] = df.apply(lambda row: " {\"S\" : \"%s\"} " %row['Codigo'], axis=1)

    return df

#Dataframe de Cnaes
cnaes = formata_items_json(lerExcel())

#Adicionando cabeçalho de uma tabela do DynamoDb
jsonTxt = "{ \"AtividadeEconomica\" : [ "

#Iterando valores do DataFrame
for index, item in cnaes.iterrows():
    jsonTxt = jsonTxt + "  { \"PutSegment\" : { \"Item\" : { \"Codigo\": %s, \"Descricao\": %s, \"Descricao-BUSCA\": %s } } } ," % (item['Codigo'], item['Descricao'], item['Descricao-BUSCA'])

#fechadno o JSON
jsonTxt = jsonTxt[:-1] + "  ]  }"
jsonTxt.replace("\('", "").replace("',\)", "")

#gerando o arquivo .json
file =  open("../output/atividadeEconomica.json", "w")
file.write(jsonTxt)
file.close()




#print(cnaes.loc[1])

#print(cnaes.to_json())
