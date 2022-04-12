"""
SFU CMPT 756
Sample STANDALONE application---music service.
"""

# Standard library modules
import os
import sys
import uuid
# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request, Response
from put_item import put_music
# Local modules
import boto3
import json
import decimal

# The path to the file (CSV format) containing the sample data
DB_PATH = '/data/top10.csv'

# The unique exercise code
# The EXER environment variable has a value specific to this exercise
# ucode = unique_code.exercise_hash(os.getenv('EXER'))

# The application

app = Flask(__name__)

bp = Blueprint('app', __name__)

database = {}

region = os.getenv('AWS_REGION', 'us-west-2')


loader_token = os.getenv('SVC_LOADER_TOKEN')
access_key = 'djnasdaskj'
secret_access_key = 'djasndaadsj'

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name=region,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_access_key)


@bp.route('/', methods=['GET'])
def list_all():
    """
    To read all data from db
    """
    table = dynamodb.Table('Leaderboard')
    a = table.scan()

    class DecimalEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, decimal.Decimal):
                return int(obj)
            return super(DecimalEncoder, self).default(obj)

    a = json.dumps(a, cls=DecimalEncoder)
    return a


@bp.route('/<music_id>', methods=['GET'])
def get_song(music_id):
    """
    To read single song from DB
    """
    table = dynamodb.Table('Leaderboard')
    try:
        response = table.get_item(Key={'music_id': str(music_id)})
        return response
    except Exception as e:
        print(str(e))
        return {}


@bp.route('/', methods=['POST'])
def create_song():
    """
    Create a new song in DB
    """
    try:
        content = request.get_json()
        Artist = content['Artist']
        SongTitle = content['SongTitle']
        upvotes = int(content['upvotes'])
        genre = content['genre']
        music_id = str(uuid.uuid4())
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    put_music(music_id=music_id, artist=Artist, SongTitle=SongTitle, upvotes=upvotes, genre=genre)
    return "song_added"


@bp.route('/<music_id>', methods=['DELETE'])
def delete_song(music_id):
    """
    Delete a song from DB
    """
    table = dynamodb.Table('Leaderboard')
    table.delete_item(Key={
        'music_id': str(music_id)})
    return "Song Deleted"


app.register_blueprint(bp, url_prefix='/api/v1/leaderboard/')

if __name__ == '__main__':
    p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=p, threaded=True)
