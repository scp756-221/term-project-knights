import unittest
import requests

class TestStringMethods(unittest.TestCase):
    def test_read(self):
        response = requests.get("http://localhost:5000/api/v1/leaderboard/")
        assert response.status_code == 200

    def test_read_single(self):
        response = requests.get("http://localhost:5000/api/v1/leaderboard/33dc8408-be2b-410b-b12a-f48efdb6f15f")
        assert response.json()['Item'] == {'Artist': 'Ed Sheeran', 'SongTitle': 'Shivers', 'genre': 'pop', 'music_id': '33dc8408-be2b-410b-b12a-f48efdb6f15f', 'upvotes': '26'}


if __name__ == '__main__':
    unittest.main()