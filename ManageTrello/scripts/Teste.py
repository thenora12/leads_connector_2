# import os
# import django
# from trello import TrelloClient
#
# # Définir la variable d'environnement DJANGO_SETTINGS_MODULE
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
#
# # Assurez-vous que les paramètres Django sont configurés
# django.setup()
#
# from ManageTrello.models.models_card import CardTrello
#
#
# def create_trello_card(key, token, board_id, list_id, card_name, card_description):
#     client = TrelloClient(api_key=key, token=token)
#     board = client.get_board(board_id)
#     target_list = board.get_list(list_id)
#     card = target_list.add_card(name=card_name, desc=card_description)
#     return card.id, card
#
#
# # Fonction pour enregistrer les données dans la base de données Django
# def save_trello_card_data_to_database(card_id, nom_complet, telephone, addresse, prix, quantite, date_reception,
#                                       produit, numero_suivi, source, statut_commande, city_ramassage_sendit):
#     trello_card = CardTrello(
#         card_id=card_id,
#         nom_complet=nom_complet,
#         telephone=telephone,
#         addresse=addresse,
#         prix=prix,
#         quantite=quantite,
#         date_reception=date_reception,
#         produit=produit,
#         numero_suivi=numero_suivi,
#         source=source,
#         statut_commande=statut_commande,
#         city_ramassage_sendit=city_ramassage_sendit
#     )
#     trello_card.save()
#
#
# # Utilisation des fonctions
# # Remplacez ces valeurs par vos propres clés et jeton d'accès
# key = "92692647ed258c3832f52e3f9f07d1c2"
# token = "ATTAf55bbe1ec116e09dca1629be00711a0d4229f284cc0dbf32dcbee29c89c07e30283BE08B"
#
# # Remplacez ces valeurs par l'ID de votre tableau et de votre liste Trello
# board_id = "65ca446717ccf180b5083436"
# list_id = "65ca447a5870e4c204ce1c1b"
#
# # Remplacez ces valeurs par le nom et la description de votre carte
# card_name = "cc"
# card_description = "cc"
#
# # Création de la carte dans Trello
# card_id, card = create_trello_card(key, token, board_id, list_id, card_name, card_description)
#
# # Enregistrement des données dans la base de données Django
# save_trello_card_data_to_database(
#     card_id,
#     "Nom_Complet",
#     "Téléphone",
#     "Adresse",
#     100,  # Prix
#     2,  # Quantité
#     "Date_de_réception",
#     "Produit",
#     "Numéro_de_Suivi",
#     "Source",
#     "Statut_Commande",
#     "City_Ramassage_Sendit"
# )


import os
import django

# Définir la variable d'environnement DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Assurez-vous que les paramètres Django sont configurés
django.setup()

from trello import TrelloClient
from ManageTrello.models.models_card import CardTrello


def fetch_trello_cards_and_save_to_database():
    # Remplacez ces valeurs par vos propres clés et jeton d'accès
    key = "92692647ed258c3832f52e3f9f07d1c2"
    token = "ATTAf55bbe1ec116e09dca1629be00711a0d4229f284cc0dbf32dcbee29c89c07e30283BE08B"

    # Remplacez ces valeurs par l'ID de votre tableau et de votre liste Trello
    board_id = "65ca446717ccf180b5083436"
    list_id = "65ca447a5870e4c204ce1c1b"

    # Se connecter à Trello
    client = TrelloClient(api_key=key, token=token)
    board = client.get_board(board_id)
    target_list = board.get_list(list_id)

    # Parcourir les cartes dans la liste cible
    for card in target_list.list_cards():
        # Vérifier si la carte existe déjà dans la base de données
        if not CardTrello.objects.filter(card_id=card.id).exists():
            # Créer une nouvelle instance de modèle pour la carte
            trello_card = CardTrello(
                card_id=card.id,
                nom_complet=card.name,  # Utilisez les informations pertinentes de la carte Trello
                telephone="",
                addresse="",
                prix=0,
                quantite=0,
                date_reception="",
                produit="",
                numero_suivi="",
                source="",
                statut_commande="",
                city_ramassage_sendit="",
            )
            # Enregistrer la carte dans la base de données
            trello_card.save()


# Appeler la fonction pour récupérer les cartes Trello et les enregistrer dans la base de données
fetch_trello_cards_and_save_to_database()
