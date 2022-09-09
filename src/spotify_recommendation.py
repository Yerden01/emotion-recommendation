import operator

import spotipy
import json
import random
from collections import Counter


def get_most_repeated_expression(expressions):
    counter = Counter(expressions)
    most_common = counter.most_common(1)
    return most_common[0][0]


def add_new_songs(expressions):
    emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Sad", 5: "Surprise", 6: 'Neutral'}
    remove_neutral_expression = list(filter(lambda x: x != 6, expressions))

    if len(remove_neutral_expression) == 0:
        remove_neutral_expression = [6]

    expression = get_most_repeated_expression(remove_neutral_expression)
    expression_name = emotion_dict[expression]
    print("most repeated expression ", expression_name)

    music_genres = {
        "Angry": [
            "pop",
            "instrumental",
            "classical",
            "power-pop"
        ],
        "Disgust": [
            "ambient",
            "chill",
            "instrumental",
            "new-age"
        ],
        "Fear": [
            "classical",
            "soundtracks",
            "new-age",
            "world-music"
        ],
        "Happy": [
            "pop",
            "dance",
            "disco",
        ],
        "Sad": [
            "acoustic",
            "singer-songwriter",
            "piano",
            "ambient"
        ],
        "Surprise": [
            "jazz",
            "funk"
        ],
        "Neutral": [
            # "ambient",
            "pop",
            "chill",
            # "classical",
        ]
    }
    args_by_expression = {
        "Angry": {
            "max_acousticness": 0.7,
            "min_energy": 0.5,
            # "min_loudness": 0.5,
            "min_tempo": 100,
            "max_valence": 0.5
        },
        "Disgust": {
            "min_instrumentalness": 0.5,
            "max_valence": 0.5
        },
        "Fear": {
            "max_acousticness": 0.5,
            "min_energy": 0.5,
            "min_instrumentalness": 0.5,
            "max_valence": 0.5
        },
        "Happy": {
            "min_danceability": 0.5,
            "min_energy": 0.5,
            "min_tempo": 100,
            "min_valence": 0.5
        },
        "Sad": {
            "min_acousticness": 0.5,
            "max_energy": 0.5,
            "max_tempo": 100,
            "max_valence": 0.5
        },
        "Surprise": {
            "min_energy": 0.5,
        },
        "Neutral": {
        },
    }

    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"

    sp_oauth = spotipy.SpotifyOAuth(client_id, client_secret, "https://not.ready",
                                    scope="user-library-read user-top-read user-modify-playback-state")

    token_dict = sp_oauth.get_access_token()
    token = token_dict['access_token']
    sp_user = spotipy.Spotify(auth=token)

    # print(sp_user.current_user())
    top_artists_json = sp_user.current_user_top_artists()

    top_artists_dumped = json.dumps(top_artists_json, sort_keys=True, indent=4)
    top_artists = json.loads(top_artists_dumped)['items']
    artist_ids = []
    for top_artist in top_artists:
        artist_ids.append(top_artist['id'])

    print(artist_ids)

    top_tracks_json = sp_user.current_user_top_tracks()
    top_tracks_dumped = json.dumps(top_tracks_json, sort_keys=True, indent=4)
    top_tracks = json.loads(top_tracks_dumped)['items']
    track_ids = []
    for top_track in top_tracks:
        track_ids.append(top_track['id'])

    print(track_ids)

    seed_artists = ['4dpARuHxo51G3z768sgnrY']
    # seed_artists = random.sample(artist_ids, 3)
    seed_genres = []
    # seed_genres = random.sample(music_genres[expression_name], 2)
    seed_tracks = ["4OSBTYWVwsQhGLF9NHvIbR", "5s78Y4ulsGO9BJh5s3GrL9", "2mdEsXPu8ZmkHRRtAdC09e", "2vK6Bd4ik48LPuP7Rcl9Eo"]
    # seed_tracks = random.sample(track_ids, 1)
    seed_args = args_by_expression[expression_name]

    print(seed_artists, seed_genres, seed_tracks, seed_args)

    recommendation_response = sp_user.recommendations(seed_artists, seed_genres, seed_tracks, 3, None, **seed_args)

    print(recommendation_response)
    recommendation_response_json = json.dumps(recommendation_response, sort_keys=True, indent=4)
    # print(recommendation_response_json)
    recommendation_tracks = json.loads(recommendation_response_json)['tracks']
    # popular_recommended_tracks = sorted(recommendation_tracks, key=operator.itemgetter('popularity'), reverse=True)
    # print(popular_recommended_tracks)

    for i in range(len(recommendation_tracks)):
        sp_user.add_to_queue(recommendation_tracks[i]['uri'])

    sp_user.next_track()

    # # Capture the authorization code
    # access_token = 'AQCnkiZqaxR_hlbpSyataYI1SowTenTmtm8cFHmPGx4V3LKmjNlhkNqqvO1jzoGOfov5gboZ7e0K2Nmej90MbJ2jQMpEUszVVYwwJOUzTsdXWHBSJIdBiUFl9dwGINLBdVSd1n0h-k81eLS1mUA7kcuN8Bwo'  # Replace with the code from the URL parameters
    #
    #
    # # Create a new Spotipy instance with the access token
    # sp_user = spotipy.Spotify(auth=access_token)


# add_new_songs([0, 0, 0, 0, 6])
# print(get_most_repeated_expression([0, 0, 0, 0, 6]))
