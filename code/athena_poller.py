import boto3
import csv
import time
import os
from urllib.parse import urlparse


def lambda_handler(event, context):
    query = os.environ['query']
    indexEndRegion = context.invoked_function_arn[15:30].find(":")+15
    region = context.invoked_function_arn[15:indexEndRegion]
    result = run_athena_query(query, os.environ['database'], os.environ['s3_output_location'],region)
    upsert_into_DDB(os.environ['Metric_Name'], result, context,region)
    return {'message': "{0} reinvent tweets so far!".format(result)}


# runs athena query, open results file at specific s3 location and returns result
def run_athena_query(query, database, s3_output_location,region):
    athena_client = boto3.client('athena', region_name=region])
    s3_client = boto3.client('s3', region_name=region])
    queryrunning = 0

    #  kickoff the Athena query
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': database
        },
        ResultConfiguration={
            'OutputLocation': s3_output_location
        }
    )

    # Log the query execution id
    print('Execution ID: ' + response['QueryExecutionId'])

    # wait for query to finish.
    while (queryrunning == 0):
        time.sleep(2)
        status = athena_client.get_query_execution(QueryExecutionId=response['QueryExecutionId'])
        results_file = status["QueryExecution"]["ResultConfiguration"]["OutputLocation"]
        if (status["QueryExecution"]["Status"]["State"] != "RUNNING"):
            queryrunning = 1

    # parse the s3 URL and find the bucket name and key name
    s3url = urlparse(results_file)
    s3_bucket = s3url.netloc
    s3_key = s3url.path
    print(s3_key)

    # download the result from s3
    s3_client.download_file(s3_bucket, s3_key[1:], "/tmp/results.csv")

    # parse file and update the data to DynamoDB
    with open("/tmp/results.csv", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row[os.environ['resultCol']])
            return row[os.environ['resultCol']]  # return result


def upsert_into_DDB(nm, value, context,region):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(os.environ['DDB_Table'])
    try:
        response = table.put_item(
            Item={
                'metric': UPPER(nm),
                'value': value
            }
        )
        return 0
    except Exception:
        print(str(e))
        return 1
