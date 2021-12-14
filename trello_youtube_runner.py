from youtube_module import YoutubeModule
from trello_module import TrelloModule
import time

yt = YoutubeModule()
tr = TrelloModule()
if __name__ == "__main__":

    playlist_url = input("Add the youtube playlist url : ")
    play_list_id = yt.get_playlist_id(playlist_url)
    playlist_title = yt.fetch_playlist_title(play_list_id)
    playlist_video_ids = yt.fetch_playlist_videos(play_list_id)
    playlist_video_details = yt.fetch_video_details(playlist_video_ids)
    print(f"Fetched {len(playlist_video_details)} video details")
    index = 0
    for video in playlist_video_details:
        print(video["snippet"]["title"])
        print("https://www.youtube.com/watch?v=" + playlist_video_ids[index])
        index += 1
    channel_title = playlist_video_details[0]["snippet"]["channelTitle"]
    print("Youtube video details fetching completed\n")
    trello_youtube_board_id = tr.get_or_create_youtube_board()
    lists_on_board_dict = tr.get_lists_on_board(trello_youtube_board_id)
    required_youtube_board_lists = ["Done", "Ongoing", "Playlist-Inbox", "Videos-Inbox"]
    # youtube_board_list_ids_dict = {"Playlist-Inbox": id_1, "Ongoing": id_2, "Done": id_3}
    youtube_board_list_ids_dict = {}
    list_to_modify_dict = {}
    list_to_create_dict = {}
    trello_list_to_create = []
    for list_name in required_youtube_board_lists:
        if list_name in lists_on_board_dict.keys():
            list_id = lists_on_board_dict[list_name]
            youtube_board_list_ids_dict.update({list_name: list_id})
        else:
            trello_list_to_create.append(list_name)

    if trello_list_to_create:
        print("Trello lists to create : ", trello_list_to_create)
        created_list_dict = tr.create_lists_on_board(
            trello_youtube_board_id, trello_list_to_create
        )

        youtube_board_list_ids_dict.update(created_list_dict)
    else:
        print("No lists to create")

    pl_inbox_id = youtube_board_list_ids_dict.get("Playlist-Inbox", None)
    if not pl_inbox_id:
        print("Playlist-Inbox list id not Found")
        exit(0)

    pl_inbox_cards = tr.get_cards_in_a_list(pl_inbox_id)
    for card in pl_inbox_cards:
        desc = card["desc"]
        desc_split = desc.split(":")
        if desc_split and len(desc_split) == 2:
            trello_pl_id = desc_split[1]
            if play_list_id == trello_pl_id:
                print("This playlist already exists in Playlist-Inbox")
                exit(0)
    trello_card_title = playlist_title + "-" + channel_title
    tr.create_card(pl_inbox_id, trello_card_title, f"playlist_id:{play_list_id}")
    exit(0)
    list_names_to_create_dict = [
        trello_list
        for trello_list in youtube_board_dict.keys()
        if trello_list not in lists_on_board
    ]
    if list_names_to_create:
        trello_lists_to_create_dict = {}
        for trello_list_name in list_names_to_create:
            trello_lists_to_create_dict.update(
                {trello_list_name: (youtube_board_lists.index(trello_list_name)) + 1}
            )

        print("trello_lists_to_create_dict : ", trello_lists_to_create_dict)
        tr.create_lists_on_board(trello_youtube_board_id, trello_lists_to_create_dict)
    print("Code executed successfully")
    # lists_to_create = []
    # for trello_list in lists_on_board:
    #     if trello_list['name ']
    # print("Code executed successfully")

    # index = 0
    # for video in playlist_video_details:
    #     print(video["snippet"]["title"])
    #     print("https://www.youtube.com/watch?v=" + playlist_video_ids[index])
    #     index += 1
