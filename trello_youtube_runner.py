from youtube_module import YoutubeModule

yt = YoutubeModule()

if __name__ == "__main__":
    playlist_url = input("Add the youtube playlist url : ")
    play_list_id = yt.get_playlist_id(playlist_url)
    playlist_title = yt.fetch_playlist_title(play_list_id)
    playlist_video_ids = yt.fetch_playlist_videos(play_list_id)
    playlist_video_details = yt.fetch_video_details(playlist_video_ids)
    print(f"Fetched {len(playlist_video_details)} video details")
    print("Code executed successfully")

    index = 0
    for video in playlist_video_details:
        print(video["snippet"]["title"])
        print("https://www.youtube.com/watch?v=" + playlist_video_ids[index])
        index += 1
