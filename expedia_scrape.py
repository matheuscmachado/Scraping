"""FUNCIONANDO!!!
1ª Melhoria: arrumar as outras entradas como: numero de quartos(rmX), numero de adultos(aX) e de criancas (aX:cY:cY, Y = idade)
2ª Melhoria: jogar os dados para uma planilha (ou pbix) e construir gráficos
3ª Melhoria: trazer diferenças entre os quartos (café, televisão, etc). Precisa?"""

import sys
import json
import datetime

import requests


HOTEIS = {
    'Acqua': 2870853,
    'Oceani': 5389392,
    'Suites': 2651700,
    'Wellness': 2478285,
    'Salinas': 2858569,
    'Rio Quente': 10238701,
    'Iberostar Bahia': 1721960
}


def get_user_choices() -> dict:
    """Asks for user input and returns a dict with the answers."""

    for key in HOTEIS:
        print("Hotel: ", key)

    #Entrada de dados feita pelo usuário
    nome_hotel = input("Escolha um nome de hotel na lista acima para ser pesquisado: ")
    start_date = input("Escolha uma data de check-in: ")
    end_date = input("Escolha uma data de check-out: ")
    #numero_de_quartos = input("Escolha quantos quartos quer na resrva: ")

    try:
        id_hotel = HOTEIS[nome_hotel.title()]  # title() transforms to "First Caps" case
        #TODO: validate start_date & end_date user input
    except Exception:
        print('Hotel escolhido não é válido.')

    return {
        'nome_hotel': nome_hotel,
        'id_hotel': id_hotel,
        'start_date': start_date,
        'end_date': end_date
    }


def get_link(room_data) -> str:
    """Construção do link para puxar os dados."""

    id_hotel = room_data['id_hotel']

    base_url = f"http://www.expedia.com.br/.h{room_data['id_hotel']}.Hotel-Reservas"
    query_string = (
        f"?chkin={room_data['start_date']}&chkout={room_data['end_date']}&rm1=a2&sort"
        + f"=recommended&hwrqCacheKey=e1879214-ce8c-4103-abc0-98cbee5a3b24HWRQ1539651169762&"
        + f"cancellable=false&regionId=6034455&vip=false&c=e67b9548-f9da-4fb9-8660-a7bc89bdf9b6&&"
        + f"exp_dp=531.43&exp_ts=1539651170373&exp_curr=BRL&swpToggleOn=false&exp_pg=HSR"
    )

    return base_url + query_string


def call_and_parse_expedia(link) -> dict:
    response = requests.get(link)
    
    if not response.ok:
        print(f'Erro (código {response.status_code}) ao obter resposta da Expedia: ' + response.text)
    
    html = response.text

    # inicialização das variáveis que vão receber os dados das ofertas e dos quartos
    dados_de_ofertas = {}
    dados_de_quartos = {}

    for line in html.split('\n'):
        if 'infosite.offersData' in line:
            dados_de_ofertas = line[21:-1]
            ofertas_dict = json.loads(dados_de_ofertas)

        elif 'var roomsAndRatePlans' in line:
            dados_de_quartos = line[24:-1]
            quartos_dict = json.loads(dados_de_quartos)
            hotel_disponibilidade = ofertas_dict['hotelSoldOut']

    return {
        'ofertas_dict': ofertas_dict,
        'quartos_dict': quartos_dict,
        'hotel_disponibilidade': hotel_disponibilidade
    }


def check_availability(hotel_disponibilidade, room_data) -> bool:
    """Checa se o hotel está sold-out."""

    if hotel_disponibilidade == 0:
        print("\nHá quartos disponíveis no",
          room_data['nome_hotel'],
          "de",
              datetime.datetime.strptime(room_data['start_date'], "%d/%m/%Y").strftime("%d/%m/%Y"),  # is this necessary?
              "a"
              , datetime.datetime.strptime(room_data['end_date'], "%d/%m/%Y").strftime("%d/%m/%Y"), ".\n")
        return True
    else:
        print("O",
          room_data['nome_hotel'],
          "não possui disponibilidade para a data selecionada.\n")
        return False


def get_offers(room_data, ofertas_dict, quartos_dict):
    """Captura preço e nome das UHs, printando na tela do usuário."""
    
    try:
        for ofertas_quarto_i in ofertas_dict['offers']:
            noites_quarto_i = ofertas_quarto_i['nightlyRates']
            quarto_disponibilidade_i = ofertas_quarto_i['bookable']
            preco_quarto_i = ofertas_quarto_i['price']['priceObject']['amount']
            preco_total_quarto_i = ofertas_quarto_i['price']['totalPrice']

            provider_id_i = ofertas_quarto_i['inventoryProviderID']
            roomtype_id_i = ofertas_quarto_i['roomTypeCode']
            chave_quarto_i = f'{provider_id_i}-{roomtype_id_i}'

            nome_quarto_i = quartos_dict['rooms'][chave_quarto_i]['name']

            if quarto_disponibilidade_i == 1:
                # TODO: fix this message formatting. Transform the dates properly
                print("O quarto",
                  nome_quarto_i
                  ,"encontra-se disponivel de",
                  datetime.datetime.strptime(room_data['start_date'], "%d/%m/%Y").strftime("%d/%m/%Y")
                  ,"A",
                  datetime.datetime.strptime(room_data['end_date'], "%d/%m/%Y").strftime("%d/%m/%Y")
                  ,"custando",
                  preco_quarto_i
                  ,"por noite, resultando em um total de:",
                  preco_total_quarto_i
                  ,".")
            else:
                print("O quarto",
                  nome_quarto_i
                  ,"não possui disponibilidade para o período.")
    except Exception as e:
        print('Erro ao processar. Encerrando o programa.')
        print('Mensagem de erro: {e!r}')
        sys.exit(1)


# Run the program
room_data = get_user_choices()
link = get_link(room_data)
parsed_data = call_and_parse_expedia(link)
is_available = check_availability(parsed_data['hotel_disponibilidade'], room_data)
if is_available:
    get_offers(room_data, parsed_data['ofertas_dict'], parsed_data['quartos_dict'])