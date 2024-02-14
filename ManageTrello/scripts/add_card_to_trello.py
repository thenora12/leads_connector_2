# import requests
#
#
# def create_trello_card(key, token, board_id, list_id, card_name, card_description):
#     url = f"https://api.trello.com/1/cards?key={key}&token={token}&idList={list_id}&name={card_name}&desc={card_description}"
#     response = requests.post(url)
#     if response.status_code == 200:
#         print("Carte créée avec succès sur Trello!")
#     else:
#         print("Erreur lors de la création de la carte sur Trello.")
#
#
# # Remplacez ces valeurs par vos propres clés et jeton d'accès
# key = "92692647ed258c3832f52e3f9f07d1c2"
# token = "ATTAf55bbe1ec116e09dca1629be00711a0d4229f284cc0dbf32dcbee29c89c07e30283BE08B"
#
# # Remplacez ces valeurs par l'ID de votre tableau et de votre liste Trello
# board_id = "65ca446717ccf180b5083436"
# list_id = "65ca447a5870e4c204ce1c1b"
#
# # Remplacez ces valeurs par le nom et la description de votre carte
# card_name = "NOM_DE_VOTRE_CARTE"
# card_description = "DESCRIPTION_DE_VOTRE_CARTE"
#
# create_trello_card(key, token, board_id, list_id, card_name, card_description)

from trello import TrelloClient


def create_trello_card(key, token, board_id, list_id, card_name, card_description):
    client = TrelloClient(api_key=key, token=token)
    board = client.get_board(board_id)
    target_list = board.get_list(list_id)
    target_list.add_card(name=card_name, desc=card_description)
    print("Carte créée avec succès sur Trello!")


# Remplacez ces valeurs par vos propres clés et jeton d'accès
key = "92692647ed258c3832f52e3f9f07d1c2"
token = "ATTAf55bbe1ec116e09dca1629be00711a0d4229f284cc0dbf32dcbee29c89c07e30283BE08B"

# Remplacez ces valeurs par l'ID de votre tableau et de votre liste Trello
board_id = "65ca446717ccf180b5083436"
list_id = "65ca447a5870e4c204ce1c1b"

# Remplacez ces valeurs par le nom et la description de votre carte
card_name = "Teste"
card_description = "Teste"

create_trello_card(key, token, board_id, list_id, card_name, card_description)


