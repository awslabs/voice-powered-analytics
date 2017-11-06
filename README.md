# Workshop Overview
In this workshop you will build a voice powered analytic engine that you can take back to your stakeholders to deliver valuable company insights.   Common questions that may be asked, “Alexa, how many Unique Users did our site have last month?” and “Alexa, how many orders have breached their delivery SLA this week?”.

## The primary products used in this workshop are:
All workshop attendees will need an AWS account with access to the following products. 
<br>
*Note For re:invent attendees:  AWS will not be providing temporary accounts for this workshop. Expected costs for this workshop is < $1 (Assuming free tier eligibility), AWS will be providing $10 AWS credits to cover the expense of the workshop.* 

### Pre-workshop Checklist
Please make sure you have the following availabile prior to the workshop.

- [ ] Amazon Developer account
- [ ] AWS Account with root access or full access
 
Or

- [ ] [Amazon Developer](https://developer.amazon.com/) account
- [ ] Ability to create new IAM policies and roles
- [ ] Full access to Athena – Clusterless Query Engine
- [ ] Full access to Quicksight – Interactive BI Visualizations
- [ ] Full access to S3 – Limitless and durable object store
- [ ] Full access to Lambda – Event-triggered functions
- [ ] Full access to DynamoDB – Managed NoSQL database
- [ ] Full access to Alexa – Voice-powered skills
- [ ] Full access to CloudFormation
- [ ] Full access to CloudWatch, CloudWatch Events, and CloudWatch Logs

**Note** There are two steps that differ from the typical AWS workflow. 

* Development of an Alexa skill requires creation of an account at [Amazon Developer](https://developer.amazon.com/alexa-skills-kit) If you have not created an account yet, please do so before the workshop.
* Using QuickSight requires [signing up](http://docs.aws.amazon.com/quicksight/latest/user/sign-up-existing.html) for the service on a per user basis. Please conplete this step before the workshop to save on time.  

## Workshop Steps

This workshop is designed for first time users of Athena and Alexa. We have broken the workshop into three Steps or focus topics. These are:

* **Athena and Data Discovery Steps**
* **Alexa Skill Building Steps**

We expect most attendees to be able to complete both the Alexa Skill Building and Athena and Data Discovery Steps.

We have provided cloud formation templates and solutions for all steps where the attende is expected to write code. Generally these come in two flavors:

1. Full solution where the attendee does not have to write any code
2. Partial solution where the attendee can author key selections of the code and double check thier work. This path is the recomended path as it provides for the most learning. If time becomes an issue, attendes will always have access to the full solitions so be bold!
3. Many sections also have **Bonus Sections** where you can build additional capability on top of the workshop.   While there aren't hard-and-fast answers for the bonus sections, feel free to engage your workshop facilitator(s)/lab assistant(s) if you'd like additional assistance with these areas.  

In addition to deciding between using the full or partial solutions. The attende can also choose to focus in on the Big Data portion or the Voice powered portion. Please spend time in the workshop you find most interesting and use our full solutions for anything you have already mastered or are not interested in. The partial solution is designed to give you a head start, but still require key additions from the attende. 
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
<td> 
<center><a href="https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=VoiceAlexaSkillFull&templateURL=https://s3.amazonaws.com/cf-templates-kljh22251-eu-west-1/vpa_roles.yaml"><img src="/media/images/CFN_Image_01.png" alt="Launch Alexa Skill into Ireland with CloudFormation" width="65%" height="65%"></a></center></td></tr></tbody></table>

**TODO This needs to create additional DDB tables as well**

## BI and Data Discovery Steps



### Step 1 - Understand Raw Data Set To Query
We will be using a dataset created from Twitter data related to AWS re:Invent 2017. In short, tweets with the #reinvent hashtag or to/from @awsreinvent 
Let's first take a look at the data set we're going to analyze and query.  
#### How we get the data into S3
The data is acquired starting with a Cloudwatch Event triggering an AWS Lambda function every 1 minute.  Lambda is making calls to Twitter's APIs for data, and then ingesting the data into AWS Kinesis Firehose.   Firsthose then microbatches the results into S3 as shown in the following diagram:
<br><IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Athena_Arch_1.png?raw=true" width="80%" height="80%"><br><br>
#### Step 1 Explore the Twitter data
This dataset is available as:
```bash
US-EAST-1 
s3://aws-vpa-tweets/
EU-WEST-1
s3://aws-vpa-tweets-euw1/
```

<details>
<summary><strong>Partial solution - Explore the Twitter Data</strong></summary><p>
AWS Firehose delivers the data into S3 as a GZIP file format.  There are 3 ways to get to this public dataset:

1. Download a sample extract of the data at the following [File Location](https://s3.amazonaws.com/aws-vpa-tweets/tweets/2017/11/06/03/aws-vpa-tweets-1-2017-11-06-03-53-28-b055a510-f718-4207-8e48-05c3ad8c3a5d.gz)
2. Using the [AWS CLI](https://aws.amazon.com/cli/)
3. Using a 3rd party S3 File Explorer such as [Cloudberry Explorer](https://www.cloudberrylab.com/explorer/amazon-s3.aspx)  
</details>


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
  's3://aws-vpa-tweets/tweets/'
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

Before we create the Lambda function, we need to retrieve the bucket where Athena will be delivering the results in our local account.  We can retrieve this by going to the **Athena** service in the AWS console, then clicking *Settings* in the top right Athena menu.  From the dialog, let's copy the value in the *Query result location* (beginning with 's3://') to a local text editor to save for later.
<details>
<summary><strong>Full Solution - Create the lambda to query Athena</strong></summary><p>

1. Go to the [AWS Lambda console page](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions)
2. Click **Create Function** 
3. We will skip using a blueprint to get started and author one from scratch. Click **Author one from scratch** 
4. Leave the trigger blank for now. Click **Next** without adding a trigger from the Configure triggers page.
5. Give your Lambda function a unique name. For example you can use **vpa_lambda_athena** for the query name. For runtime select **Python 3.6**
6. Add a role.  Under role, *Choose an existing role*, and in the box below, choose the role starting with title *vparoles-VPALambdaAthenaPoller*
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

1. Add the role to the Lambda function: lambda_athena_poller
1. Set the following Environment variables:

```
vpa_athena_database = tweets
vpa_ddb_table = VPA_Metrics_Table
vpa_metric_name = Reinvent Twitter Sentiment
vpa_athena_query = SELECT count(*) FROM default."tweets"
region = eu-west-1
vpa_s3_output_location = s3://<your_s3_bucket_name>/poller/
```
Note: for vpa_s3_output_location, use the Athena s3 location copied in the top of this Step's instructions.  
1. From the **Lambda function handler and role** ensure the Handler is set to `vpa_lambda_athena.lambda_handler` and the Existing role to `lambda_athena_poller`
1. Select Advanced Settings in order to configure the Timeout value to **1 minute**
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

## Alexa Skill Building Steps

### Setting up Your Voice User Interface

There are two parts to an Alexa skill. The first part is the Voice User Interface (VUI). This is where we define how we will handle a user's voice input, and which code should be executed when specific commands are uttered. The second part is the actual programming logic for our skill.   Both will be configured in this step-by-step guide.<br>
<IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Arch.png?raw=true" width="80%" height="80%"><br><br>
Alexa fits into your Voice Powered Analytics architecture as the interaction interface for retrieving metrics.  Alexa determines what metrics to retrieve through intents (which we'll describe and configure in the next steps).  The intents correspond to metrics in your DynamoDB data store, which Lambda functions retrieve and send back to the Alexa-enabled device to communicate back to the user:<br>
<IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Arch2.png?raw=true" width="80%" height="80%"><br><br>   
<details>
<summary><strong>Full solution - Setting up VUI (expand for details)</strong></summary><p>
  1. Go to the <a href="http://developer.amazon.com/">Amazon Developer Portal</a>. In the top-right corner of the screen, click the <b>"Sign In"</b> button. <br>(If you don't already have an account, you will be able to create a new one for free.)<br>
  <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_1.png?raw=true" width="80%" height="80%"><br>
  2. Once you have signed in, click the <b>Alexa button</b> at the top of the screen.<br>
  <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_2.png?raw=true" width="80%" height="80%"><br>
  3.  On the Alexa page, choose the <b>"Get Started"</b> button for the Alexa Skills Kit.<br>
  <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_3.png?raw=true" width="40%" height="40%"><br>
  4.  Select <b>"Add A New Skill."</b> This will get you to the first page of your new Alexa skill.
  5.  Fill out the <b>Skill Information screen</b>. Make sure to review the tips we provide below the screenshot.<br>
  <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_4.png?raw=true" width="80%" height="80%"><br>
  <details>
 <summary><strong>Skill Information Tips (expand for details)</strong></summary><p> 

#### Skill Information Tips<br>
i.  <b>Skill Type</b> For this skill, we are creating a skill using the Custom Interaction Model. This is the default choice.
ii. <b>Language</b> Choose the first language you want to support. You can add additional languages in the future, but we need to start with one. (This guide is using U.S. English to start.)
iii.  <b>Name</b> This is the name that will be shown in the Alexa Skills Store, and the name your users will refer to.
iv. <b>Invocation Name</b> This is the name that your users will need to say to start your skill. We have provided some common issues developers encounter in the list below, but you should also review the entire <a href="https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/choosing-the-invocation-name-for-an-alexa-skill">Invocation Name Requirements</a>.
<table>
<thead>
<tr>
<th>Invocation Name Requirements</th>
<th>Examples of incorrect invocation names</th>
</tr>
</thead>
<tbody>
<tr>
<td>The skill invocation name must not infringe upon the intellectual property rights of an entity or person.</td>
<td>korean air; septa check</td>
</tr>
<tr>
<td>Invocation names should be more than one word (unless it is a brand or intellectual property), and must not be a name or place</td>
<td>horoscope; trivia; guide; new york</td>
</tr>
<tr>
<td>Two word invocation names are not allowed when one of the words is a definite article, indefinite article, or a preposition</td>
<td>any poet; the bookie; the fool</td>
</tr>
<tr>
<td>The invocation name must not contain any of the Alexa skill launch phrases and connecting words.  Launch phrase examples include "launch," "ask," "tell," "load," and "begin."  Connecting word examples include "to," "from," "by," "if," "and," "whether."</td>
<td>trivia game for star wars; better with bacon</td>
</tr>
<tr>
<td>The invocation name must not contain the wake words "Alexa," "Amazon," "Echo," or the words "skill" or "app."</td>
<td>hackster initial skill; word skills</td>
</tr>
<tr>
<td>The invocation name must be written in each language you choose to support.  For example, the German version of your skill must have an invocation name written in German, while the English (US) version must have an invocation name written in English.</td>
<td>kitchen stories (German skill)</td>
</tr></tbody></table>
 </p></details>
6.  Click the Next button to move to the <b>Interaction Model</b>.
7. Click on the <b>Launch Skill Builder (Beta)</b> button . This will launch the new Skill Builder Dashboard.
<IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_5.png?raw=true" width="80%" height="80%"><br>
8.  Click on the "<b>Code Editor"</b> item under Dashboard on the top left side of the skill builder.
9.  In the textfield provided, replace any existing code with the code provided in the <a href="https://github.com/voicehacks/setup-local-recommendations/blob/master/speech-assets/InteractionModel.json">Interaction Model</a>, then click "Apply Changes" or "Save Model".
10.  Click on the <b>"Dashboard"</b> button.
11.  Add some more sample utterances for your newly generated intents. These are the things a user would say to make a specific intent happen. Here are a few examples:
  - Show me my metrics / List my metrics
  - What is my {metric}<br>
<IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_6.png?raw=true" width="80%" height="80%"><br>
12.  Click <b>"Build Model"</b> and <b>"Save"</b><br>
<IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_7.png?raw=true" width="80%" height="80%"><br>
13. If your interaction model builds successfully, click on <b>Configuration button</b> to move on to Configuration. In our next step of this guide, we will be creating our Lambda function in the AWS developer console, but keep this browser tab open, because we will be returning here on <a href="https://github.com/voicehacks/setup-local-recommendations/blob/master/step-by-step/3-connect-vui-to-code.md">Page #3: Connect VUI to Code</a>. <br>
<IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_8.png?raw=true" width="80%" height="80%"><br>
<br>If you get an error from your interaction model, check through this list:
   - Did you copy & paste the provided code into the appropriate boxes?
   - Did you accidentally add any characters to the Interaction Model or Sample Utterances?
</details>

### Configure Alexa Backend
Now that we've configured the voice interaction, let's set up our Lambda function to leverage your DynamoDB metrics and be triggered by the Alexa Skills Kit. 
<br>Please deploy the following template into your AWS environment which contains the Lambda code for the Alexa skill. 
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
<td> <center><a href="https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=VoiceAlexaSkillFull&templateURL=https://s3.amazonaws.com/cf-templates-kljh22251-eu-west-1/skill_template_partial.yaml"><img src="/media/images/CFN_Image_01.png" alt="Launch Alexa Skill into Ireland with CloudFormation" width="65%" height="65%"></a></center></td></tr></tbody></table>
<details>
<summary><strong>Full solution - Setting up Alexa Backend (expand for details)</strong></summary><p>
  1. Check your <b>AWS region</b>. For the reinvent workshop, we'll be using the <b>EU (Ireland)</b> region.<br>
<IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_9.png?raw=true" width="80%" height="80%"><br>
  2. Open the Lambda function, starting with <b>“VoiceAlexaSkillFull-AlexaMetricSkill-1”</b> deployed with the Cloudformation.   <b>Configure your trigger</b>. Click the <b>Triggers</b> tab. Within the <b>Triggers</b> pane, click the link to <b>Add a Trigger</b>. A pop-up should appear, click in the dashed box and select Alexa Skills Kit from the list. If you don't see Alexa Skills Kit in the list, jump back to step #3 on this page.<br>
  <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_10.png?raw=true" width="80%" height="80%"><br>
  3. Once you have selected Alexa Skills Kit, click the <b>Configuration</b> Tab to go back to your code.<br>
  4. The <b>ARN value</b> should be in the top right corner. Copy this value for use in the next section of the guide.<br>
  <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_11.png?raw=true" width="80%" height="80%"><br>
</p>
  5.  Within the Lambda configuration, navigate to <b>Environment Variables</b>.  Add a greeting and exit message for your Alexa skill by adding two environment variables(case sensitive): <b>greeting_msg</b> and <b>exit_msg</b>
  <details>
<summary>Example</summary><p>
  greeting_msg <i>Welcome to the Voice Powered Analytics.  Please tell me what metrics you'd like to hear. To hear available metrics, ask Alexa tell me my metrics</i> <br>
  and
  exit_msg <i>Thank you for trying the Voice Powered Analytics.  Have a nice day!</i>
</p></details>
  6.  We'll also add an environment variable called: <b>metrics_table</b> called <i>VPA_Metrics_Table</i>.  This references the DynamoDB table that the Alexa skill will be querying for your metric 
<details>
<summary>Hint</summary><p>
  <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_11b.png?raw=true" width="80%" height="80%">
  </p></details>
  7. Bonus (If time): can you add a skill to the Lambda function which enables users to "List My Metrics"
<details>
<summary>Optionally, you can deploy the following CloudFormation:</summary><p>
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
<td> <center><a href="https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=VoiceAlexaSkillFull&templateURL=https://s3.amazonaws.com/cf-templates-kljh22251-eu-west-1/skill_template.yaml"><img src="/media/images/CFN_Image_01.png" alt="Launch Alexa Skill into Ireland with CloudFormation" width="65%" height="65%"></a></center></td></tr></tbody></table>
</p></details>

</details>

### Connecting Your Voice User Interface to Your Lambda Function
On Step 1 "Setting up Your Voice User Interface" of this Step, we created a voice user interface for the intents and utterances we expect from our users. On "Step 2 Configure Alexa Backend", we created a Lambda function that contains all of our logic for the skill. On this page, we need to connect those two pieces together.<br>
<details>
<summary><strong>Full solution - Connecting VUI to Lambda (expand for details)</strong></summary><p>
  
1.  Go back to the <b><a href="https://developer.amazon.com/edw/home.html#/skills/list">Amazon Developer Portal</a></b> and select your skill from the list. You may still have a browser tab open if you started at the beginning of this tutorial.
2. Open the "Configuration" tab on the left side.<br>
  <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_12.png?raw=true" width="40%" height="40%"><br>
3. Select the <b>"AWS Lambda ARN"</b> option for your endpoint. You have the ability to host your code anywhere that you would like, but for the purposes of simplicity and frugality, we are using AWS Lambda. <a href="https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/developing-an-alexa-skill-as-a-web-service">(Read more about Hosting Your Own Custom Skill Web Service.)</a> With the AWS Free Tier, you get 1,000,000 free requests per month, up to 3.2 million seconds of compute time per month. Learn more at <a href="https://aws.amazon.com/free/">https://aws.amazon.com/free/</a>. In addition, Amazon now offers <a href="https://developer.amazon.com/alexa-skills-kit/alexa-aws-credits">AWS Promotional Credits for developers who have live Alexa skills that incur costs on AWS related to those skills</a> IMPORTANT: Make sure you select the same region that you created your Lambda in.<br>
  <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_13.png?raw=true" width="80%" height="80%"><br>
4.  Paste your <b>Lambda's ARN</b> (Amazon Resource Name) into the textbox provided. It should look similar to the screenshot above.
5.  Leave <b>"Account Linking" set to "No"</b>. For this skill, we won't be using Account Linking, but you can learn more about <a href="https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/linking-an-alexa-user-with-a-user-in-your-system">Linking an Alexa User with a User in Your System.</a>
6.  Click the <b>"Next"</b> button to continue to page #4 of this guide.
</details>
</p>

### Testing Your Alexa Skill
You've now created a Voice User Interface and a Lambda function, and connected the two together. Your skill is now ready to test.
<details>
<summary><strong>Full Solution - Testing Your Alexa Skill</strong></summary><p>
1.  Go back to the <b><a href="https://developer.amazon.com/edw/home.html#/skills/list">Amazon Developer Portal</a></b> and select your skill from the list. You may still have a browser tab open if you started at the beginning of this tutorial.
2. Open the <b>"Test"</b> tab on the left side.<br>
  <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_15.png?raw=true" width="40%" height="40%"><br>
3.  Test your skill with the <b>Service Simulator</b>. To validate that your skill is working as expected, use the Service Simulator. In the <b>Enter Utterance</b> text box, type "What’s my reinvent tweets over the last hour."<br>
  <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_16.png?raw=true" width="80%" height="80%"><br>
  </p>
4.  Other testing methods to consider:
- <a href="https://echosim.io/">Echosim.io</a> - a browser-based Alexa skill testing tool that makes it easy to test your skills without carrying a physical device everywhere you go.
- <a href="https://github.com/alexa/skill-sample-nodejs-city-guide/blob/master/unit-testing.md"> Unit Testing with Alexa</a> - a modern approach to unit testing your Alexa skills with <a href="http://getpostman.com/">Postman</a> and <a href="http://aws.amazon.com/apigateway">Amazon API Gateway</a>.
5. If your sample skill is working properly, you can now customize your skill.

<summary><strong>Service Simulator Tips</strong></summary><p>
- After you click the <b>"Ask [Your Skill Name]"</b> button, you should see the <b>Lambda Request and Lambda Response boxes</b> get populated with JSON data like in the screenshot above.
- Click the <b>Listen</b> button in the bottom right corner to hear Alexa read the response.
- You can have an entire conversation with your skill with the Service Simulator. Try the following commands:
- "tell me about this place"
- [Press the listen button, and type "recommend an attraction" in the box]
- [Press the listen button, and type "give me an activity" in the box]
(Continue this process for all of the utterances. To start over, click the "Reset" button.)
- If you receive a response that reads: <i>"The remote endpoint could not be called, or the response it returned was invalid,"</i> this is an indication that something is broken. AWS Lambda offers an additional testing tool to help you troubleshoot your skill.
</p></p></details></details>

### Bonus: What Utterances and Intents Are Needed For a "List My Metrics" skill
<details>
<summary><strong>Hints</strong></summary><p>
  <br>Intent: ListMetrics
  <br>Utterance(s): 
  <br>- ListMetrics List My Metrics
  <br>- ListMetrics What are my metrics
</p></details>