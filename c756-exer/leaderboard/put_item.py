import boto3


def put_music( music_id,artist,SongTitle,upvotes,genre ,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Leaderboard')
    response = table.put_item(
       Item={
            'music_id': music_id,
            'info': {
                'Artist': artist,
                'SongTitle': SongTitle,
                'upvotes': upvotes,
                'genre': genre
            }
            
        }
    )
    return response


if __name__ == '__main__':
    movie_resp = put_music(1, "Glass Animals","Heat Waves","60","electric")
    print("Put movie succeeded:")
 