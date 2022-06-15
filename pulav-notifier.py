import requests
import re
import json
import boto3

def findPulav():

    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    
    page = requests.get("https://www.santhiskitchens.com/menu", headers=headers).text
    
    return re.search(r'\bPulavs\b', page)

def lambda_handler(event, context):
    
    client = boto3.client('sns')
    snsArn = 'arn:aws:sns:us-east-2:account_number_redacted:PulavNotifier'
    message = "https://www.santhiskitchens.com/menu/"
    
    if findPulav():
        
        status = "available"
        statusCode = 200
    
        response = client.publish(
            TopicArn = snsArn,
            Message = message ,
            Subject='Pulav is available today'
        )
        
    else:
        status = "unavailable"
        statusCode = 404

    return {
        'statusCode': statusCode,
        'body': status
    }