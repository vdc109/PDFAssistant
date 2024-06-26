import boto3

# dynamodb = boto3.resource('dynamodb',
#                     aws_access_key_id=ACCESS_KEY_ID,
#                     aws_secret_access_key=ACCESS_SECRET_KEY,
#                     aws_session_token=AWS_SESSION_TOKEN)

#dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='userdata',
    KeySchema=[
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        }
         
    ],
    AttributeDefinitions=[
             {
            'AttributeName': 'email',
            'AttributeType': 'S'
        } 
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='userdata')

# Print out some data about the table.
print(table.item_count)
