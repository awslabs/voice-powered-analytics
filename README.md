##**Note that this workshop is not yet live.  It will be live at reinvent 2017 Wednesday 11/29**

# Voice Powered Analytics

This workshop is designed for first time users of QuickSight, Athena, and Alexa. We have broken the workshop into three steps or focus topics. 
These are:

* Using QuickSight for Data Discovery
* Using Athena to query data in S3 and create answers for Alexa
* Building an Alexa skill to access the answers from Athena

We expect most attendees to be able to complete the full workshop in 2 hours. 
To help keep things focused on Athena, Alexa, and QuickSight we have provided CloudFormation templates and sample code.
Many sections also have **Bonus Sections** where you can build additional capability on top of the workshop.  
Feel free to engage your workshop facilitator(s)/lab assistant(s) if you'd like additional assistance with these areas.  


## Prerequisites

Please make sure you have the following available prior to the workshop.

* Amazon Developer account
* AWS Account with admin or full access to all services

**Note** There are two steps that differ from the typical AWS workflow. 
Please complete these before attending the workshop to save time. 
* Development of an Alexa skill requires creation of an account at [Amazon Developer](https://developer.amazon.com/alexa) 
* Using QuickSight requires [Signing up for QuickSight](http://docs.aws.amazon.com/quicksight/latest/user/sign-up-existing.html)


## Modules

This workshop is broken up into multiple modules. The QuickSight section is optional as the Athena and Alexa sections do not build on any of the artifcats created in the QuickSight section. 
You must however complete the Athena lab before starting on the Alexa lab. 

1. **OPTIONAL** [Amazon QuickSight Section](README-QuickSight.md)
1. [Amazon Athena Section](README-Athena.md)
1. [Amazon Alexa Section](README-Alexa.md)

After you have completed the workshop you can disable to the CloudWatch Event to disable the Athena poller if you would like to leave the resources in place but not pay for ongoing Athena table scans. If you want to completely remove all resources please follow the [cleanup guide](README-Cleanup.md).

## Lab Setup

We have provided a CloudFormation template to create resources needed by this lab but are not the focus of the workshop. These include IAM Roles, IAM Policies, a DynamoDB table, and a CloudWatch Event rule. These are listed as outputs in the CloudFormation template in case you want to inspect them.
Please launch the below template so that the resources created will be ready by the time you get to those sections in the lab guides. 

Region | Launch Template
----- | -----

EU-WEST-1 | [![Launch Template](/media/images/CFN_Image_01.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=VPA-Setup&templateURL=https://s3.amazonaws.com/aws-vpa-tweets/setup/vpa_setup.yaml)

