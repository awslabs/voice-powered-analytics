##**Note that this workshop is not yet live.  It will be live at reinvent 2017 Wednesday 11/29**

# Voice Powered Analytics

his workshop is designed for first time users of Athena and Alexa. We have broken the workshop into three Steps or focus topics. These are:

* **Athena and Data Discovery Steps**
* **Alexa Skill Building Steps**

We expect most attendees to be able to complete both the Alexa Skill Building and Athena and Data Discovery Steps.

We have provided cloud formation templates and solutions for all steps where the attende is expected to write code. Generally these come in two flavors:

1. Full solution where the attendee does not have to write any code
2. Partial solution where the attendee can author key selections of the code and double check thier work. This path is the recomended path as it provides for the most learning. If time becomes an issue, attendes will always have access to the full solitions so be bold!
3. Many sections also have **Bonus Sections** where you can build additional capability on top of the workshop.   While there aren't hard-and-fast answers for the bonus sections, feel free to engage your workshop facilitator(s)/lab assistant(s) if you'd like additional assistance with these areas.  


## Prerequisites

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


## Modules

This workshop is broken up into multiple modules. You must complete each Section before proceeding to the next, however, there are AWS CloudFormation templates available that you can use to launch the necessary resources without manually creating them yourself if you'd like to skip ahead.

1. [Athena and Data Discovery Section](README-Athena)
2. [Alexa Skill Building Section](README-Alexa)

After you have completed the workshop you can delete all of the resources that were created by following the [cleanup guide](README-Cleanup).