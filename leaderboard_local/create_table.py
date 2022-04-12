import boto3
import uuid
import pandas as pd
from put_item import put_music


def create_leader_table(dynamodb=None):
    """
    Create the table in dynamo db with the given schema
    """
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='Leaderboard',
        KeySchema=[
            {
                'AttributeName': 'music_id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'music_id',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


def load_data(df):
    """
    Dumping the default data in DB
    """
    for i in range(df.shape[0]):
        temp = df.iloc[i]
        id = str(uuid.uuid4())
        artist = temp['Artist']
        song = temp['SongTitle']
        upvotes = int(temp['upvotes'])
        genre = temp['genre']
        put_music(id, artist, song, upvotes, genre)


if __name__ == '__main__':
    df = pd.read_csv("top10.csv")
    leader_table = create_leader_table()
    print("Table status:", leader_table.table_status)
    load_data(df)
    print("Table status: Loaded data")
