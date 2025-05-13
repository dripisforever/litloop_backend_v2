import boto3
import json
from celery import shared_task

sqs = boto3.client('sqs', region_name='your-region')
QUEUE_URL = 'https://sqs.eu-north-1.amazonaws.com/911167897535/litloop-queue-s3'

@shared_task
def poll_s3_events():
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=10
    )

    for msg in response.get('Messages', []):
        body = json.loads(msg['Body'])
        s3_event = json.loads(body['Message']) if 'Message' in body else body
        # Handle event (e.g., file name = s3_event['Records'][0]['s3']['object']['key'])
        print("Got S3 event:", s3_event)

        # IMPORTANT PART
        # IMPORTANT PART
        # IMPORTANT PART
        # IMPORTANT PART
        # IMPORTANT PART
        launch_spot_task.delay(video_s3_url=video_s3_url)

        # Delete message after processing
        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=msg['ReceiptHandle']
        )
