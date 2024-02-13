import os
from trello import TrelloClient

from ManageTrello.models.models_board import TableTrello, CustomFieldOptionTrello, CustomFieldTrello, ListTrello


def get_table_id_from_name(table_name):
    try:
        table = TableTrello.objects.get(name=table_name)
    except TableTrello.DoesNotExist:
        return None

    return table.id_table


def get_custom_field_ids_for_table(table_name):
    try:
        table = TableTrello.objects.get(name=table_name)
    except TableTrello.DoesNotExist:
        return {}

    custom_fields = CustomFieldTrello.objects.filter(table=table)
    custom_field_ids = {field.name: {'id': field.id_field, 'type': field.field_type} for field in custom_fields}
    return custom_field_ids


def get_custom_field_options_of_source():
    try:
        custom_field_source = CustomFieldTrello.objects.get(name='source')
    except CustomFieldTrello.DoesNotExist:
        return {}

    try:
        sources = CustomFieldOptionTrello.objects.filter(custom_field=custom_field_source)
    except CustomFieldOptionTrello.DoesNotExist:
        return {}

    custom_field_ids = {field.name: field.option_id for field in sources}
    return custom_field_ids


def get_custom_field_options_of_status():
    try:
        custom_field_status = CustomFieldTrello.objects.get(name='statut_commande')
    except CustomFieldTrello.DoesNotExist:
        return {}

    try:
        statuses = CustomFieldOptionTrello.objects.filter(custom_field=custom_field_status)
    except CustomFieldOptionTrello.DoesNotExist:
        return {}

    custom_field_ids = {field.name: field.option_id for field in statuses}
    return custom_field_ids


def get_list_id_input():
    try:
        list_entree = ListTrello.objects.get(role='nouvelle_entree')
    except ListTrello.DoesNotExist:
        return None

    return list_entree.id_list


api_key = os.getenv("TRELLO_API_KEY")
api_token = os.getenv("TRELLO_API_TOKEN")
table_name = os.getenv("TRELLO_TABLE_NAME")

client = TrelloClient(api_key=api_key, token=api_token)
BOARD_ID = get_table_id_from_name(table_name)
BOARD = client.get_board(BOARD_ID) if BOARD_ID else None
CUSTOM_FIELDS_IDS = get_custom_field_ids_for_table(table_name) if BOARD else None
DICT_SOURCE_FIELDS_SOURCE = get_custom_field_options_of_source()
DICT_SOURCE_FIELDS_STATUS = get_custom_field_options_of_status()
TRELLO_LIST_ID_INPUT = get_list_id_input()


