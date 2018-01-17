# Voice Powered Analytics

### Introduction
In this workshop, you will build an Alexa skill that queries metrics from a data lake, which you will define.  The goal after leaving this workshop, is for you to understand how to uncover Key Performance Indicators (KPIs) from a data set, build and automate queries for measuring those KPIs, and access them via Alexa voice-enabled devices.  Startups can make  available voice powered analytics to query at any time, and Enterprises can deliver these types of solutions to stakeholders so they can have easy access to the Business KPIs that are top of mind.         
This workshop requires fundamental knowledge of AWS services, but is designed for first time users of QuickSight, Athena, and Alexa. We have broken the workshop into three sections or focus topics. 
These are:

* Data Discovery using QuickSight
* Building Data Lake analytics in Athena (based on objects in S3) to generate answers for Alexa
* Building a custom Alexa skill to access the analytics queries from Athena

We expect most attendees to be able to complete the full workshop in **2 hours**. 

To help keep moving through the sections in case you get stuck anywhere, we have provided CloudFormation templates and sample code.

For those feeling creative, many sections also have **Bonus Sections** where you can build additional capability on top of the workshop.  
Feel free to engage your workshop facilitator(s)/lab assistant(s) if you'd like additional assistance with these areas.  

You can also contact @chadneal or @WestrichAdam on twitter if you have additional questions or feedback.

## Prerequisites

Please make sure you have the following available prior to the workshop.

* <a href="https://developer.amazon.com/alexa" target="_blank">Amazon Developer</a> account (Free) **Note** This is different from a typical AWS workflow. 
* AWS Account with admin or full access to all services
* Using QuickSight requires <a href="http://docs.aws.amazon.com/quicksight/latest/user/sign-up-existing.html" target="_blank">Signing up for QuickSight</a>

## Lab Setup

We have provided a CloudFormation template to create baseline resources needed by this lab but are not the focus of the workshop. These include IAM Roles, IAM Policies, a DynamoDB table, and a CloudWatch Event rule. These are listed as outputs in the CloudFormation template in case you want to inspect them.

**Please launch the template below so that the resources created will be ready by the time you get to those sections in the lab guides.** 

**Pick the desired region that's closest to your location for optimal performance **

When you launch the template you will be asked for a few inputs. Use the following table for reference. 

Input Name | Value
:---: | :---:
Stack Name | VPA-Setup
DDBReadCapacityUnits | 5
DDBWriteCapacityUnits | 5

<details>
<summary><strong>Watch a video of launching CloudFormation (Click to expand)</strong></summary><p>

![launcg CloudFormation](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/vpa-cloudformation-launch.gif)

</details>

<table><tr><td>Region</td> <td>Launch Template</td></tr>
<tr>
<td>EU-WEST-1</td> <td><a href="https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=VPA-Setup&templateURL=https://s3.amazonaws.com/aws-vpa-tweets-euw1/setup/vpa_setup.yaml" target="_blank"><IMG SRC="/media/images/CFN_Image_01.png"></a></td></tr> <tr><td>US-EAST-1</td> <td><a href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=VPA-Setup&templateURL=https://s3.amazonaws.com/aws-vpa-tweets/setup/vpa_setup.yaml" target="_blank"><IMG SRC="/media/images/CFN_Image_01.png"></a></td></tr>


## Modules

This workshop is broken up into multiple modules. The QuickSight section is optional as the Athena and Alexa sections do not build on any of the artifcats created in the QuickSight section. 
You must however complete the Athena lab before starting on the Alexa lab. 

1. [Amazon QuickSight Section](README-QuickSight.md) 
1. [Amazon Athena Section](README-Athena.md)
1. [Amazon Alexa Section](README-Alexa.md)

After you have completed the workshop you can disable to the CloudWatch Event to disable the Athena poller. This will stop the automated scans of s3 from Athena and also serve to stop any further Athena costs. If you want to completely remove all resources please follow the [cleanup guide](README-Cleanup.md).

