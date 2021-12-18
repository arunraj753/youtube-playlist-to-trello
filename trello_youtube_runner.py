from youtube_module import YoutubeModule
from trello_module import TrelloModule

yt = YoutubeModule()
tr = TrelloModule()
if __name__ == "__main__":

    playlist_url = input("Add the youtube playlist url : ")
    print("\nStarting Youtube Section\n")
    play_list_id = yt.get_playlist_id(playlist_url)
    playlist_title = yt.fetch_playlist_title(play_list_id)
    playlist_video_ids = yt.fetch_playlist_videos(play_list_id)
    playlist_video_details = yt.fetch_video_details(playlist_video_ids)
    print(f"Fetched {len(playlist_video_details)} video details")
    # for video in playlist_video_details:
    #     print(video["snippet"]["title"])

    channel_title = playlist_video_details[0]["snippet"]["channelTitle"]
    first_video_id = playlist_video_ids[0]
    thumbnail_url = yt.get_video_thumbnail(first_video_id)
    print("Starting Trello Section")

    trello_youtube_board_id = tr.get_or_create_youtube_board()
    lists_on_board_dict = tr.get_lists_on_board(trello_youtube_board_id)
    required_youtube_board_lists = ["Done", "Ongoing", "Playlist-Inbox"]
    # youtube_board_list_ids_dict = {"Playlist-Inbox": id_1, "Ongoing": id_2, "Done": id_3}
    youtube_board_list_ids_dict = {}
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

    pl_inbox_list_id = youtube_board_list_ids_dict.get("Playlist-Inbox", None)
    ongoing_list_id = youtube_board_list_ids_dict.get("Ongoing", None)

    if not pl_inbox_list_id:
        print("Playlist-Inbox list id not Found")
        exit(0)
    if not ongoing_list_id:
        print("Ongoing list id not Found")
        exit(0)

    pl_inbox_cards = tr.get_cards_in_a_list(pl_inbox_list_id)
    ongoing_cards = tr.get_cards_in_a_list(ongoing_list_id)
    for card in pl_inbox_cards:
        desc = card["desc"]
        desc_split = desc.split(":")
        if desc_split and len(desc_split) == 2:
            trello_pl_id = desc_split[1]
            if play_list_id == trello_pl_id:
                print("This playlist already exists in Playlist-Inbox list")
                exit(0)
    for card in ongoing_cards:
        desc = card["desc"]
        desc_split = desc.split(":")
        if desc_split and len(desc_split) == 2:
            trello_pl_id = desc_split[1]
            if play_list_id == trello_pl_id:
                print("This playlist already exists in Ongoing list")
                exit(0)
    trello_card_title = playlist_title + "-" + channel_title
    card_desc = f"playlist_id:{play_list_id}"
    created_card_id = tr.create_card(
        pl_inbox_list_id, trello_card_title, card_desc, playlist_url
    )
    tr.create_attachment_on_card(created_card_id, thumbnail_url, "true")
    tr.create_checklist_on_card(
        created_card_id, playlist_video_ids, checklist_name="Videos List"
    )

    print("\nCode Execited Successfully !!!")
