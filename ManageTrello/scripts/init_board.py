import os

import requests
from trello import TrelloClient
from ManageTrello.models.models_board import WorkSpaceTrello, TableTrello, ListTrello, CustomFieldTrello, LabelTrello, \
    CustomFieldOptionTrello

# Assurez-vous que les variables d'environnement sont définies
os.environ['TRELLO_API_KEY'] = '92692647ed258c3832f52e3f9f07d1c2'
os.environ['TRELLO_API_SECRET'] = '98d6b3d552aba9eec00c9d986f81e18f9167e57132a698dafc6bc73fb9f86514'
os.environ['TRELLO_TOKEN'] = 'ATTAf55bbe1ec116e09dca1629be00711a0d4229f284cc0dbf32dcbee29c89c07e30283BE08B'
LISTES_TRELLO = [
    {"name": "Entrees", "role": "nouvelle_entree"},
    {"name": "SRDV pas encore saisie", "role": "en_attente_de_saisie"},
    {"name": "Confirmees", "role": "confirme"},
    {"name": "A retraiter", "role": "a_retraiter"},
    {"name": "Injoignables societe de livraison", "role": "injoignable"},
    {"name": "A relancer societe de livraison", "role": "a_relancer"},
    {"name": "Sous RDV", "role": "rendez_vous_fixe"},
    {"name": "Communiquees pour livraison", "role": "communique"},
    {"name": "Problematiques", "role": "a_resoudre"},
    {"name": "Livrees", "role": "livre"},
    {"name": "Retournees", "role": "retourne"},
    {"name": "Annulees", "role": "annule"},
    {"name": "Incompletes ou fausses", "role": "a_verifier"},
    {"name": "A NE PAS TOUCHER", "role": "non_modifiable"},
][::-1]


CUSTOM_FIELDS_TRELLO = [
    {'name': 'statut_commande', 'type': 'list', 'options': [{'name': 'En attente', 'color': 'yellow'},
                                                            {'name': 'Confirmee', 'color': 'green'},
                                                            {'name': 'En cours d acheminement', 'color': 'sky'},
                                                            {'name': 'Non atteignable', 'color': 'red'},
                                                            {'name': 'Livree', 'color': 'blue'},
                                                            {'name': 'Annulee', 'color': 'orange'},
                                                            {'name': 'Annulee par le client', 'color': 'orange'},
                                                            {'name': 'Retournee', 'color': 'pink'},
                                                            {'name': 'Payee', 'color': 'lime'},
                                                            {'name': 'Produit indisponible', 'color': 'black'},
                                                            ]
     },
    {'name': 'date_reception', 'type': 'date'},
    {'name': 'nom_complet', 'type': 'text'},
    {'name': 'telephone', 'type': 'text'},
    {'name': 'addresse', 'type': 'text'},
    {'name': 'produit', 'type': 'text'},
    {'name': 'quantite', 'type': 'number'},
    {'name': 'prix', 'type': 'number'},
    {'name': 'city_ramassage_sendit', 'type': 'text'},
    {'name': 'city_sendit', 'type': 'text'},
    {'name': 'societe_livraison', 'type': 'list', 'options': [{'name': 'Sendit', 'color': 'green'},
                                                              {'name': 'Casablanca-livreur', 'color': 'blue'},
                                                              {'name': 'Marrakech-livreur', 'color': 'red'},
                                                              {'name': 'Rabat-Livreur', 'color': 'orange'},
                                                              {'name': 'Tanger-Livreur', 'color': 'purple'},
                                                              {'name': 'Khawa-Tanger-Ville', 'color': 'lime'},
                                                              {'name': 'Khawa-Tanger-Region', 'color': 'pink'},
                                                              {'name': 'Tawsil', 'color': 'sky'},
                                                              ]
     },
    {'name': 'numero_suivi', 'type': 'text'},
    {'name': 'source', 'type': 'list', 'options': [{'name': 'CRM TikTok', 'color': 'blue', 'pos': 1},
                                                   {'name': 'Storeino', 'color': 'green', 'pos': 2},
                                                   {'name': 'Facebook', 'color': 'blue_dark', 'pos': 3},
                                                   {'name': 'Whatsapp', 'color': 'lime', 'pos': 4},
                                                   {'name': 'BIOZONE', 'color': 'purple', 'pos': 5},
                                                   {'name': 'Telephonique', 'color': 'red', 'pos': 6},
                                                   {'name': 'Shopify', 'color': 'sky', 'pos': 7},
                                                   {'name': 'Youcan', 'color': 'orange', 'pos': 8},
                                                   {'name': 'Autre', 'color': 'black_light', 'pos': 9},
                                                   ]
     },
    {'name': 'envoyer_livraison', 'type': 'checkbox'},
    {'name': 'whatsapp_confirmation', 'type': 'checkbox'},
    {'name': 'sms_livraison', 'type': 'checkbox'},
]

LABELS_TRELLO = [
    {'name': 'En attente', 'color': 'yellow_light'},
    {'name': 'Confirmee', 'color': 'green'},
    {'name': 'En cours d acheminement', 'color': 'sky'},
    {'name': 'Non atteignable', 'color': 'red_dark'},
    {'name': 'Livree', 'color': 'blue_light'},
    {'name': 'Annulee', 'color': 'orange_dark'},
    {'name': 'Annulee par le client', 'color': 'orange_light'},
    {'name': 'Retournee', 'color': 'pink_dark'},
    {'name': 'Payee', 'color': 'lime_light'},
    {'name': 'Produit indisponible', 'color': 'black_light'},
]


def create_custom_field(api_key, token, board_id, field_name, field_type):
    headers = {'Content-Type': 'application/json'}
    url = "https://api.trello.com/1/customFields"
    query = {
        'key': api_key,
        'token': token,

    }
    data = {
        'idModel': board_id,
        'modelType': 'board',
        'name': field_name,
        'type': field_type
    }
    response = requests.post(url, headers=headers, params=query, json=data)
    return response.json()


def create_option_custom_field(api_key, token, id_custom_field, value: str, color: str = 'none'):
    url = f"https://api.trello.com/1/customFields/{id_custom_field}/options"
    headers = {'Content-Type': 'application/json'}
    query = {
        'key': api_key,
        'token': token,
    }
    data = {
        'value': {'text': value},
        'pos': 'bottom',
        'color': color
    }
    response = requests.post(url, headers=headers, params=query, json=data)
    return response.json()


def run():
    # Initialisation du client Trello
    api_key = os.environ['TRELLO_API_KEY']
    api_secret = os.environ['TRELLO_API_SECRET']
    token = os.environ['TRELLO_TOKEN']
    print("api_key : %s" % api_key)
    print("api_secret : %s" % api_secret)
    client = TrelloClient(
        api_key=api_key,
        # api_secret=os.environ['TRELLO_API_SECRET'],
        token=token
    )

    # 1) Création de l'objet WorkSpaceTrello
    workspace = WorkSpaceTrello.objects.create(
        name="Gestion des commandes",
    )

    # 2) Création d'un tableau Trello
    tableau_trello = client.add_board("Mon Tableau Trello")
    tableau = TableTrello.objects.create(
        workspace=workspace,
        name=tableau_trello.name,
        id_table=tableau_trello.id,
    )

    # Avant de créer les nouvelles listes, archivez les listes existantes
    existing_lists = tableau_trello.list_lists()
    for list in existing_lists:
        list.close()

    # 3) Création des listes dans le tableau Trello
    for list_info in LISTES_TRELLO:
        trello_list = tableau_trello.add_list(list_info['name'])
        ListTrello.objects.create(
            table=tableau,
            name=trello_list.name,
            id_list=trello_list.id,
            role=list_info['role']
        )

    # 4) Création des champs personnalisés (Custom Fields)
    for field in CUSTOM_FIELDS_TRELLO:
        options = field['options'] if 'options' in field.keys() else None
        response_custom_field = create_custom_field(api_key, token, tableau_trello.id, field['name'], field['type'])

        custom_field = CustomFieldTrello.objects.create(
            table=tableau,
            name=response_custom_field['name'],
            field_type=response_custom_field['type'],
            id_field=response_custom_field['id']
        )

        if response_custom_field['type'] == 'list':
            print('options')
            print(options)
            for option in options:
                print('-' * 20)
                print(option)
                response_option = create_option_custom_field(api_key, token,
                                                             response_custom_field['id'],
                                                             value=option['name'],
                                                             color=option['color']
                                                             )
                if 'error' in response_option.keys():
                    raise Exception(response_option['message'])

                print(response_option)
                CustomFieldOptionTrello.objects.create(
                    custom_field=custom_field,
                    name=option['name'],
                    option_id=response_option["id"],
                    color=option['color'],
                )
                print('-' * 20)

    # 5) Création des étiquettes (Labels)
    for label in LABELS_TRELLO:
        label = tableau_trello.add_label(label['name'], label['color'])  # Choisissez ou déterminez la couleur
        LabelTrello.objects.create(
            table=tableau,
            name=label.name,
            color=label.color
        )

    print("Tout a été créé sur Trello et dans la base de données Django.")
