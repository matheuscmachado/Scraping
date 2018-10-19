"""FUNCIONANDO!!!
1ª Melhoria: arrumar as outras entradas como: numero de quartos(rmX), numero de adultos(aX) e de criancas (aX:cY:cY, Y = idade)
2ª Melhoria: jogar os dados para uma planilha (ou pbix) e construir gráficos
3ª Melhoria: trazer diferenças entre os quartos (café, televisão, etc). Precisa?"""

import requests
import json
import datetime
import sys

hoteis = {'Acqua': 2870853, 'Oceani': 5389392, 'Suites': 2651700, 'Wellness': 2478285,
          'Salinas': 2858569, 'Rio Quente': 10238701, 'Iberostar Bahia': 1721960}

for key in hoteis:
    print("Hotel: ",
          key)

#Entrada de dados feita pelo usuário
nome_hotel = input("Escolha um nome de hotel na lista acima para ser pesquisado: ")
start_date = input("Escolha uma data de check-in: ")
end_date = input("Escolha uma data de check-out: ")
#numero_de_quartos = input("Escolha quantos quartos quer na resrva: ")

#captura do ID do hotel segundo o dicionario de hoteis
id_hotel = hoteis[str(nome_hotel)]

""""Construção do link para puxar os dados """

base_url = f"http://www.expedia.com.br/.h{id_hotel}.Hotel-Reservas"
query_string = f"?chkin={start_date}&chkout={end_date}&rm1=a2&sort" \
               f"=recommended&hwrqCacheKey=e1879214-ce8c-4103-abc0-98cbee5a3b24HWRQ1539651169762&" \
               f"cancellable=false&regionId=6034455&vip=false&c=e67b9548-f9da-4fb9-8660-a7bc89bdf9b6&&" \
               f"exp_dp=531.43&exp_ts=1539651170373&exp_curr=BRL&swpToggleOn=false&exp_pg=HSR"

url = base_url + query_string

response = requests.get(url)

html = response.text

"""inicialização das variáveis que vão receber os dados das ofertas e dos quartos"""
dados_de_ofertas = {}
dados_de_quartos = {}

for line in html.split('\n'):
    if 'infosite.offersData' in line:
        dados_de_ofertas = line[21:-1]

ofertas_dict = json.loads(dados_de_ofertas)

for line in html.split('\n'):
    if 'var roomsAndRatePlans' in line:
        dados_de_quartos = line[24:-1]

quartos_dict = json.loads(dados_de_quartos)

hotel_disponibilidade = ofertas_dict['hotelSoldOut']

#Checa se o hotel está sold-out

if hotel_disponibilidade == 0:
    print("\nHá quartos disponíveis no",
          nome_hotel,
          "de",
          datetime.datetime.strptime(start_date, "%d/%m/%Y").strftime("%d/%m/%Y"),
          "a"
          , datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime("%d/%m/%Y"), ".\n")
else:
    print("O",
          nome_hotel,
          "não possui disponibilidade para a data selecionada.\n")

#Se o hotel não está sold-out, captura preço e nome das UHs

for i in range(12):
    try:
        ofertas_quarto_i = ofertas_dict['offers'][i]
        noites_quarto_i = ofertas_quarto_i['nightlyRates']
        quarto_disponibilidade_i = ofertas_quarto_i['bookable']
        preco_quarto_i = ofertas_quarto_i['price']['priceObject']['amount']
        preco_total_quarto_i = ofertas_quarto_i['price']['totalPrice']

        provider_id_i = ofertas_quarto_i['inventoryProviderID']
        roomtype_id_i = ofertas_quarto_i['roomTypeCode']
        chave_quarto_i = str(provider_id_i) + "-" + str(roomtype_id_i)

        nome_quarto_i = quartos_dict['rooms'][chave_quarto_i]['name']

        if quarto_disponibilidade_i == 1:
            print("O quarto",
                  nome_quarto_i
                  ,"encontra-se disponivel de",
                  datetime.datetime.strptime(start_date, "%d/%m/%Y").strftime("%d/%m/%Y")
                  ,"A",
                  datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime("%d/%m/%Y")
                  ,"custando",
                  preco_quarto_i
                  ,"por noite, resultando em um total de:",
                  preco_total_quarto_i
                  ,".")
        else:
            print("O quarto",
                  nome_quarto_i
                  ,"não possui disponibilidade para o período.")
    except:
        sys.exit(1)