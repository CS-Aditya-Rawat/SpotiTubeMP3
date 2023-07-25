import requests
import yt_dlp
from bs4 import BeautifulSoup


def get_spotify_playlist_details(playlist_url):
    page_content = requests.get(url=playlist_url, stream=True).content
    bs_instance = BeautifulSoup(page_content, "lxml")
    meta_tags = bs_instance.find_all("meta", {"name": "music:song"})
    track_ids = [tag.get("content") for tag in meta_tags]
    print(f"Found {len(track_ids)} songs in the Playlist")
    tracks = []
    try:
        for track in track_ids:
            page = requests.get(track, stream=True).content
            data = BeautifulSoup(page, "lxml")
            track_details = data.title.text
            [song_name, singer] = track_details.rsplit("-", 1)
            singer = singer[singer.find("by") + 3 : singer.find("|")].strip()
            tracks.append([song_name, singer])
    except Exception as e:
        print(e)

    return tracks


def download_youtube_audio(search_query, output_path):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": output_path + "/%(title)s.%(ext)s",
        "default_search": "ytsearch",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(search_query, download=True)

    print(f"Downloaded: {info_dict['title']}.mp3")


if __name__ == "__main__":
    PLAYLIST_URL = ""  # Enter The Playlist URL
    songs = get_spotify_playlist_details(PLAYLIST_URL)
    CUSTOM_PATH = ""  # Enter the Path where to save songs
    for song, singer in songs:
        download_youtube_audio(song + " " + singer, "CUSTOM_PATH")
