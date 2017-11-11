##**Note that this workshop is not yet live.  It will be live at reinvent 2017 Wednesday 11/29**

# Voice Powered Analytics

This workshop is designed for first time users of QuickSight, Athena, and Alexa. We have broken the workshop into three steps or focus topics. 
These are:

#### Using QuickSight for Data Discovery
#### Using Athena to query data in S3 and create answers for Alexa
#### Building an Alexa skill to access the answers from Athena

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
* Using QuickSight requires [signing up](http://docs.aws.amazon.com/quicksight/latest/user/sign-up-existing.html)


## Modules

This workshop is broken up into multiple modules. You must complete each Section before proceeding to the next, however, there are AWS CloudFormation templates available that you can use to launch the necessary resources without manually creating them yourself if you'd like to skip ahead.

1. [Amazon QuickSight Section](README-QuickSight.md)
1. [Amazon Athena Section](README-Athena.md)
1. [Amazon Alexa Section](README-Alexa.md)

After you have completed the workshop you can delete all of the resources that were created by following the [cleanup guide](README-Cleanup.md).