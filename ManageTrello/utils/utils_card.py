from trello import TrelloClient

from ManageTrello.trello_client import get_table_id_from_name
from ManageTrello.models.models_card import *


def get_custom_field_value(custom_field_data, custom_field_id):
    # Récupérer la valeur du custom field
    custom_field_value = None
    for field_item in custom_field_data:

        if not isinstance(field_item, dict):
            continue

        if field_item["idCustomField"] == custom_field_id:
            # print("field_item : %s" % str(field_item))
            is_value_exist = "value" in field_item.keys()
            is_idvalue_exist = "idValue" in field_item.keys()
            value_is_none = field_item['value'] is None if is_value_exist else True
            idvalue_is_none = field_item['idValue'] is None if is_idvalue_exist else True
            if is_value_exist:
                if value_is_none and idvalue_is_none:
                    continue
                if value_is_none and not idvalue_is_none:
                    custom_field_value = field_item['idValue']
                else:
                    if 'text' in field_item["value"].keys():
                        custom_field_value = field_item["value"]["text"]
                    elif 'number' in field_item["value"].keys():
                        custom_field_value = float(field_item["value"]["number"])
                    elif 'date' in field_item["value"].keys():
                        custom_field_value = str(field_item["value"]["date"])
                    elif 'checked' in field_item["value"].keys():  # Ajout pour gérer les checkbox
                        custom_field_value = bool(field_item["value"]["checked"])
                    else:
                        raise "Cet id de custom field n'existe pas : %s" % custom_field_id
                    break
            else:
                custom_field_value = field_item['idValue']

    return custom_field_value



