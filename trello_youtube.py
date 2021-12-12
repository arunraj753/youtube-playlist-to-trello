import os
from googleapiclient.discovery import build
import json
import requests

youtube_api_key = os.environ.get("YOUTUBE_API_KEY")

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
        return playlist_response["items"][0]["snippet"]["title"]
    except Exception as e:
        print("An error occured in fetch_playlist_title() \n", e)
        exit(0)


if __name__ == "__main__":
    playlist_url = input("Add the youtube playlist url : ")
    play_list_id = get_playlist_id(playlist_url)
    fetch_playlist_title(play_list_id)
    all_videos = []
exit(0)
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
                    json.loads(e.content).get("error").get("errors")[0].get("reason")
                )
                print(reason)
            else:
                print("An error occured")
        exit(0)

    for item in playlist_response["items"]:
        video_id = item["contentDetails"]["videoId"]
        playlist_videos_id.append(video_id)
    next_page_token = playlist_response.get("nextPageToken")
    if not next_page_token:
        break
videos_count = len(playlist_videos_id)
print("playlist videos count : ", videos_count)
# test = playlist_videos_id[:50]
# print(test)

start = 0
end = videos_count if videos_count <= 50 else 50

while True:
    video_ids = playlist_videos_id[start:end]
    try:
        vid_request = youtube.videos().list(part="snippet", id=video_ids)
        vid_response = vid_request.execute()
        all_videos.extend(vid_response["items"])
        # print(vid_response["items"][0]["snippet"]["title"])
        print(f"Fetched videos from {start+1} to {end+1}")
    except Exception as e:
        print("Error while fetching Videos : ", e)
        exit(0)

    if end > videos_count:
        break
    start = end
    end = start + 50

print(len(all_videos))

index = 0

# for v in all_videos:
#     print(v["snippet"]["title"])
#     print("https://www.youtube.com/watch?v=" + playlist_videos_id[index])
#     index += 1

print("\Code executed successfully")


exit(0)
