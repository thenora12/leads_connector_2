from django.db import models
import requests
from trello import CustomFieldNumber, CustomFieldText, CustomFieldDate, CustomFieldList

from ManageTrello.models.models_board import ListTrello
from ManageTrello.trello_client import BOARD, TRELLO_LIST_ID_INPUT, CUSTOM_FIELDS_IDS, DICT_SOURCE_FIELDS_SOURCE, \
    DICT_SOURCE_FIELDS_STATUS, api_key, api_token
from ManageTrello.utils.utils_card import get_custom_field_value


class CardTrello(models.Model):
    card_id = models.CharField(max_length=200, unique=True)
    nom_complet = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    addresse = models.CharField(max_length=200)
    prix = models.IntegerField()
    quantite = models.IntegerField()
    date_reception = models.CharField(max_length=200)
    produit = models.CharField(max_length=200)
    numero_suivi = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    statut_commande = models.CharField(max_length=200)
    city_ramassage_sendit = models.CharField(max_length=200)
    list = models.ForeignKey(ListTrello, on_delete=models.CASCADE)
    def create_description(self):
        print('we aree in desc')
        fields = [
            ("👤", "Nom Complet", self.nom_complet),
            ("📞", "Téléphone", self.telephone),
            ("📍", "Adresse", self.addresse),
            ("💰", "Prix", self.prix),
            ("🔢", "Quantité", self.quantite),
            ("📅", "Date de réception", self.date_reception),
            ("📦", "Produit", self.produit),
            ("🔍", "Numéro de Suivi", self.numero_suivi),
            ("🌐", "Source", self.source),
        ]
        print(str(fields))
        description = "\n".join(
            [f"{emoji} {name}: {value if value else 'Non spécifié'}" for emoji, name, value in fields])
        print(description)
        return description

    def get_dict_custom_fields_trello(self):

        custom_fields_dict = {
            "nom_complet": self.nom_complet,
            "telephone": self.telephone,
            "addresse": self.addresse,
            "prix": str(self.prix),
            "quantite": str(self.quantite),
            "date_reception": self.date_reception,
            "produit": self.produit,
            'statut_commande': DICT_SOURCE_FIELDS_STATUS['En attente'],
            "numero_suivi": self.numero_suivi,
        }

        if self.source == '':
            custom_fields_dict.update(
                {'source': DICT_SOURCE_FIELDS_SOURCE['Autre']}
            )
        else:
            custom_fields_dict.update(
                {'source': DICT_SOURCE_FIELDS_SOURCE[self.source]}
            )

        return custom_fields_dict

    def update_custom_fields_card(self, card):

        custom_fields = self.get_dict_custom_fields_trello()
        print('custom_fields : %s' % str(custom_fields))
        for field_name, field_value in custom_fields.items():
            print('set_custom_field : %s | %s' % (field_name, field_value))
            custom_field_type = CUSTOM_FIELDS_IDS[field_name]["type"]
            custom_field_id = CUSTOM_FIELDS_IDS[field_name]["id"]

            if custom_field_type == "text":
                custom_field = CustomFieldText(card, custom_field_id, custom_field_id, field_value)
            elif custom_field_type == "number":
                custom_field = CustomFieldNumber(card, custom_field_id, custom_field_id, field_value)
            elif custom_field_type == "date":
                custom_field = CustomFieldDate(card, custom_field_id, custom_field_id, field_value)
            elif custom_field_type == "list":
                if field_name == 'source':
                    custom_field = CustomFieldList(card, custom_field_id, custom_field_id, field_value)
                    custom_field.list_options = {value: value for key, value in DICT_SOURCE_FIELDS_SOURCE.items()}
                elif field_name == 'statut_commande':
                    custom_field = CustomFieldList(card, custom_field_id, custom_field_id, field_value)
                    custom_field.list_options = {value: value for key, value in DICT_SOURCE_FIELDS_STATUS.items()}
                else:
                    print('Le custom field %s n est pas reconnnu : %s' % field_name)
                    continue
            else:
                continue

            custom_field.field_type = custom_field_type
            card.set_custom_field(field_value, custom_field)

    def update_custom_fields_cardid(self, card_id):
        card = BOARD.get_card(card_id)
        self.update_custom_fields_card(card)

    def push_to_trello(self, list_id=TRELLO_LIST_ID_INPUT):
        print('push_to_trello')
        trello_list = BOARD.get_list(list_id)
        print('trello_list')
        description = self.create_description()
        print(description)
        card = trello_list.add_card(self.nom_complet, description)
        print("card : %s" % str(card))
        self.card_id = card.id
        print('card.id : %s' % str(card.id))
        self.update_custom_fields_card(card)
        return card.id, card


    def get_custom_fields_card(self, card_id):
        base_url = "https://api.trello.com/1"
        url = f"{base_url}/cards/{card_id}/customFieldItems"

        headers = {
            "Accept": "application/json"
        }

        query = {
            "key": api_key,
            "token": api_token
        }

        response = requests.get(url, headers=headers, params=query)
        custom_field_data = response.json()

        full_name = get_custom_field_value(custom_field_data, CUSTOM_FIELDS_IDS['nom_complet'])
        phone = get_custom_field_value(custom_field_data, CUSTOM_FIELDS_IDS['telephone'])
        full_address = get_custom_field_value(custom_field_data, CUSTOM_FIELDS_IDS['addresse'])
        total_with_customer_currency = get_custom_field_value(custom_field_data, CUSTOM_FIELDS_IDS['prix'])
        total_quantity = get_custom_field_value(custom_field_data, CUSTOM_FIELDS_IDS['quantite'])
        product_name = get_custom_field_value(custom_field_data, CUSTOM_FIELDS_IDS['produit'])
        order_date = get_custom_field_value(custom_field_data, CUSTOM_FIELDS_IDS['date_reception'])
        tracking_number = get_custom_field_value(custom_field_data, CUSTOM_FIELDS_IDS['numero_suivi'])
        id_sheeper_operator = get_custom_field_value(custom_field_data, CUSTOM_FIELDS_IDS['societe_livraison'])
        order_source = get_custom_field_value(custom_field_data, CUSTOM_FIELDS_IDS['source'])
        id_trello_order_status = get_custom_field_value(custom_field_data,
                                                        CUSTOM_FIELDS_IDS['statut_commande'])
        city_sendit = get_custom_field_value(custom_field_data,
                                             CUSTOM_FIELDS_IDS['city_sendit'])
        city_ramassage_sendit = get_custom_field_value(custom_field_data,
                                                       CUSTOM_FIELDS_IDS['city_ramassage_sendit'])
        dict_order_values = {
            "full_name": full_name,
            "phone": phone,
            "full_address": full_address,
            "total_with_customer_currency": total_with_customer_currency,
            "total_quantity": total_quantity,
            "product_name": product_name,
            "order_date": order_date,
            "tracking_number": tracking_number,
            "id_sheeper_operator": id_sheeper_operator,
            "source": order_source,
            "id_trello_order_status": id_trello_order_status,
            "city_sendit": city_sendit,
            "city_ramassage_sendit": city_ramassage_sendit,

        }

        return dict_order_values

    @classmethod
    def get_cards_data_by_list(cls, list):
        cards = cls.objects.filter(list=list)
        cards_data = []
        for card in cards:
            card_data = {
                'card_id': card.card_id,
                'nom_complet': card.nom_complet,
                'telephone': card.telephone,
                'addresse': card.addresse,
                'prix': card.prix,
                'quantite': card.quantite,
                'date_reception': card.date_reception,
                'produit': card.produit,
                'numero_suivi': card.numero_suivi,
                'source': card.source,
                'statut_commande': card.statut_commande,
                'city_ramassage_sendit': card.city_ramassage_sendit,
                # Add other fields as needed
            }
            cards_data.append(card_data)
        return cards_data