# Voice Powered Analytics - QuickSight Lab

In this lab we will use QuickSight to explore our dataset and visualize a few interesting metrics of the twitter dataset. 

**NOTE** If you are already familiar with QuickSight please feel free to skip to the [Athena Section](README-Athena.md) below

## Step 1 - Understand The Raw Data (OPTIONAL)

This is an optional step of the optional lab. It is intended to give you a better understanding of the data we are using for the lab. 
If you don't want to inspect the JSON files you can safely skip this step and continue with [Step 2](#step-2---create-an-athena-table). 
Each file in s3 has a collection of JSON objects stored within the file.
In addition, the files have been gziped by [Kinesis FIrehose](https://aws.amazon.com/kinesis/firehose/) which saves cost and improves performance.

We will be using a dataset created from Twitter data related to AWS re:Invent 2017. 
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
US-EAST-1 | ```s3://aws-vpa-tweets/```
EU-WEST-1 | ```s3://aws-vpa-tweets-euw1/```


Amazon Kinesis Firehose delivers the data into S3 as a GZIP file format.
You can use a variety of methods to download one of the files in the dataset. If you use the AWS CLI today, this is likely the easiest method to take a look at the data.

List one of the files with (Note use **s3://aws-vpa-tweets-euw1...** for Ireland):
```bash
aws s3 ls s3://aws-vpa-tweets/tweets/sample/2017/11/06/04/aws-vpa-tweets-sample.gz
```
Download this file to your local directory (Note use **s3://aws-vpa-tweets-euw1...** for Ireland):
```bash
aws s3 cp s3://aws-vpa-tweets/tweets/sample/2017/11/06/04/aws-vpa-tweets-sample.gz .
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

## Step 2 - Create an Athena table

We need to create a table in Amazon Athena. This will allow us to query the data at rest in S3 from QuickSight. 
The twitter data is stored as JSON documents and then compressed in s3. 
Athena supports reading of gzip files and includes json SerDe's to make parsing the data easy.

There is no need to copy the dataset to a new bucket for the workshop. 
The data is publicly available in the bucket we provide.   

**Create Athena table**

1. Please make sure you are in the **same region** that launched the Cloudformation stack 
1. For the **Ireland region**, modify the location field below with the following location:
LOCATION
  's3://aws-vpa-tweets-euw1/tweets/'
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
  's3://aws-vpa-tweets/tweets/'
```

**Verify the table created correctly** 
1. You'll see an Athena table called *tweets* in the *default* database (You may have to hit refresh).
1. If you click on the *tweets* table, you can see the fields that we saw earlier.    
1. Let's test that the tweets table works.  In the same Query Editor run the following `SELECT` statement (clear the previous statement):

```SQL
SELECT COUNT(*) AS TOTAL_TWEETS FROM tweets;
```
The statement above shows the total amount of tweets in our data set. 
**Note** The result should be in the 1000's. If you got a tiny number, something is wrong. 
Recreate your table or ask one of the lab assistants for help.


## Step 3 - Explore the data using Quicksight
We've created an Athena table directly on top of our S3 Twitter data, let's explore some insights on the data.  
While this can be achieved through Athena itself or compatible query engines, Amazon Quicksight enables you to connect directly to Athena and quickly visualize it into charts and graphs without writing any SQL code.  
Let's explore:      

**Import Permissions note** 
1. Launch the [QuickSight portal](https://us-east-1.quicksight.aws.amazon.com/).  This may ask you to register your email address for Quicksight access.  
1. If haven't already configured, Quicksight may need special permissions to access Athena:   
a. (These settings can only be changed in the **N.Virginia region**) In the upper right corner, ensure **US East N. Virginia** is selected, then to the right of the *region* in the upper right corner, choose your profile name, and from the dropdown menu, choose *Manage Quicksight*.    
b. On the left menu, click *Account Settings*  
c. Click the *Edit AWS permissions* button  
d. Ensure the box *Amazon Athena* is checked.  
e. Click *Choose S3 Buckets*, **Choose Select All**.   
f. Click the Tab *S3 Buckets you can access across AWS*, under *Use Different Bucket*, Type: ```aws-vpa-tweets``` (Note For Ireland: ```aws-vpa-tweets-euw1```) Then click **Add S3 Bucket**, then click **Select Buckets**, then click **Apply**    
<details>
<summary><strong>Watch how to set Quicksight Permissions</strong></summary><p>

![Watch how to set Quicksight Permissions](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Quicksight_Permissions.gif)
</p></details> 

1. **(if running out of Ireland)** In the main Quicksight portal page, switch back to the **EU Ireland Region**)
1. In the upper right choose your  **Manage data**
1. Now in the upper left choose **New data set**
1. You will see tiles for each of the QuickSight supported data sources. From this page select the **Athena** tile. 
1. When asked for the dataset name you can choose anything you like, for our example we use **tweets-dataset** You can choose to validate that SSL will be used for data between Athena and QuickSight. Finish be selecting **Create data source**
1. Now we need to choose the Athena table we created in **Step 1**. For our example we used the **Default** database, with a table name of **tweets**. Finish by clicking on **Select**. 
1. SPICE is not needed for this workshop. If asked, select **Directly query your data**. Click Visualize when done. 
1. QuickSight will now import the data. Wait until you see **Import Complete**. Then close the summary window. 
1. Add the **created** field from the Athena table by dragging it from the Field list to the empty AutoGraph window.
1. From the *Visual types* in the bottom left corner, select **Vertical bar chart**
1. Add another Visual by selecting in the top left corner, the **+ Add** button  and then **Add visual**
1. On this new graph, lets add the **country** field. 
1. As you can see, lots of tweets do not include which country the tweet was created in. Lets filter these results out. Click on the large bar labeled **none**, then select **exclude "none"** from the pop up window. As you can see the tweets without a location were excluded.
1. Lets change the visual from a bar chart to a pie chart. Select the entire visual, then from the bottom right select the **pie chart** visual.  Add **Group By: "country"**

**Bonus: What other interesting insights can you find from this data in Quicksight?**
* **Tweet @chadneal and @WestrichAdam** with link to a screenshot of an interesting insight you captured from this data.  It may be added below to our ***Voice Powered Analytics** Quicksight Attendee Submissions* 
<details>
	<summary><strong>Voice Powered Analytics Quicksight Attendee Submissions!</summary></strong>

Kiran Chitturi (@nkchitturi) 11/29/17:
![@nkchitturi Quicksight Submission](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/VPA_Quicksight_Submission_1.jpg) 
 
Thibaut LaBarre (@Thibqut) 11/29/17:
![@Thibqut Quicksight Submission](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/VPA_Quicksight_Submission_2.jpg) 
 
Cameron Pope (@theaboutbox) 11/29/17:
![@theaboutbox Quicksight Submission](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/VPA_Quicksight_Submission_3.jpg)
</details>

 
## Step 4 - Start on the Athena lab
 
To continue the workshop, start on the [Athena Lab](README-Athena.md)
