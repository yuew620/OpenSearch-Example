import boto3
import re
import requests
import json
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection

#input these parameters
endpoint = '***.ap-southeast-1.es.amazonaws.com'  # the proxy endpoint, including https://
region = 'ap-southeast-1'  # e.g. us-west-1
index = 'log-wy'  # index name
bucketName = "***"  # s3 bucket name
objectKey = "news/sample.json"  # s3 object

service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                   region, service, session_token=credentials.token)
print(credentials.access_key)
print(credentials.secret_key)
print(credentials.token)
# url = endpoint + '/' + index + '/_doc'
# headers = {"Content-Type": "application/json"
#           }
s3 = boto3.client('s3')
search = OpenSearch(
    hosts=[{'host': endpoint, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

eventDemo = {
    "Records": [
        {
            "eventVersion": "2.1",
            "eventSource": "aws:s3",
            "awsRegion": "ap-east-2",
            "eventTime": "2019-09-03T19:37:27.192Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {
                "principalId": "AWS:AIDAINPONIXQXHT3IKHL2"
            },
            "requestParameters": {
                "sourceIPAddress": "205.255.255.255"
            },
            "responseElements": {
                "x-amz-request-id": "D82B88E5F771F645",
                "x-amz-id-2": "vlR7PnpV2Ce81l0PRw6jlUpck7Jo5ZsQjryTjKlc5aLWGVHPZLj5NeC6qMa0emYBDXOo6QBU0Wo="
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "828aa6fc-f7b5-4305-8584-487c791949c1",
                "bucket": {
                    "name": bucketName,
                    "ownerIdentity": {
                        "principalId": "A3I5XTEXAMAI3E"
                    },
                    "arn": "arn:aws:s3:::lambda-artifacts-deafc19498e3f2df"
                },
                "object": {
                    "key": objectKey,
                    "size": 1305107,
                    "eTag": "b21b84d653bb07b05b1e6b33684dc11b",
                    "sequencer": "0C0F6F405D6ED209E1"
                }
            }
        }
    ]
}
contextDemo = ""

documentDemo = {
    "title": "Moneyball",
    "director": "Bennett Miller",
    "year": "2011"
}

#simple test
#search.index(index="movies", doc_type="_doc", id="1", body=documentDemo)

# Lambda execution starts here
def handler(event, context):
    for record in event['Records']:
        # Get the bucket name and key for the new file
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        # Get, read, and split the file into lines
        obj = s3.get_object(Bucket=bucket, Key=key)
        body = obj['Body'].read()
        lines = body.splitlines()
        idNum = 0
        for line in lines:
            # document = json.loads(line)
            document = line
            idNum = idNum + 1;
            print(document)
            if document.strip():
                print("start")
                r = search.index(index="log-wy", doc_type="_doc", id=idNum, body=document)
                # r = requests.post(url, auth=awsauth, json=document, headers=headers)
                print(r)


handler(eventDemo, contextDemo)


print(search.get(index="log-wy", doc_type="_doc", id="1"))
print(search.get(index="log-wy", doc_type="_doc", id="2"))
print(search.get(index="log-wy", doc_type="_doc", id="3"))
print(search.get(index="log-wy", doc_type="_doc", id="4"))