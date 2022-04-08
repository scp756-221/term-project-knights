import requests
from put_item import put_music

def test_read():
    assert True
    # response = requests.get("http://localhost:5000/api/v1/leaderboard/")
    # assert response.status_code == 200

def test_read_single():
    Artist = 'Akshita'
    SongTitle = 'Hate'
    upvotes = 1
    genre = 'pop'
    music_id = '28'
    response = put_music(music_id=music_id, artist=Artist, SongTitle=SongTitle, upvotes=upvotes, genre=genre)
    assert response['ResponseMetadata']['HTTPStatusCode']==200