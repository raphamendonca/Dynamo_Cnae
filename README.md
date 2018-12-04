# Dynamo_Cnae
Caraga de Cnae para Dynamo
------------------------------------------------
## Preparando o ambiente

instalar o virtualenv, isso serve para não ser instaladas dependencias e nem necessitar alterar a instalação do
`apt install virtualenv`

Criar um vitual environment
`virtualenv dynamo_cnae p=python3`

ativar o vitual environment
`source dynamo_cnae/bin/activate`

instalar as dependencias na virtualenv
`pip install pandas xlrd `

## Executando os scripts
------------------------------------------------------------------------------------------------------------------------------
para transformar xls em json para o dynamo:
 `python xls_to_dynamodb_json.py -i clean_cnae.xlsx -o atividadeEconomica.json -n Dev.Pessoa.Pessoa.AtividadeEconomica `
 
 serão gerados arquivos limitados a 25 requests
 
 Para executar a carga no dynamo utilize o comando:
 
  `python carrega_dados_aws.py -u localhost:8000 -r local`
  
  Substituir os valores de url e region para a sua instancia do dynamo