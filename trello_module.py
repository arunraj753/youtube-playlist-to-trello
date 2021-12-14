import os
import requests
from requests.api import request
import time

trello_api_key = os.environ.get("TRELLO_API_KEY")
trello_api_token = os.environ.get("TRELLO_API_TOKEN")
YOUTUBE_BOARD_NAME = "The Youtube Board"
YOUTUBE_BOARD_NAME = "Getting Things Done - GTD"


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
        print(request_url)
        print("Payload : ", self.payload)
        response = requests.get(request_url, data=self.payload)
        self.validate_response_status(response)
        response_json = response.json()
        return response_json

    def create_card(self, list_id, card_name, desc):
        endpoint = "1/cards"
        request_url = self.url + endpoint
        payload = self.payload.copy()
        payload.update({"idList": list_id, "name": card_name, "desc": desc})
        response = requests.post(request_url, data=payload)
        self.validate_response_status(response)
        response_json = response.json()
        print(response_json)

    def get_or_create_youtube_board(self):
        boards_json = self.get_user_boards()
        for board in boards_json:
            if board["name"] == YOUTUBE_BOARD_NAME:
                print("Youtube Board Found")
                return board["id"]
        exit(0)
        endpoint = "1/boards/"
        request_url = self.url + endpoint

        payload = self.payload.copy()
        payload.update({"name": YOUTUBE_BOARD_NAME, "defaultLists": "false"})
        response = requests.post(request_url, data=payload)
        self.validate_response_status(response)
        print(" Youtube Board Created!!")
        board_id = response.json()["id"]
        return board_id


# 61b5b73439525b53b1517e05
