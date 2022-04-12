"""
SFU CMPT 756
Sample STANDALONE application---leaderboard service.
"""

# Standard library modules
import logging
import sys

# Local modules
import requests
import simplejson as json
# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request, Response
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'LeaderBoard process')

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "readall",
        "update"
    ]
}
bp = Blueprint('app', __name__)


@bp.route('/health')
@metrics.do_not_track()
def health():
    """
    Monitors health of the app
    """
    return Response("", status=200, mimetype="application/json")


@bp.route('/readiness')
@metrics.do_not_track()
def readiness():
    """
    Checks if the app is ready
    """
    return Response("", status=200, mimetype="application/json")


@bp.route('/', methods=['GET'])
def list_all():
    """
    To read all data from db
    """
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    payload = {"objtype": "music"}
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/<genre>', methods=['GET'])
def get_genre_songs(genre):
    """
    Filter songs based on a genre
    """
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    payload = {"objtype": "music"}
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    items = response.json()["Items"]
    result = []
    for item in items:
        if item['Genre'] == genre:
            result.append(item)
    resp = {'Count': len(result), "Items": result}
    return resp


@bp.route('/upvote/<music_id>', methods=['POST'])
def upvote(music_id):
    """
    Upvoting a song by 1 based on a given music id
    """
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')

    payload = {"objtype": "music", "objkey": music_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})

    Votes = int(response.json()["Items"][0]["Votes"])

    url = db['name'] + '/' + db['endpoint'][4]
    response = requests.put(
        url,
        params=payload,
        json={"Votes": str(Votes + 1)},
        headers={'Authorization': headers['Authorization']})
    return {"message": 'Song upvoted successfully'}


@bp.route('/downvote/<music_id>', methods=['POST'])
def downvote(music_id):
    """
    Down voting a song by 1 based on a given music id
    """
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')

    payload = {"objtype": "music", "objkey": music_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})

    Votes = int(response.json()["Items"][0]["Votes"])

    url = db['name'] + '/' + db['endpoint'][4]
    response = requests.put(
        url,
        params=payload,
        json={"Votes": str(Votes - 1)},
        headers={'Authorization': headers['Authorization']})
    return {"message": 'Song downvoted successfully'}


@bp.route('/tabletopper', methods=['GET'])
def get_top_song():
    """
    Get the song with highest number of votes
    """
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    payload = {"objtype": "music"}
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    items = response.json()["Items"]
    max = 0
    max_item = ""
    for item in items:
        if int(item['Votes']) > max:
            max = int(item['Votes'])
            max_item = item
    resp = {'Count': 1, "Items": max_item}
    return resp


app.register_blueprint(bp, url_prefix='/api/v1/leaderboard/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("missing port arg 1")
        sys.exit(-1)
    p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=p, threaded=True)
