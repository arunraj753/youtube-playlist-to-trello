import os
from googleapiclient.discovery import build
import json
import requests

youtube_api_key = os.environ.get("YOUTUBE_API_KEY")
trello_api_token = os.environ.get("TRELLO_API_TOKEN")

youtube = build("youtube", "v3", developerKey=youtube_api_key)


playlist_videos_id = []
next_page_token = None


def get_playlist_id(playlist_url):
    youtube_url, play_list_id = playlist_url.split("&list=")
    if youtube_url.startswith(
        "https://www.youtube.com/watch?v="
    ) and play_list_id.startswith("PL"):
        play_list_id = play_list_id.split("&index")[0]
        print("play_list_id : ", play_list_id)
        return play_list_id
    else:
        print("Invalid playlist url")
        exit(0)


def fetch_playlist_title(play_list_id):
    try:
        playlist_request = youtube.playlists().list(
            part="snippet",
            id=play_list_id,
        )
        playlist_response = playlist_request.execute()
        playlist_title = playlist_response["items"][0]["snippet"]["title"]
        print("Playlist Title : ", playlist_title)
        return playlist_title
    except Exception as e:
        print("An error occured in fetch_playlist_title() \n", e)
        exit(0)


def fetch_playlist_videos(play_list_id):
    playlist_video_ids = []
    next_page_token = None
    while True:
        playlist_request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=play_list_id,
            pageToken=next_page_token,
        )
        try:
            playlist_response = playlist_request.execute()
        except Exception as e:
            if isinstance(e, str):
                print(e)
            else:
                if e.resp.get("content-type", "").startswith("application/json"):
                    reason = (
                        json.loads(e.content)
                        .get("error")
                        .get("errors")[0]
                        .get("reason")
                    )
                    print(reason)
                else:
                    print("An error occured")
            exit(0)

        for item in playlist_response["items"]:
            video_id = item["contentDetails"]["videoId"]
            playlist_video_ids.append(video_id)
        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            print(f"Fetched {len(playlist_video_ids)} videos ids from the playlist")
            break
    return playlist_video_ids


def fetch_video_details(playlist_video_ids):
    videos_count = len(playlist_video_ids)
    start = 0
    end = videos_count if videos_count <= 50 else 50
    playlist_video_details = []
    while True:
        video_ids = playlist_video_ids[start:end]
        try:
            vid_request = youtube.videos().list(part="snippet", id=video_ids)
            vid_response = vid_request.execute()
            playlist_video_details.extend(vid_response["items"])
            print(f"\tVideos from {start+1} to {end}")
        except Exception as e:
            print("Error while fetching Videos : ", e)
            exit(0)
        if end >= videos_count:
            break
        start = end
        end = videos_count if videos_count < start + 50 else start + 50
    return playlist_video_details


if __name__ == "__main__":
    playlist_url = input("Add the youtube playlist url : ")
    play_list_id = get_playlist_id(playlist_url)
    playlist_title = fetch_playlist_title(play_list_id)
    playlist_video_ids = fetch_playlist_videos(play_list_id)
    playlist_video_details = fetch_video_details(playlist_video_ids)
    print(f"Fetched {len(playlist_video_details)} video details")
    index = 0

    # for video in playlist_video_details:
    #     print(video["snippet"]["title"])
    #     print("https://www.youtube.com/watch?v=" + playlist_video_ids[index])
    #     index += 1
