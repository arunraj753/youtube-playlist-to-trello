from googleapiclient.discovery import build
import os
import json

youtube_api_key = os.environ.get("YOUTUBE_API_KEY")


class YoutubeModule:

    youtube = build("youtube", "v3", developerKey=youtube_api_key)

    def get_playlist_id(self, playlist_url):
        url_split = playlist_url.split("&list=")
        if len(url_split) == 2:
            youtube_url, play_list_id = url_split
            if youtube_url.startswith(
                "https://www.youtube.com/watch?v="
            ) and play_list_id.startswith("PL"):
                play_list_id = play_list_id.split("&index")[0]
                print("play_list_id : ", play_list_id)
                return play_list_id
            else:
                print("Invalid playlist url")
                exit(0)
        else:
            print("Invalid playlist url")
            exit(0)

    def fetch_playlist_title(self, play_list_id):
        try:
            playlist_request = self.youtube.playlists().list(
                part="snippet",
                id=play_list_id,
            )
            playlist_response = playlist_request.execute()
            playlist_title = playlist_response["items"][0]["snippet"]["title"]
            print("Playlist Title : ", playlist_title)
            return playlist_title
        except Exception as e:
            # print("An error occured in fetch_playlist_title() \n", e)
            print("Invalid Playlist URL")
            exit(0)

    def fetch_playlist_videos(self, play_list_id):
        playlist_video_ids = []
        next_page_token = None
        while True:
            playlist_request = self.youtube.playlistItems().list(
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

    def get_video_thumbnail(self, video_id):
        vid_request = self.youtube.videos().list(part="snippet", id=video_id)
        vid_response = vid_request.execute()
        channel_thumbnails = vid_response["items"][0]["snippet"]["thumbnails"][
            "standard"
        ]
        thumbnail_url = channel_thumbnails["url"]
        return thumbnail_url

    def fetch_video_details(self, playlist_video_ids):
        videos_count = len(playlist_video_ids)
        start = 0
        end = videos_count if videos_count <= 50 else 50
        playlist_video_details = []
        while True:
            video_ids = playlist_video_ids[start:end]
            try:
                vid_request = self.youtube.videos().list(part="snippet", id=video_ids)
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
