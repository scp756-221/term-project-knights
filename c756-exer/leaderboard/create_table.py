import boto3


def create_leader_table(dynamodb=None):
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
                'AttributeType': 'N'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table




if __name__ == '__main__':
    leader_table = create_leader_table()
    print("Table status:", leader_table.table_status)
