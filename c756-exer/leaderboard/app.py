"""
SFU CMPT 756
Sample STANDALONE application---music service.
"""

# Standard library modules
import csv
import logging
import os
import sys
import uuid

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request

# Local modules
import unique_code
import boto3

# The path to the file (CSV format) containing the sample data
DB_PATH = '/data/top10.csv'

# The unique exercise code
# The EXER environment variable has a value specific to this exercise
# ucode = unique_code.exercise_hash(os.getenv('EXER'))

# The application

app = Flask(__name__)

bp = Blueprint('app', __name__)

database = {}

#
# def load_db():
#     global database
#     with open(DB_PATH, 'r') as inp:
#         rdr = csv.reader(inp)
#         next(rdr)  # Skip header line
#         for artist, songtitle, id, upvotes, genre in rdr:
#             database[id] = (artist, songtitle, upvotes, genre)

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete"
    ]
}

region = os.getenv('AWS_REGION', 'us-west-2')

# these must be present; if they are missing, we should probably bail now
# access_key = os.getenv('AWS_ACCESS_KEY_ID')
# secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Must be presented to authorize call to `/load`
loader_token = os.getenv('SVC_LOADER_TOKEN')

dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url='http://localhost:8000',
        region_name=region)

@bp.route('/health')
def health():
    return ""


@bp.route('/readiness')
def readiness():
    return ""


@bp.route('/', methods=['GET'])
def list_all():
    # global database
    table = dynamodb.Table('Leaderboard-shivekchhabra')
    print("===========")
    print("here")
    print("=============")
    print(table.get_items())
    # items = table.get_item(
    #         Key={
    #             'uuid' : 1,
    #         }
    #     )
    # print(items)

    # response = {
    #     "Count": len(database),
    #     "Items":
    #         [{'Artist': value[0], 'SongTitle': value[1], 'music_id': id, 'upvotes':value[2], 'genre':value[3]}
    #          for id, value in database.items()]
    # }
    return 'table'


@bp.route('/<music_id>', methods=['GET'])
def get_song(music_id):
    global database
    if music_id in database:
        value = database[music_id]
        response = {
            "Count": 1,
            "Items":
                [{'Artist': value[0],
                  'SongTitle': value[1],
                  'music_id': music_id,
                  'upvotes': value[2],
                  'genre': value[3]}]
        }
    else:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    return response

@bp.route('/v1/<genre>', methods=['GET'])
def get_song_genre(genre):
    global database
    data = []
    print(list(database.values()))
    for i in list(database.values()):
        if i[3]== genre:
            data.append([i[0], i[1], i[2], i[3]])
    print(data)
    response = {
    "Count": len(data),
    "Items":
        [{'Artist': value[0], 'SongTitle': value[1], 'upvotes':value[2], 'genre':value[3]}
        for value in data]
    }
    
    return response


@bp.route('/', methods=['POST'])
def create_song():
    global database
    try:
        content = request.get_json()
        Artist = content['Artist']
        SongTitle = content['SongTitle']
        upvotes = content['upvotes']
        genre = content['genre']
    except Exception:
        return app.make_response(
            ({"Message": "Error reading arguments"}, 400)
            )
    music_id = str(uuid.uuid4())
    database[music_id] = (Artist, SongTitle, upvotes, genre)
    response = {
        "music_id": music_id
    }
    return response


@bp.route('/<music_id>', methods=['DELETE'])
def delete_song(music_id):
    global database
    if music_id in database:
        del database[music_id]
    else:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    return {}

@bp.route('/<music_id>', methods=['POST'])
def upvote(music_id):
    global database
    if music_id in database:
        try:
            content = request.get_json()
            value = database[music_id]
            upvotes = value[2]
            upvotes = str(int(upvotes)+1)
            database[music_id] = (value[0], value[1], upvotes, value[3])
            response = {
        "music_id": music_id
    }

        except Exception as e:
            return app.make_response(
            ({"Message": "Error reading data"}, 400)
            )
        
    else:
        response = {
            "Count": 0,
            "Items": []
        }
    
        return app.make_response((response, 404))
    return response

# @bp.route('/test', methods=['GET'])
# def test():
#     # This value is for user scp756-221
#     if ('1e0715252b48ed14858ae1ce646d67195183ffb8f9dc02d73c82323d8d75f482' !=
#             ucode):
#         raise Exception("Test failed")
#     return {}


@bp.route('/shutdown', methods=['GET'])
def shutdown():
    # From https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c # noqa: E501
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return {}


app.register_blueprint(bp, url_prefix='/api/v1/music/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("missing port arg 1")
        sys.exit(-1)

    # load_db()
    # app.logger.error("Unique code: {}".format(ucode))
    p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=p, threaded=True)
