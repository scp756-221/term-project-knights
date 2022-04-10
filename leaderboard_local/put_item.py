import boto3
import os

access_key = 'djnasdaskj'
secret_access_key = 'djasndaadsj'
region = os.getenv('AWS_REGION', 'us-west-2')

def put_music( music_id,artist,SongTitle,upvotes,genre ,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url='http://localhost:8000',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key)

    table = dynamodb.Table('Leaderboard')
    response = table.put_item(
       Item={
            'music_id': music_id,
            'Artist': artist,
            'SongTitle': SongTitle,
            'upvotes': upvotes,
            'genre': genre
            
        }
    )
    return response


if __name__ == '__main__':
    movie_resp = put_music(1, "Glass Animals","Heat Waves","60","electric")
    print("Put movie succeeded:")
 