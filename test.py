import requests
import json

BASE_URL = "http://127.0.0.1:3000/api/tracks"

def get_track(track_id=None):
    try:
        if track_id is None:
            url = f"{BASE_URL}"
            res = requests.get(url)
            res.raise_for_status()
            print('Get_tracks')
            print(res.json())
            print('-' * 20)
        else:
            url = f"{BASE_URL}/{track_id}"
            res = requests.get(url)
            if res.status_code == 404:
                print(f'Get_track {track_id}')
                print(f"Track {track_id} not found")
                print('-' * 20)
            else:
                res.raise_for_status()
                print(f'Get_track {track_id}')
                print(res.json())
                print('-' * 20)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")

def post_track(song_name, artist, album, release_year):
    try:
        data = {
            "song_name": song_name,
            "artist": artist,
            "album": album,
            "release_year": release_year
        }
        headers = {
            "Content-Type": "application/json"
        }
        res = requests.post(BASE_URL, data=json.dumps(data), headers=headers)
        res.raise_for_status()
        print('Post_track')
        print(res.json())
        print('-' * 20)
    except requests.exceptions.RequestException as e:
        print('Post_track')
        print(f"An error occurred while making the request: {e}")
        print('-' * 20)
def put_track(track_id, song_name=None, artist=None, album=None, release_year=None):
    try:
        url = f"{BASE_URL}/{track_id}"
        data = {}
        if song_name:
            data["song_name"] = song_name
        if artist:
            data["artist"] = artist
        if album:
            data["album"] = album
        if release_year:
            data["release_year"] = release_year
        headers = {
            "Content-Type": "application/json"
        }
        res = requests.put(url, data=json.dumps(data), headers=headers)
        if res.status_code == 404:
            print(f"Track {track_id} not found")
        elif res.status_code == 400:
            print(res.json()["message"])
            print('-' * 20)
        else:
            res.raise_for_status()
            print(f'Put_track {track_id}')
            print(res.json())
            print('-' * 20)
    except requests.exceptions.RequestException as e:
        print(f'Put_track {track_id}')
        print(f"An error occurred while making the request: {e}")
        print('-' * 20)
def patch_track(track_id, **kwargs):
    try:
        url = f"{BASE_URL}/{track_id}"
        headers = {
            "Content-Type": "application/json"
        }
        res = requests.get(url)
        if res.status_code == 404:
            print(f"Track {track_id} not found")
            return
        track = res.json()
        for key, value in kwargs.items():
            if value is not None:
                track[key] = value
        res = requests.patch(url, data=json.dumps(track), headers=headers)
        if res.status_code == 400:
            print(f'Patch_track {track_id}')
            print(res.json()["message"])
        elif res.status_code == 200:
            res.raise_for_status()
            print(f'Patch_track {track_id}')
            print(f"Track {track_id} updated successfully")
            print(res.json())
            print('-' * 20)
        else:
            print(f"Failed to update track {track_id}")
    except requests.exceptions.RequestException as e:
        print("Patch_track")
        print(f"An error occurred while making the request: {e}")
        print('-' * 20)

def delete_track(track_id):
    try:
        url = f"{BASE_URL}/{track_id}"
        res = requests.delete(url)
        if res.status_code == 404:
            print('Delete_track')
            print(f"Track {track_id} not found")
            print('-' * 20)
        else:
            res.raise_for_status()
            print(f'Delete_track {track_id}')
            print(f"Track {track_id} deleted")
            print('-' * 20)
    except requests.exceptions.RequestException as e:
        print('Delete_track')
        print(f"An error occurred while making the request: {e}")
        print('-' * 20)


delete_track(2)
post_track("Glitch", 'Parkway Drive', 'Darker Still', 2022)
get_track()
put_track(1, 'Sir Psycho Sexy', 'Red Hot Chili Peppers', 'BSSM', 1991)
get_track()
patch_track(1, song_name="Scar Tissue", artist="RHCP", album='Californication')
get_track()
put_track(4, 'Dig', 'Mudvayne', 'L.D.50', 2000)
post_track("Master of Puppets", 'Metallica', 'Master of Puppets', 1986)
patch_track(3, artist='Vasiliy Utkin')
patch_track(4, album='Vulgar Display of Power', song_name='Walk', release_year='dsdjsoiddjdid')
get_track()
get_track(2)
get_track(-5)
get_track(7)