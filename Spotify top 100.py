from pprint import pprint

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


URL = "https://www.billboard.com/charts/hot-100/"
SPOTIPY_CLIENT_ID = "YOUR ID"
SPOTIPY_CLIENT_SECRET = "YOUR SECRET"
SPOTIPY_REDIRECT_URI = "http://example.com"


date_to_travel = input("Which year you would like to travel? Type date in format YYYY-MM-DD: ")
# date_to_travel = "1995-03-20"
year = date_to_travel[:4]
final_url = f"{URL}{date_to_travel}"
response = requests.get(final_url).content

soup = BeautifulSoup(response, "html.parser")
songs_tags = soup.findAll(class_="chart-element__information__song")
# artists_tags = soup.findAll(class_="chart-element__information__artist text--truncate color--secondary")

songs_titles = [song.getText() for song in songs_tags]
# artists = [artist.getText() for artist in artists_tags]


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="playlist-modify-private"))

user_id = sp.current_user()["id"]
tracks = []

# Track search
for song in songs_titles:
    try:
        track = sp.search(q=f"track: {song} year: {year}", type="track")["tracks"]["items"][0]["uri"]
        print(f"Track found - {song}")
        tracks.append(track)
    except IndexError:
        print(f"Track not found - {song}")

# Creating and Adding tracks to playlist
playlist_name = f"Top 100 songs - {date_to_travel}"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=tracks)

