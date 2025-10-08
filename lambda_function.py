import json
import boto3

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Employees')

def lambda_handler(event, context):
    try:
        method = event.get('httpMethod')
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}
        response = {}

        if method == 'POST':
            emp_id = body.get('id')
            if not emp_id:
                return {'statusCode': 400, 'body': json.dumps({'error': 'Missing id'})}

            required_fields = ['name', 'department', 'designation', 'email', 'salary']
            for field in required_fields:
                if field not in body:
                    return {'statusCode': 400, 'body': json.dumps({'error': f'Missing {field}'})}

            item = {
                'id': emp_id,
                'name': body['name'],
                'department': body['department'],
                'designation': body['designation'],
                'email': body['email'],
                'salary': body['salary']
            }
            table.put_item(Item=item)
            response = {'message': 'Employee added', 'id': emp_id}


        elif method == 'GET':
            emp_id = None
            if event and 'queryStringParameters' in event and event['queryStringParameters']:
                emp_id = event['queryStringParameters'].get('id')

            if emp_id:
                result = table.get_item(Key={'id': emp_id})
                response = result.get('Item', {'error': 'Employee not found'})
            else:
                scan_result = table.scan()
                response = scan_result.get('Items', [])

        elif method == 'PUT':
            emp_id = body.get('id')
            if not emp_id:
                return {'statusCode': 400, 'body': json.dumps({'error': 'Missing id'})}

            update_expr = "SET "
            expr_values = {}
            expr_names = {}

            for k, v in body.items():
                if k != 'id':
                    update_expr += f"#{k} = :{k}, "
                    expr_values[f":{k}"] = v
                    expr_names[f"#{k}"] = k  # alias for reserved names

            update_expr = update_expr.rstrip(", ")

            if not expr_values:
                return {'statusCode': 400, 'body': json.dumps({'error': 'No fields to update'})}

            table.update_item(
                Key={'id': emp_id},
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expr_values,
                ExpressionAttributeNames=expr_names
            )
            response = {'message': 'Employee updated'}

        elif method == 'DELETE':
            emp_id = None
            if event and 'queryStringParameters' in event and event['queryStringParameters']:
                emp_id = event['queryStringParameters'].get('id')

            if not emp_id:
                return {'statusCode': 400, 'body': json.dumps({'error': 'Missing id in query parameter'})}

            table.delete_item(Key={'id': emp_id})
            response = {'message': 'Employee deleted'}

        else:
            response = {'error': 'Unsupported method'}

        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
