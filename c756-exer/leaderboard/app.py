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
from put_item import put_music
# Local modules
import unique_code
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

# these must be present; if they are missing, we should probably bail now
# access_key = os.getenv('AWS_ACCESS_KEY_ID')
# secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Must be presented to authorize call to `/load`
loader_token = os.getenv('SVC_LOADER_TOKEN')
access_key = 'djnasdaskj'
secret_access_key = 'djasndaadsj'

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name=region,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_access_key)


@bp.route('/health')
def health():
    return ""


@bp.route('/readiness')
def readiness():
    return ""


@bp.route('/', methods=['GET'])
def list_all():
    table = dynamodb.Table('Leaderboard')
    print("hi")
    print(table.scan())
    print("bye")
    a=table.scan()
    class DecimalEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, decimal.Decimal):
                    return int(obj)
                return super(DecimalEncoder, self).default(obj)
    a=json.dumps(a,cls=DecimalEncoder)
    return a


@bp.route('/<music_id>', methods=['GET'])
def get_song(music_id):
    table = dynamodb.Table('Leaderboard')
    try:
        response = table.get_item(Key={'music_id': str(music_id)})
        return response
    except Exception as e:
        print(str(e))
        return {}


@bp.route('/v1/<genre>', methods=['GET'])
def get_song_genre(genre):
    table = dynamodb.Table('Leaderboard')
    try:
        response = table.scan(FilterExpression=Attr("genre").eq(genre))
        print(response)
        return response
    except Exception as e:
        print(str(e))
        return {}
    # data = []
    # print(list(database.values()))
    # for i in list(database.values()):
    #     if i[3]== genre:
    #         data.append([i[0], i[1], i[2], i[3]])
    # print(data)
    # response = {
    # "Count": len(data),
    # "Items":
    #     [{'Artist': value[0], 'SongTitle': value[1], 'upvotes':value[2], 'genre':value[3]}
    #     for value in data]
    # }

    return response


@bp.route('/', methods=['POST'])
def create_song():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
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
    print("here")
    return "song_added"


@bp.route('/<music_id>', methods=['DELETE'])
def delete_song(music_id):
    table = dynamodb.Table('Leaderboard')
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    table.delete_item(Key={
                'music_id': str(music_id)})
    return "Song Deleted"


@bp.route('/<music_id>', methods=['POST'])
def upvote(music_id):
    # dynamodb.updateItem({
    #     TableName: "Leaderboard",
    #     Key: {"music_id": {S: music_id}},
    #     ExpressionAttributeValues: {":inc": {N: "1"}},
    #     UpdateExpression: "ADD upvotes :inc"
    # })

    table = dynamodb.Table('Leaderboard')
    # response = table.get_item(Key={'music_id': str(music_id)})
    # print(response)
    # upvotes=int(response['upvote'])+1
    table.update_item(
        Key={
            'music_id': str(music_id)
        },UpdateExpression="set upvotes=:val",
        ExpressionAttributeValues={
            ':val': 1
        })
    return {}


@bp.route('/shutdown', methods=['GET'])
def shutdown():
    # From https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c # noqa: E501
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return {}


app.register_blueprint(bp, url_prefix='/api/v1/leaderboard/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("missing port arg 1")
        sys.exit(-1)
    # app.logger.error("Unique code: {}".format(ucode))
    p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=p, threaded=True)
