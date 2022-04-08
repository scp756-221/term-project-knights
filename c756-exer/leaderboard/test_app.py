import requests
import os
from put_item import put_music

username = os.getenv('AWS_ACCESS_KEY_ID')
password = os.getenv('AWS_SECRET_ACCESS_KEY_ID')


def test_read():
    response = requests.get("http://44.238.226.5:80/api/v1/leaderboard/", auth=(username, password))
    assert response.status_code == 200


def test_upvote():
    test_id = '22e47f97-11ca-4c3c-8e77-f3068fddaf6e'
    orig_votes = ''
    before_upvote = requests.get("http://44.238.226.5:80/api/v1/leaderboard/", auth=(username, password))

    op = before_upvote.json()
    for i in op['Items']:
        if i['music_id'] == test_id:
            orig_votes = i['Votes']
            break
    response = requests.post("http://44.238.226.5:80/api/v1/leaderboard/upvote/22e47f97-11ca-4c3c-8e77-f3068fddaf6e",
                             auth=(username, password))

    after_upvote = requests.get("http://44.238.226.5:80/api/v1/leaderboard/", auth=(username, password))
    op2 = after_upvote.json()
    flag = 0
    for i in op2['Items']:
        if i['music_id'] == test_id and i['Votes'] == str(int(orig_votes) + 1):
            assert True
            flag = 1
    if flag == 0:
        assert False
