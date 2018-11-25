# Voice Powered Analytics - Athena Lab

In this lab, we will work with Athena and Lambda. 
The goal of the lab is to use Lambda and Athena to create a solution to query data at rest in s3 and build answers for Alexa. 

## Step 1 - Double check you are running in the same region that the cloudformation was launched

In this section we will use Athena and Lambda. Please make sure as you switch between tabs, that you are still using the same region launched with the cloudformation

## (OPTIONAL) Step 2 -  Understand The Raw Data in S3

This is an optional step of the optional lab. It is intended to give you a better understanding of the data we are using for the lab. 

**NOTE: If you're familiar with S3 and JSON and don't want to inspect the JSON files you can safely skip this step and continue with Step 3 below.** 

Each file in s3 has a collection of JSON objects stored within the file.
In addition, the files have been gziped by [Kinesis Firehose](https://aws.amazon.com/kinesis/firehose/) which saves cost and improves performance.

We will be using a dataset created from Twitter data related to AWS and re:Invent 2018. 
This dataset includes tweets with the #reinvent hashtag or to/from @awsreinvent. 
If you tweet about this workshop now and use the #reinvent hashtag you will be able see that tweet later on in the workshop!
Let's first take a look at the data set we're going to analyze and query.  

### How we get the data into S3
The data is acquired starting with a CloudWatch Event triggering an AWS Lambda function every 5 minutes. Lambda is making calls to Twitter's APIs for data, and then ingesting the data into [Kinesis Firehose](https://aws.amazon.com/kinesis/firehose/).   
Firehose then micro-batches the results into S3 as shown in the following diagram:
![Workshop dataset](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Athena_Arch_1.png)

This dataset is available in the following regions

Region | Bucket
:---: | :---|
EU-WEST-1 | ```s3://aws-vpa-tweets-euw1/```


Amazon Kinesis Firehose delivers the data into S3 as a GZIP file format.
You can use a variety of methods to download one of the files in the dataset. If you use the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) today, this is likely the easiest method to take a look at the data.

**NOTE: The commands below require the installation of the AWS Command Line Interface (CLI).   Click here to [install](https://docs.aws.amazon.com/cli/latest/userguide/installing.html)**
 

List one of the files with (Note use **s3://aws-vpa-tweets-euw1...** for Ireland):
```bash
aws s3 ls s3://aws-vpa-tweets-euw1/tweets/sample/2017/11/06/04/aws-vpa-tweets-sample.gz
```
Download this file to your local directory (Note use **s3://aws-vpa-tweets-euw1...** for Ireland):
```bash
aws s3 cp s3://aws-vpa-tweets-euw1/tweets/sample/2017/11/06/04/aws-vpa-tweets-sample.gz .
```

Since the files are compressed, you will need to unzip it. In addition the data is stored in raw text form. Make sure you rename the file to either *.json or *.text.
The data format look like this:
```json
{  
	"id": 914642318044655600,  
	"text": "Two months until #reInvent! Check out the session calendar & prepare for reserved seating on Oct. 19! http://amzn.to/2fxlVg7  ",  
	"created": "2017-10-02 00:04:56",  
	"screen_name": " AWSReinvent ",  
	"screen_name_followers_count": 49864,  
	"place": "none",  
	"country": "none",  
	"retweet_count": 7,  
	"favorite_count": 21
}
```

## Step 3 - Create an Athena table

We need to create a table in Amazon Athena. This will allow us to query the data at rest in S3. 
The twitter data is stored as JSON documents and then compressed in s3. 
Athena supports reading of gzip files and includes json SerDe's to make parsing the data easy.

There is no need to copy the dataset to a new bucket for the workshop. 
The data is publicly available in the bucket we provide.   

**Create Athena table**

1. Please make sure you are **Ireland region**
1. In your AWS account navigate to the **Athena** service
1. In the top left menu, choose *Query Editor*
1. Use this code to create the Athena table. Once added, click **Run Query**

```SQL
CREATE EXTERNAL TABLE IF NOT EXISTS default.tweets(
  id bigint COMMENT 'Tweet ID', 
  text string COMMENT 'Tweet text', 
  created timestamp COMMENT 'Tweet create timestamp', 
  screen_name string COMMENT 'Tweet screen_name',
  screen_name_followers_count int COMMENT 'Tweet screen_name follower count',
  place string COMMENT 'Location full name',
  country string COMMENT 'Location country',
  retweet_count int COMMENT 'Retweet count', 
  favorite_count int COMMENT 'Favorite count')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
WITH SERDEPROPERTIES ( 
  'paths'='id,text,created,screen_name,screen_name_followers_count,place_fullname,country,retweet_count,favorite_count') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://aws-vpa-tweets-euw1/tweets/'
```

**We need to produce an integer for our Alexa skill. To do that we need to create a query that will return our desired count** 
1. You'll see an Athena table called *tweets* in the *default* database (You may have to hit refresh).
1. If you click on the *tweets* table, you can see the fields that we saw earlier.    
1. Here's an example SQL `SELECT` Query statement that can be run (clear the previous statement):

```SQL
SELECT COUNT(*) AS TOTAL_TWEETS FROM tweets;
```
The statement above shows the total amount of tweets in our data set. 
**Note** The result should be in the 1000's. If you got a tiny number, something is wrong. 
Recreate your table or ask one of the lab assistants for help.

If you are happy with the value returned by your query you can move to **Step 4**, or if you're a SQL guru (or just curious what other queries that you can come up with), you can experiment with other queries with Athena . 

The Athena syntax is widely compatible with Presto. You can learn more about it from our [Amazon Athena Getting Started](http://docs.aws.amazon.com/athena/latest/ug/getting-started.html) and the [Presto Docs](https://prestodb.io/docs/current/) web sites
 
**Bonus: What other interesting SQL insights can you create in Athena?**
 
**Tweet @WestrichAdam** with link to additional query insights that you captured from this data. It may be added below to our ***Voice Powered Analytics** Additional Queries Attendee Submissions*

<details>
<summary><strong>OPTIONAL - Try out a few additional queries (and Attendee Submissions).</strong></summary><p>

```SQL
--Total number of tweets
SELECT COUNT(*) FROM tweets

--Total number of tweets in last 3 hours
SELECT COUNT(*) FROM tweets WHERE created > now() - interval '3' hour

--Total number of tweets by user chadneal
SELECT COUNT(*) FROM tweets WHERE screen_name LIKE '%chadneal%'

--Total number of tweets that mention AWSreInvent
SELECT COUNT(*) FROM tweets WHERE text LIKE '%AWSreInvent%'

** Attendee Submissions **
-- Submitted by Patrick (@imapokesfan) 11/29/17:
SELECT screen_name as tweeters,text as the_tweet
from default.tweets
where text like '#imwithslalom%'
group by screen_name, text

-- Submitted by Cameron Pope (@theaboutbox) 11/29/17:
SELECT count(*) from tweets where text like '%excited%'

```
</details>

## Step 4 - Create a lambda to query Athena

In this step we will create a **Lambda function** that runs every 5 minutes. The lambda code is provided but please take the time to review the function.

1. Go to the [AWS Lambda console page](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions)
1. Make sure you are in the same region as the initial CloudFormation deployment
1. Click **Create Function** 
1. We will skip using a blueprint to get started and author one from scratch. Click **Author one from scratch** 
1. Under name add **vpa_lambda_athena_poller**
1. For Runtime, select **Python 3.6**
1. Under Role leave the default value of **Choose an existing role**
1. Under existing role, select **VPALambdaAthenaPollerRole**
1. Click **Create Function** 

<details>
<summary><strong>Watch how to create the function</strong></summary><p>

**Watch how to create the function**
![Watch how to create a function](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_lab_lambda-create-function.gif)

</details>


### Function Code

1. For Handler, ensure that it is set to: **lambda_function.lambda_handler**
1. Select inline code and then use the code below

*NOTE: the code below will be querying Athena with the SQL statement that you defined above every 5 minutes (from our Cloudwatch Event trigger). It then inserts into DynamoDB so it can be available for low latency voice retrieval in the next module*

```Python
import boto3
import csv
import time
import os
import logging
from urllib.parse import urlparse

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# These ENV are expected to be defined on the lambda itself:
# vpa_athena_database, vpa_ddb_table, vpa_metric_name, vpa_athena_query, region, vpa_s3_output_location

# Responds to lambda event trigger
def lambda_handler(event, context):
    vpa_athena_query = os.environ['vpa_athena_query']
    athena_result = run_athena_query(vpa_athena_query, os.environ['vpa_athena_database'],
                                     os.environ['vpa_s3_output_location'])
    upsert_into_DDB(str.upper(os.environ['vpa_metric_name']), athena_result, context)
    logger.info("{0} reinvent tweets so far!".format(athena_result))
    return {'message': "{0} reinvent tweets so far!".format(athena_result)}


# Runs athena query, open results file at specific s3 location and returns result
def run_athena_query(query, database, s3_output_location):
    athena_client = boto3.client('athena', region_name=os.environ['region'])
    s3_client = boto3.client('s3', region_name=os.environ['region'])
    queryrunning = 0

    # Kickoff the Athena query
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
    logger.info('Execution ID: ' + response['QueryExecutionId'])

    # wait for query to finish.
    while queryrunning == 0:
        time.sleep(2)
        status = athena_client.get_query_execution(QueryExecutionId=response['QueryExecutionId'])
        results_file = status["QueryExecution"]["ResultConfiguration"]["OutputLocation"]
        if status["QueryExecution"]["Status"]["State"] != "RUNNING":
            queryrunning = 1

    # parse the s3 URL and find the bucket name and key name
    s3url = urlparse(results_file)
    s3_bucket = s3url.netloc
    s3_key = s3url.path

    # download the result from s3
    s3_client.download_file(s3_bucket, s3_key[1:], "/tmp/results.csv")

    # Parse file and update the data to DynamoDB
    # This example will only have one record per petric so always grabbing 0
    metric_value = 0
    with open("/tmp/results.csv", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            metric_value = row['_col0']

    os.remove("/tmp/results.csv")
    return metric_value


# Save result to DDB for fast access from Alexa/Lambda
def upsert_into_DDB(nm, value, context):
    region = os.environ['region']
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(os.environ['vpa_ddb_table'])
    try:
        response = table.put_item(
            Item={
                'metric': nm,
                'value': value
            }
        )
        return 0
    except Exception:
        logger.error("ERROR: Failed to write metric to DDB")
        return 1

```

<details>
<summary><strong>Watch how to update the function code, execution role, and basic settings</strong></summary><p>

![Watch how to update the function](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_lab_lambda-code-role.gif)

</details>


### Environment variables

You will need the S3 bucket name you selected from the CloudFormation template. 
If you forgot the name of your bucket you can locate the name on the output tab of the CloudFormation stack.

![S3 Bucket Name on CloudFormation Outputs Tab](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/vpa-s3-buckename.png)

1. Set the following Environment variables:

*Note: It's a lambda best practice to separate configuration from your code into the Environment variables section.  Below you'll see our AWS Region, Athena database, Athena query, S3 output bucket (results from the athena query), and the DynamoDB table where we'll be writing the results for low latency voice retrieval*  

```
vpa_athena_database = tweets
vpa_ddb_table = VPA_Metrics_Table
vpa_metric_name = Reinvent Twitter Sentiment
vpa_athena_query = SELECT count(*) FROM default."tweets"
region = eu-west-1
vpa_s3_output_location = s3://<your_s3_bucket_name>/poller/
```

<details>
<summary><strong>Screenshot of the Lambda env's - note use your bucket name</strong></summary><p>

![Lambda env](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/vpa-lambda-env.png)


</details>

### Basic Settings

1. Set the timeout to 2 min


### Triggers Pane

We will use a CloudWatch Event Rule created from the CloudFormation template to trigger this Lambda. 
Scroll up to the top of the screen in the **Designers** section and select the pane **Triggers**. 

1. Under the **Add trigger**, click the empty box icon, followed by **CloudWatch Events**
1. Scroll down, and under *Rule*, select **VPAEvery5Min**
1. Leave the box checked for **Enable trigger**
1. Click the **Add** button, then scroll up and click **Save** (the Lambda function)

<details>
<summary><strong>Watch how to update the trigger</strong></summary><p>

![Watch how to update the trigger](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_lab_CWE_1.gif)

</details>


## Step 4 - Create a test event and test the Lambda

At this point we are ready to test the Lambda. Before doing that we have to create a test event. 
Lambda provides many test events, and provides for the ability to create our own event. 
In this case, we will use the standard CloudWatch Event.

### To create the test event

1. In the upper right, next to test, select **Configure test events**
1. Select **Create new test event**
1. Select **Amazon Cloudwatch** for the event template
1. Type **VPASampleEvent** for the event name
1. Click **Create** in the bottom right of the window

<details>
<summary><strong>Watch how to configure a test event</strong></summary><p>

![Watch how to configure a test event](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/vpa-lambda-test-cwe.gif)

</details>


### Now we should test the Lambda. 

1. Click **test** in the upper right
1. Once the run has completed, click on the **Details** link to see how many reinvent tweets are stored in s3.

Note, there should be > 10,000 tweets. If you get a number lower than this please ask a lab assistant for help.

<details>
<summary><strong>Watch how to test the lambda</strong></summary><p>

![Watch how to test the lambda](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/vpa-lambda-test-run.gif)

</details>

## Start working on the Alexa skill

You are now ready to build the Alexa skill, you can get started here [Amazon Alexa Section](README-Alexav2.md)
