import json
import uuid
import boto3
from urllib.parse import parse_qs

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('task_list')

def handler(event, context):
    http_method = event['httpMethod']
    
    if http_method == 'GET':
        return handle_get(event, context)
    elif http_method == 'POST':
        return handle_post(event, context)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'message': 'Method Not Allowed'})
        }

def handle_get(event, context):
    try:
        # Retrieve all items from the DynamoDB table
        response = table.scan()
        items = response['Items']
        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def handle_post(event, context):
    try:
        # Parse form data from event body
        body = parse_qs(event['body'])
        # Assuming form data contains 'task_name' and 'deadline' fields
        task_date = body['task_date'][0]
        task_name = body['task_name'][0]
        due_date = body['due_date'][0]
        description = body['description'][0]
        
        
        # Add item to DynamoDB table
        response = table.put_item(Item={'task_id': str(uuid.uuid4()),'task_date': task_date, 'task_name': task_name, 'due_date': due_date, 'description': description})
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Item added successfully'})
        }
    except Exception as e:
        # Handle exception
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
