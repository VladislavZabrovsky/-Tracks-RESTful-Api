from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracks.db'
db = SQLAlchemy(app)
parser = reqparse.RequestParser()
parser.add_argument("song_name", type=str, required=False)
parser.add_argument("artist", type=str, required=False)
parser.add_argument("album", type=str, required=False)
parser.add_argument("release_year", type=int, required=False)

class TrackModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(255))
    artist = db.Column(db.String(255))
    album = db.Column(db.String(255))
    release_year = db.Column(db.Integer)

    def __init__(self, song_name, artist, album, release_year):
        self.song_name = song_name
        self.artist = artist
        self.album = album
        self.release_year = release_year

def abort_if_track_doesnt_exist(track_id):
    if not TrackModel.query.get(track_id):
        abort(404, message=f"Track {track_id} doesn't exist")

class Track(Resource):
    def get(self, track_id):
        abort_if_track_doesnt_exist(track_id)
        track = TrackModel.query.get(track_id)
        return {
            "id": track.id,
            "song_name": track.song_name,
            "artist": track.artist,
            "album": track.album,
            "release_year": track.release_year
        }

    def delete(self, track_id):
        abort_if_track_doesnt_exist(track_id)
        track = TrackModel.query.get(track_id)
        db.session.delete(track)
        db.session.commit()
        return '', 204

    def put(self, track_id):
        args = parser.parse_args()
        track = TrackModel.query.get(track_id)

        if not track:
            new_track = TrackModel(
                song_name=args["song_name"],
                artist=args["artist"],
                album=args["album"],
                release_year=args["release_year"],
            )
            db.session.add(new_track)
            db.session.commit()
            return {
                "id": new_track.id,
                "song_name": new_track.song_name,
                "artist": new_track.artist,
                "album": new_track.album,
                "release_year": new_track.release_year,
            }
        else:
            track.song_name = args["song_name"]
            track.artist = args["artist"]
            track.album = args["album"]
            track.release_year = args["release_year"]
            db.session.commit()
            return {
                "id": track.id,
                "song_name": track.song_name,
                "artist": track.artist,
                "album": track.album,
                "release_year": track.release_year
            }, 201

    def patch(self, track_id):
        abort_if_track_doesnt_exist(track_id)
        args = parser.parse_args()
        track = TrackModel.query.get(track_id)
        track.song_name = args.get("song_name", track.song_name)
        track.artist = args.get("artist", track.artist)
        track.album = args.get("album", track.album)
        track.release_year = args.get("release_year", track.release_year)
        db.session.commit()
        return {
            "id": track.id,
            "song_name": track.song_name,
            "artist": track.artist,
            "album": track.album,
            "release_year": track.release_year
        }, 200

class TrackList(Resource):
    def get(self):
        tracks = TrackModel.query.all()
        track_data = [
            {
                "id": track.id,
                "song_name": track.song_name,
                "artist": track.artist,
                "album": track.album,
                "release_year": track.release_year,
            }
            for track in tracks
        ]
        return track_data

    def post(self):
        args = parser.parse_args()
        new_track = TrackModel(
            song_name=args["song_name"],
            artist=args["artist"],
            album=args["album"],
            release_year=args["release_year"],
        )
        db.session.add(new_track)
        db.session.commit()
        return {
            "id": new_track.id,
            "song_name": new_track.song_name,
            "artist": new_track.artist,
            "album": new_track.album,
            "release_year": new_track.release_year,
        }, 201

api.add_resource(TrackList, "/api/tracks")
api.add_resource(Track, "/api/tracks/<int:track_id>")

def initialize_database_with_data():
    data = {
        1: {"song_name": "Suck My Kiss", "artist": "Red Hot Chili Peppers", "album": "Blood Sugar Sex Magik", "release_year": 1991},
        2: {"song_name": "Strife", "artist": "Trivium", "album": "Vengeance Falls", "release_year": 2013},
        3: {"song_name": "Off the Abyss", "artist": "Lorna Shore", "album": "...And I Return To Nothingness", "release_year": 2021},
        4: {"song_name": "Cemetery Gates", "artist": "Pantera", "album": "Cowboys from Hell", "release_year": 1990},
        5: {"song_name": "Please End Me", "artist": "Paleface Swiss", "album": "Single track", "release_year": 2023}
    }

    for track_id, track_info in data.items():
        new_track = TrackModel(
            song_name=track_info["song_name"],
            artist=track_info["artist"],
            album=track_info["album"],
            release_year=track_info["release_year"]
        )
        db.session.add(new_track)

    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        initialize_database_with_data()
    app.run(debug=True, port=3000, host="127.0.0.1")