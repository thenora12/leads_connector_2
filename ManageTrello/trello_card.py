import os
import django
import requests

# Définir la variable d'environnement DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
# Assurez-vous que les paramètres Django sont configurés
django.setup()
from ManageTrello.models.models_board import ListTrello
from trello import TrelloClient
from ManageTrello.models.models_card import CardTrello
from ManageTrello.trello_client import get_list_id_from_name
api_key = os.getenv("TRELLO_API_KEY")
api_token = os.getenv("TRELLO_API_TOKEN")
table_name = os.getenv("TRELLO_TABLE_NAME")
def fetch_trello_cards_and_save_to_database():
    key = "92692647ed258c3832f52e3f9f07d1c2"
    token = "ATTAf55bbe1ec116e09dca1629be00711a0d4229f284cc0dbf32dcbee29c89c07e30283BE08B"
    board_id = "65ca446717ccf180b5083436"
    list_id = "65ca447a5870e4c204ce1c1b"

    client = TrelloClient(api_key=key, token=token)
    board = client.get_board(board_id)
    target_list = board.get_list(list_id)

    # Parcourir les cartes dans la liste cible
    for card in target_list.list_cards():
        # Vérifier si la carte existe déjà dans la base de données
        if not CardTrello.objects.filter(card_id=card.id).exists():
            list_trello_instance = ListTrello.objects.get(id_list='65cb6ae27f0b62cbce1533ab')
            trello_card = CardTrello(
                card_id=card.id,
                nom_complet=card.name,  # Utilisez les informations pertinentes de la carte Trello
                telephone="",
                addresse="",
                prix=1,
                quantite=1,
                date_reception="",
                produit="",
                numero_suivi=1,
                source="",
                statut_commande="",
                city_ramassage_sendit="",
                list=list_trello_instance
            )
            trello_card.save()
fetch_trello_cards_and_save_to_database()
def get_card_id_input(name_card):
    try:
        list_entree = CardTrello.objects.filter(nom_complet=name_card)
    except ListTrello.DoesNotExist:
        return None
    return list_entree
# get_card_id_input("Test")
#Récupère les cartes d'une liste spécifiée par son nom.
def get_cards_from_list(name_liste):
    list_id = get_list_id_from_name(name_liste)
    list_cards =[]
    if list_id:
        list_instance = ListTrello.objects.get(id_list=list_id)
        cards_data = CardTrello.get_cards_data_by_list(list_instance)
        for card_data in cards_data:
            print(card_data)
            list_cards.append(card_data)
    else:
        print(f"List {name_liste} does not exist.")
        return None  # Return None if the list does not exist
    return list_cards
#Retrieves the card IDs from a given list instance.
def get_card_ids_in_list(list_instance):
    ids_card=[]
    if list_instance:
        for card in list_instance:
            ids_card.append(card["card_id"])
    return ids_card
# list = get_cards_from_list("Entrees")
# print(get_card_ids_in_list(list))
# get_list("Entrees")
# fetch_trello_cards_and_save_to_database()
def get_card_id_input(name_card):
    try:
        # Supposons que CardTrello est le bon modèle
        card_list = CardTrello.objects.filter(nom_complet=name_card)
    except CardTrello.DoesNotExist:
        # Journalisez l'erreur ou levez l'exception selon vos préférences
        return []

    return card_list
def get_table_id_from_name(name_card):
    try:
        card = CardTrello.objects.get(nom_complet=name_card)
    except CardTrello.DoesNotExist:
        return None

    return card.card_id
def get_trello_data():
    key = "92692647ed258c3832f52e3f9f07d1c2"
    token = "ATTAf55bbe1ec116e09dca1629be00711a0d4229f284cc0dbf32dcbee29c89c07e30283BE08B"
    board_id = "65ca446717ccf180b5083436"

    client = TrelloClient(api_key=key, token=token)
    board = client.get_board(board_id)
    return board
print(get_trello_data())

