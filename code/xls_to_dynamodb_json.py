import pandas as pd
from unicodedata import normalize
import sys, getopt

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
def lerExcel(inputfile):
    df = pd.read_excel(inputfile)

    df['Descricao-BUSCA'] = df['Descricao']
    df['Descricao-BUSCA'] = df.apply(lambda row: remover_acentos(row['Descricao-BUSCA']), axis=1)
    df['Codigo'] = df.apply(lambda row: limpa_codigo(row['Codigo']), axis=1)

    return df

def formata_items_json(df):
    df['Descricao'] = df.apply(lambda row: " {\"S\" : \"%s\"} " % row['Descricao'], axis=1)
    df['Descricao-BUSCA'] = df.apply(lambda row: " {\"S\" : \"%s\"} " %row['Descricao-BUSCA'], axis=1)
    df['Codigo'] = df.apply(lambda row: " {\"S\" : \"%s\"} " %row['Codigo'], axis=1)

    return df

#Metodo para gerar o JSON
def geraJson(df,outputfile, tableName):
    cnaes = formata_items_json(df)
    #Adicionando cabeçalho de uma tabela do DynamoDb
    jsonTxt = "{ \" %s \" : [ " % tableName

    #Iterando valores do DataFrame
    for index, item in cnaes.iterrows():
        jsonTxt = jsonTxt + "  { \"PutSegment\" : { \"Item\" : { \"Codigo\": %s, \"Descricao\": %s, \"Descricao-BUSCA\": %s } } } ," % (item['Codigo'], item['Descricao'], item['Descricao-BUSCA'])

    #fechadno o JSON
    jsonTxt = jsonTxt[:-1] + "  ]  }"
    jsonTxt.replace("\('", "").replace("',\)", "")

    #gerando o arquivo .json
    file =  open(outputfile, "w")
    file.write(jsonTxt)
    file.close()


def main(argv):
    inputfile = 'clean_cnae.xlsx'
    outputfile = 'atividadeEconomica.json'
    tableName = 'AtividadeEconomica'

    try:
        opts, args = getopt.getopt(argv,"hi:o:n:",["input=","output=", "name="])
    except getopt.GetoptError:
        print ('xls_to_dynamodb_json.py -i <inputfile> -o <outputfile> -n <tableName>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('xls_to_dynamodb_json.py -i <inputfile> -o <outputfile> -n <tableName>')
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            outputfile = arg
        elif opt in ("-n", "--name"):
            tableName = arg

    xls2df = lerExcel(inputfile)
    geraJson(xls2df, outputfile, tableName)


if __name__ == "__main__":
   main(sys.argv[1:])
