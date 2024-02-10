import requests

from ManageTrello.models.models_board import WorkSpaceTrello, TableTrello, ListTrello, CustomFieldTrello, \
    CustomFieldOptionTrello, LabelTrello

def run():
    # Vos informations d'identification API
    api_key = '92692647ed258c3832f52e3f9f07d1c2'
    token = 'ATTAf55bbe1ec116e09dca1629be00711a0d4229f284cc0dbf32dcbee29c89c07e30283BE08B'

    # Endpoint pour obtenir tous les tableaux de l'utilisateur
    url_get_boards = "https://api.trello.com/1/members/me/boards"

    # Paramètres de la requête
    query = {
        'key': api_key,
        'token': token
    }

    # Récupérer tous les tableaux
    response = requests.get(url_get_boards, params=query)
    boards = response.json()

    # Vérifier si la récupération a réussi
    if response.status_code == 200:
        print(f"{len(boards)} tableaux trouvés. Suppression en cours...")
        # Parcourir chaque tableau et le supprimer
        for board in boards:
            board_id = board['id']
            url_delete_board = f"https://api.trello.com/1/boards/{board_id}"
            del_response = requests.delete(url_delete_board, params=query)

            if del_response.status_code == 200:
                print(f"Tableau {board['name']} supprimé avec succès.")
            else:
                print(f"Échec de la suppression du tableau {board['name']}.")
    else:
        print("Échec de la récupération des tableaux.")

    WorkSpaceTrello.objects.all().delete()
    TableTrello.objects.all().delete()
    ListTrello.objects.all().delete()
    CustomFieldTrello.objects.all().delete()
    CustomFieldOptionTrello.objects.all().delete()
    LabelTrello.objects.all().delete()
