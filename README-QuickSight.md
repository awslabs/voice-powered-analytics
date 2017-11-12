##**Note that this workshop is not yet live.  It will be live at reinvent 2017 Wednesday 11/29**

# Voice Powered Analytics - QuickSight Lab (OPTIONAL)

In this lab we will use QuickSight to explore our dataset and visualize a few interesting metrics of the twitter dataset. 

**NOTE** The QuickSight Lab is optional. Exploring the dataset is an extremely helpful process however the rest of the workshop does not depend on the QuickSight Lab. If you are already familiar with QuickSight please feel free to skip to the [Athena Setion](README-Athena.md)

### Step 1 - (OPTIONAL) Understand Raw Data Set To Query

This is an optional step of the optional lab! It is intended to give you a better understanding of the data we are using for the lab. If you don't want to inspect the JSON files and trust that each file in s3 has a collection of JSON objects in the file, and that the file has been correctly gziped by [Kinesis FIrehose](https://aws.amazon.com/kinesis/firehose/), you can skip this section and continue with [Step 2](#step-2)

We will be using a dataset created from Twitter data related to AWS re:Invent 2017. In short, this dataset includes tweets with the #reinvent hashtag or to/from @awsreinvent. In fact you if you tweet about this workshop now and use the #reinvent hashtag you will be able see that tweet later on in the workshop!
Let's first take a look at the data set we're going to analyze and query.  

### How we get the data into S3
The data is acquired starting with a CloudWatch Event triggering an AWS Lambda function every 5 minutes. Lambda is making calls to Twitter's APIs for data, and then ingesting the data into [Kinesis FIrehose](https://aws.amazon.com/kinesis/firehose/).   
Firehose then micro-batches the results into S3 as shown in the following diagram:
![Workshop dataset](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Athena_Arch_1.png)

This dataset is available in the following regions
Region | Bucket
:---: | :---|
US-EAST-1 | s3://aws-vpa-tweets/
EU-WEST-1 | s3://aws-vpa-tweets-euw1/


Amazon Kinesis Firehose delivers the data into S3 as a GZIP file format.
You can use a variety of methods to download one of the files in the dataset. If you use the AWS CLI today, this is likely the easiest method to take a look at the data.

An example would be 

1. Download a sample extract of the data at the following [File Location](https://s3.amazonaws.com/aws-vpa-tweets/tweets/2017/11/06/03/aws-vpa-tweets-1-2017-11-06-03-53-28-b055a510-f718-4207-8e48-05c3ad8c3a5d.gz)
2. Using the [AWS CLI](https://aws.amazon.com/cli/)
3. Using a 3rd party S3 File Explorer such as [Cloudberry Explorer](https://www.cloudberrylab.com/explorer/amazon-s3.aspx)  



<details>
<summary><strong>Full solution - Explore the Twitter Data Using AWS CLI</strong></summary><p>
When using the AWS CLI, you can run the following commands to see the folder/prefix structure of the data.  Firehose delivers the data in micro-batches by time.  When navigating to the file itself, it is in the GZIP file format:

```bash
$ aws s3 ls s3://aws-vpa-tweets-euw1/
         PRE tweets/
$ aws s3 ls s3://aws-vpa-tweets-euw1/tweets/
         PRE 2017/
$ aws s3 ls s3://aws-vpa-tweets-euw1/tweets/2017/
         PRE 10/
         PRE 11/
$ aws s3 ls s3://aws-vpa-tweets-euw1/tweets/2017/11/
         PRE 01/
         PRE 02/
         PRE 03/
         PRE 04/
         PRE 05/
         PRE 06/
$ aws s3 ls s3://aws-vpa-tweets-euw1/tweets/2017/11/06/
         PRE 00/
         PRE 01/
         PRE 02/
         PRE 03/
         PRE 04/
$ aws s3 ls s3://aws-vpa-tweets-euw1/tweets/2017/11/06/04/
2017-11-05 20:09:30        270 aws-vpa-tweets-1-2017-11-06-04-08-28-f5542a86-818d-4b7a-8d84-aaff9ea4bec9.gz
```
Let's download the file by copying it locally and then using our favorite editor to open it:
``` bash
$ aws s3 cp s3://aws-vpa-tweets-euw1/tweets/2017/11/06/04/aws-vpa-tweets-1-2017-11-06-04-08-28-f5542a86-818d-4b7a-8d84-aaff9ea4bec9.gz .
download: s3://aws-vpa-tweets-euw1/tweets/2017/11/06/04/aws-vpa-tweets-1-2017-11-06-04-08-28-f5542a86-818d-4b7a-8d84-aaff9ea4bec9.gz to ./aws-vpa-tweets-1-2017-11-06-04-08-28-f5542a86-818d-4b7a-8d84-aaff9ea4bec9.gz
$ vi aws-vpa-tweets-1-2017-11-06-04-08-28-f5542a86-818d-4b7a-8d84-aaff9ea4bec9.gz 
```
The data format looks something like this:
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
In the next section, we're going to use these fields to create HIVE external tables in AWS Athena and query the data directly in S3.
</details>

### Step 2 - Create an Athena table for Initial Data Discovery

Now we're comfortable with the dataset, let's create a table in Athena on top of this data.  There is no need to copy the dataset to a new bucket for the workshop. The data is publicly available. You will however need to create an Athena database and table to query the data. The twitter data is compressed in s3, but in a JSON syntax which Athena has native support for. 

<details>
<summary><strong>Full solution - Create Athena table (expand for details)</strong></summary><p>

1. In your AWS account navigate to the **Athena** service
2. In the top left menu, choose *Query Editor*.
3. To create a new table, use this code to create the [HIVE external table](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-CreateTable) Data Definition Language (DDL):

```SQL
CREATE EXTERNAL TABLE tweets(
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
4. Then hit the *Run Query* button
5. In a few seconds, you'll see an Athena table called *tweets* in the *default* database (You may have to hit refresh).
6. If you click on the *tweets* table, you can see the fields that are in our raw S3 data.    
7. Let's test that the tweets table works.  In the same Query Editor run the following `SELECT` statement (clear the previous statement):

```SQL
SELECT COUNT(*) AS TOTAL_TWEETS FROM tweets;
```
The statement above shows the total amount of tweets in our data set (result value should be well over 8k).  
</p></details>

<details>
<summary><strong>Partial solution - Create Athena table using Glue(expand for details)</strong></summary><p>

TODO: Use AWS Glue to discover and build a DDL.

</p></details>

### Step 3 - Explore the data using Quicksight
We've created an Athena table directly on top of our S3 Twitter data, let's explore some insights on the data.  While this can be achieved through Athena itself or compatible query engines, Amazon Quicksight enables you to connect directly to Athena and quickly visualize it into charts and graphs without writing any SQL code.  Let's explore:      
<details>
<summary><strong>Full solution - Explore Athena data in Quicksight</strong></summary><p>

1. Launch the [QuickSight portal](https://eu-west-1.quicksight.aws.amazon.com/).  This may ask you to register your email address for Quicksight access.  
1. If haven't already configured, Quicksight may need special permissions to access Athena:   
a. (These settings can only be changed in the N.Virginia region) In the upper right corner, ensure US East N. Virginia is selected, then to the right of the *region* in the upper right corner, choose your profile name, and from the dropdown menu, choose *Manage Quicksight*.  
b. On the left menu, click *Account Settings*<br>
c. Click the *Edit AWS permissions* button<br>
d. Ensure the box *Amazon Athena* is checked, then click *Apply*
1. In the main Quicksight portal page (ensure you're in the EU Ireland Region)
1. In the upper right choose your  **Manage data**
1. Now in the upper left choose **New data set**
1. You will see tiles for each of the QuickSight supported data sources. From this page select the **Athena** tile. 
1. When asked for the dataset name you can choose anything you like, for our example we use **tweets-dataset** You can choose to validate that SSL will be used for data between Athena and QuickSight. Finish be selecting **Create data source**
1. Now we need to choose the Athena table we created in **Step 1**. For our example we used the **Default** database, with a table name of **tweets**. Finish by clicking on **Select**. 
1. You will now be asked if you want to use spice or direct query access. If in the Ireland region, choose direct query access (SPICE is not yet available in this region).  Click **Visualize** when done. 
1. QuickSight will now import the data. Wait until you see **Import Complete**. Then close the summary window. 
1. Add the **created** field from the Athena table by dragging it from the Field list to the empty AutoGraph window.
1. From the *Visual types* in the botom left corner, select **Vertical bar chart**
1. Add another Visual by selecting in the top left corner, the **+ Add** button  and then **Add visual**
1. On this new graph, lets add the **country** field. 
1. As you can see, lots of tweets do not include which country the tweet was created in. Lets filter these results out. Click on the large bar labeled **none**, then select **exclude "none"** from the pop up window. As you can see the tweets without a location were excluded.
1. Lets change the visual from a bar chart to a pie chart. Select the entire visual, then from the bottom right select the **pie chart** visual.  Add **Group By: "none"**

</p></details>

**Bonus: What other interesting insights can you find from this data in Quicksight**


### Step 4 - Create a query to find the number of reinvent tweets 



<details>
<summary><strong>Full solution - Athena Query (expand for details)</strong></summary><p>

1. We need to produce an integer for our Alexa skill. To do that we need to create a query that will return our desired count.
1. To find the last set of queries from Quicksight, go to the Athena AWS Console page, then select *History* on the top menu.
1. You can see the latest queries under the column *Query* (starting with the word 'SELECT').  You can copy these queries to a text editor to save later.  
1. We'll be running these queries in the *Query Editor*. Navigate there in the top Athena menu.  
1. Ensure that the **default** database is selected and you'll see our *tweets* table.  
1. The Athena syntax is widely compatable with Presto. You can learn more about it from our [Amazon Athena Getting Started](http://docs.aws.amazon.com/athena/latest/ug/getting-started.html) and the [Presto Docs](https://prestodb.io/docs/current/) web sites
1. Once you are happy with the value returned by your query you can move to **Step 4**, otherwise you can experiment with other query types. 
1. Let's write a new query, there are several ways that you can do this:<br>
a. Use one of the queries that we had selected from the *Query Editor*<br>
b. Write a new query using the [Presto SELECT format](https://prestodb.io/docs/current/sql/select.html) Hint: The Query text to find the number of #reinvent tweets is:  `SELECT COUNT(*) FROM tweets`<br>
**TODO Show advanced query building techniques for our dataset**<br>
c. Use or build off one of th examples below:
</details>
<details>
<summary><strong>A few examples of other queries are listed below.</strong></summary><p>

```SQL
--Total number of tweets
SELECT COUNT(*) FROM tweets

--Total number of tweets in last 3 hours
SELECT COUNT(*) FROM tweets WHERE created > now() - interval '3' hour

--Total number of tweets by user chadneal
SELECT COUNT(*) FROM tweets WHERE screen_name LIKE '%chadneal%'

--Total number of tweets that mention AWSreInvent
SELECT COUNT(*) FROM tweets WHERE text LIKE '%AWSreInvent%'

```
</details>

### Step 5 - Create a lambda to query Athena

In this step we will create a **Lambda function** that runs every 5 minutes. The lambda code is provided but please take the time to review the function.

#### Run the setup CloudFormation template

We have created a CloudFormation template to create the IAM roles, IAM Policies, DynamoDB table, and s3 bucket needed for this workshop.
The template can be found in `code/setup/vpa_setup.yaml` or [on Github](https://github.com/awslabs/voice-powered-analytics/blob/master/code/setup/vpa_setup.yaml)

Before we create the Lambda function, we need to retrieve the bucket where Athena will be delivering the results in our local account.  We can retrieve this by going to the **Athena** service in the AWS console, then clicking *Settings* in the top right Athena menu.  From the dialog, let's copy the value in the *Query result location* (beginning with 's3://') to a local text editor to save for later.
<details>
<summary><strong>Full Solution - Create the lambda to query Athena</strong></summary><p>

1. Go to the [AWS Lambda console page](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions)
2. Click **Create Function** 
3. We will skip using a blueprint to get started and author one from scratch. Click **Author one from scratch** 
4. Leave the trigger blank for now. Click **Next** without adding a trigger from the Configure triggers page.
5. Give your Lambda function a unique name. For example you can use **vpa_lambda_athena** for the query name. For runtime select **Python 3.6**
6. Add a role.  Under role, *Choose an existing role*, and in the box below, choose the role named *VPALambdaAthenaPoller*
7. Click *Create function*
8. Select inline code and then use the:

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
    upsert_into_DDB(os.environ['vpa_metric_name'], athena_result, context)
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

1. Add the role to the Lambda function: VPALambdaAthenaPoller
1. Set the following Environment variables:

```
vpa_athena_database = tweets
vpa_ddb_table = VPA_Metrics_Table
vpa_metric_name = Reinvent Twitter Sentiment
vpa_athena_query = SELECT count(*) FROM default."tweets"
region = eu-west-1
vpa_s3_output_location = s3://<your_s3_bucket_name>/poller/
```
Note: for vpa_s3_output_location, use the Athena s3 location from the output of the setup CloudFormation template.  
1. From the **Lambda function handler and role** ensure the Handler is set to `lambda_function.lambda_handler` and the Existing role to `VPALambdaAthenaPoller`
1. Select Advanced Settings in order to configure the Timeout value to **2 minutes**
1. Click **Next**
1. From the review page, select **Create Function**

</details>


<details>
<summary><strong>Full Solution - Create a CloudWatch Event Rule to trigger Lambda </strong></summary><p>

1. Go to the [CloudWatch Events Rules console page](https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#rules:). 
2. Click **create rule**
3. From the create rule page in the Event Source section. Select **Schedule** followed by **fixed rate** with a value of **5** minutes.
4. From the Target section select **Add target**, then **lambda function**, followed by the new query we just created, **Athena_poller**.
5. Next click on the **Configure Details**
6. Give your rule a name, in this case **every-5-min**
7. Unselect the **Enabled** button to disable the trigger and then select **Create rule** 
</details>

#### Optional CloudFormation
<summary>If you couldn't complete the steps above, optionally, you can deploy the following CloudFormation into your account:</summary><p>
<table>
<thead>
<tr>
<th>Region</th>
<th>Launch Template</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Ireland</strong> (eu-west-1)</td>
<td> <center><a href="https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=AthenaPoller&templateURL=https://s3.amazonaws.com/cf-templates-kljh22251-eu-west-1/athena_poller_template.yaml"><img src="/media/images/CFN_Image_01.png" alt="Launch Athena Poller into Ireland with CloudFormation" width="65%" height="65%"></a></center></td></tr></tbody></table>
</p></details>

1. You select the new policy you created for this roles permissions. You can use the filter to search for **poller**. Now select **Next: Review** to review our role. 
2. Set the Role name to **poller_full_access** and click **create role**
3. Open the Lambda function and retrieve the S3 Athena output location to put in the environment variable