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
from flask import request, Response
from put_item import put_music
from prometheus_flask_exporter import PrometheusMetrics
# Local modules
import unique_code
import boto3
import requests
import simplejson as json
import decimal

# The path to the file (CSV format) containing the sample data
DB_PATH = '/data/top10.csv'

# The unique exercise code
# The EXER environment variable has a value specific to this exercise
# ucode = unique_code.exercise_hash(os.getenv('EXER'))

# The application

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'LeaderBoard process')

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete"
    ]
}
bp = Blueprint('app', __name__)


@bp.route('/health')
def health():
    return ""


@bp.route('/readiness')
def readiness():
    return ""


# class DecimalEncoder(json.JSONEncoder):
#         def default(self, obj):
#             if isinstance(obj, decimal.Decimal):
#                 return int(obj)
#             return super(DecimalEncoder, self).default(obj)


@bp.route('/', methods=['GET'])
def list_all():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    payload = {"objtype": "music", "objkey": "c2573193-f333-49e2-abec-182915747756"}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())


# @bp.route('/<music_id>', methods=['GET'])
# def get_song(music_id):
#     table = dynamodb.Table('LeaderBoard-projects-g')
#     try:
#         response = table.get_item(Key={'music_id': str(music_id)})
#         return response
#     except Exception as e:
#         print(str(e))
#         return {}
#
#
# @bp.route('/v1/<genre>', methods=['GET'])
# def get_song_genre(genre):
#     table = dynamodb.Table('LeaderBoard-projects-g')
#     try:
#         response = table.scan(FilterExpression=Attr("genre").eq(genre))
#         print(response)
#         return response
#     except Exception as e:
#         print(str(e))
#         return {}
#     # data = []
#     # print(list(database.values()))
#     # for i in list(database.values()):
#     #     if i[3]== genre:
#     #         data.append([i[0], i[1], i[2], i[3]])
#     # print(data)
#     # response = {
#     # "Count": len(data),
#     # "Items":
#     #     [{'Artist': value[0], 'SongTitle': value[1], 'upvotes':value[2], 'genre':value[3]}
#     #     for value in data]
#     # }
#
#     return response
#
#
# @bp.route('/', methods=['POST'])
# def create_song():
#     headers = request.headers
#     # check header here
#     if 'Authorization' not in headers:
#         return Response(json.dumps({"error": "missing auth"}),
#                         status=401,
#                         mimetype='application/json')
#     try:
#         content = request.get_json()
#         Artist = content['Artist']
#         SongTitle = content['SongTitle']
#         upvotes = int(content['upvotes'])
#         genre = content['genre']
#         music_id = str(uuid.uuid4())
#     except Exception:
#         return json.dumps({"message": "error reading arguments"})
#     put_music(music_id=music_id, artist=Artist, SongTitle=SongTitle, upvotes=upvotes, genre=genre)
#     print("here")
#     return "song_added"
#
#
# @bp.route('/<music_id>', methods=['DELETE'])
# def delete_song(music_id):
#     table = dynamodb.Table('LeaderBoard-projects-g')
#     headers = request.headers
#     # check header here
#     if 'Authorization' not in headers:
#         return Response(json.dumps({"error": "missing auth"}),
#                         status=401,
#                         mimetype='application/json')
#     table.delete_item(Key={
#                 'music_id': str(music_id)})
#     return "Song Deleted"
#
#
# @bp.route('/<music_id>', methods=['POST'])
# def upvote(music_id):
#     # dynamodb.updateItem({
#     #     TableName: "Leaderboard",
#     #     Key: {"music_id": {S: music_id}},
#     #     ExpressionAttributeValues: {":inc": {N: "1"}},
#     #     UpdateExpression: "ADD upvotes :inc"
#     # })
#
#     table = dynamodb.Table('LeaderBoard-projects-g')
#     # response = table.get_item(Key={'music_id': str(music_id)})
#     # print(response)
#     # upvotes=int(response['upvote'])+1
#     table.update_item(
#         Key={
#             'music_id': str(music_id)
#         },UpdateExpression="set upvotes=:val",
#         ExpressionAttributeValues={
#             ':val': 1
#         })
#     return {}
#
#
# @bp.route('/shutdown', methods=['GET'])
# def shutdown():
#     # From https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c # noqa: E501
#     func = request.environ.get('werkzeug.server.shutdown')
#     if func is None:
#         raise RuntimeError('Not running with the Werkzeug Server')
#     func()
#     return {}


app.register_blueprint(bp, url_prefix='/api/v1/leaderboard/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("missing port arg 1")
        sys.exit(-1)
    # app.logger.error("Unique code: {}".format(ucode))
    p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=p, threaded=True)