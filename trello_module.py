import os
import requests
from requests.api import request
import time

trello_api_key = os.environ.get("TRELLO_API_KEY")
trello_api_token = os.environ.get("TRELLO_API_TOKEN")
YOUTUBE_BOARD_NAME = "The Youtube Board"


class TrelloModule:
    payload = {"key": trello_api_key, "token": trello_api_token}
    url = "https://api.trello.com/"

    def validate_response_status(self, response):
        success_codes = [200, 201, 203]
        if response.status_code not in success_codes:
            print("An error occured.\nResponse status code : ", response.status_code)
            print(response.text)
            exit(0)

    def get_user_boards(self):
        endpoint = "1/members/me/boards"
        request_url = self.url + endpoint
        payload = self.payload.copy()
        payload.update({"fields": "name"})
        response = requests.get(request_url, data=payload)
        self.validate_response_status(response)
        return response.json()

    def get_lists_on_board(self, board_id):
        endpoint = f"1/boards/{board_id}/lists"
        request_url = self.url + endpoint
        response = requests.get(request_url, data=self.payload)
        self.validate_response_status(response)
        return dict(
            [
                (trello_list["name"], trello_list["id"])
                for trello_list in response.json()
            ]
        )

    def create_lists_on_board(self, board_id, trello_list_to_create):
        endpoint = f"1/boards/{board_id}/lists"
        request_url = self.url + endpoint
        created_list_dict = {}
        for list_name in trello_list_to_create:
            payload = self.payload.copy()
            payload.update({"name": list_name})
            response = requests.post(request_url, data=payload)
            self.validate_response_status(response)
            response_json = response.json()
            print(f"Created the list : {list_name}")
            created_list_dict.update({response_json["name"]: response_json["id"]})
        return created_list_dict

    def get_cards_in_a_list(self, list_id):
        endpoint = f"1/lists/{list_id}/cards"
        request_url = self.url + endpoint
        response = requests.get(request_url, data=self.payload)
        self.validate_response_status(response)
        response_json = response.json()
        return response_json

    def create_card(self, list_id, card_name, desc, url):
        endpoint = "1/cards"
        request_url = self.url + endpoint
        payload = self.payload.copy()
        payload.update(
            {"idList": list_id, "name": card_name, "desc": desc, "urlSource": url}
        )
        response = requests.post(request_url, data=payload)
        self.validate_response_status(response)
        response_json = response.json()
        print(
            f"New Trello Card created with title:{card_name} & id: {response_json['id']}"
        )
        return response_json["id"]

    def get_or_create_youtube_board(self):
        boards_json = self.get_user_boards()
        for board in boards_json:
            if board["name"] == YOUTUBE_BOARD_NAME:
                print("Youtube Board Found")
                return board["id"]
        endpoint = "1/boards/"
        request_url = self.url + endpoint

        payload = self.payload.copy()
        payload.update({"name": YOUTUBE_BOARD_NAME, "defaultLists": "false"})
        response = requests.post(request_url, data=payload)
        self.validate_response_status(response)
        print(" Youtube Board Created!!")
        board_id = response.json()["id"]
        return board_id

    def create_attachment_on_card(self, card_id, attatchment_url, cover_status):
        endpoint = f"1/cards/{card_id}/attachments"
        request_url = self.url + endpoint
        payload = self.payload.copy()
        payload.update({"url": attatchment_url, "setCover": cover_status})
        response = requests.post(request_url, data=payload)
        self.validate_response_status(response)
        print("Attachment created on the card")

    def create_checklist_on_card(
        self, card_id, playlist_video_ids, checklist_name="Checklist"
    ):
        endpoint = f"1/cards/{card_id}/checklists"
        request_url = self.url + endpoint
        payload = self.payload.copy()
        payload.update({"name": checklist_name})
        response = requests.post(request_url, data=payload)
        self.validate_response_status(response)
        checklist_id = response.json()["id"]
        print("Checklist created with title : ", checklist_name)
        print("Adding checklist items:-")
        # Adding items to the created checklist
        endpoint = f"1/checklists/{checklist_id}/checkItems"
        request_url = self.url + endpoint
        index = 0
        for video_id in playlist_video_ids:
            video_link = "https://www.youtube.com/watch?v=" + video_id
            payload = self.payload.copy()
            payload.update({"name": video_link})
            response = requests.post(request_url, data=payload)
            self.validate_response_status(response)

            print("\t", video_link)
        print(f"Added {len(playlist_video_ids)} items to checklist")
