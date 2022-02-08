# OpenSearch-Example

s3 to OpenSearch demo

s3-to-Opensearch2.py can upload a s3 object file to OpenSearch.

1、setup cloud9 , using aws configure to set the AK and SK

2、Grant the user with role to use OpenSearch

3、config the OpenSearch security group , grant the cloud9 or ec2 to send traffic in

4、config the OpenSearch Access Policy to Grant the user 

5、upload the s3-to-Opensearch2.py to cloud9

pip install boto3

pip install opensearch-py

pip install requests

pip install requests-aws4auth

modify s3-to-Opensearch2.py input parameters including 

endpoint = '***.ap-southeast-1.es.amazonaws.com'  # the proxy endpoint, including https://
region = 'ap-southeast-1'  # e.g. us-west-1
index = '***'  # index name
bucketName = "***"  #s3 bucket
objectKey = "news/sample.json"   #s3 object

6、run the python script

