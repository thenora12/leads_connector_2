import requests
import os
from dotenv import load_dotenv

from ManageTrello.trello_client import BOARD_ID

load_dotenv()

def run():
    api_key = os.getenv("TRELLO_API_KEY")
    api_token = os.getenv("TRELLO_API_TOKEN")
    webhook_sync_trello2sheet = 'https://10a6-79-93-21-229.ngrok-free.app/sync_trello2sheet/webhook_sync_trello/' # os.getenv("WEBHOOK_SYNC_TRELLO2SHEET")


    print("api_key : %s" % api_key)
    print("api_token : %s" % api_token)

    trello_board_or_list_id = BOARD_ID
    print("trello_board_or_list_id : %s" % str(trello_board_or_list_id))
    url = f"https://api.trello.com/1/tokens/{api_token}/webhooks/"
    headers = {"Content-Type": "application/json"}
    data = {
        "key": api_key,
        "callbackURL": webhook_sync_trello2sheet,
        "idModel": trello_board_or_list_id,
        "description": "Webhook les livraisons à synchroniser avec le Sheet",
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Webhook cree avec succes.")
        # print(response.json())
    else:
        print("Erreur lors de la creation du webhook %s:" % str(response.status_code))
        print(response.text)


