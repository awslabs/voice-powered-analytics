# Workshop Overview
In this [workshop](https://github.com/awslabs/voice-powered-analytics) you will build a voice powered analytic engine that you can take back to your stakeholders to deliver valuable company insights.   Common questions that may be asked, “Alexa, how many Unique Users did our site have last month?” and “Alexa, how many orders have breached their delivery SLA this week?”.


## Section 4: Alexa For Business Deployment
In this section, we will deploy the newly created Alexa skill to a private repository within Alexa For Business.   This will make the skill only accessible to specific individuals within your organization so they can add it as a skill onto their device.  
 
Note, that the following dependencies are needed in order to successfully complete this section of the workshop.

- [ ] Successful completion of [Alexa Skill Building Section](https://github.com/awslabs/voice-powered-analytics/blob/master/README-Alexa.md)
- [ ] Installation of the [Alexa Skills Kit (ASK) Command Line Interface (CLI)](https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html)

#### Update Alexa Skill with Required Metadata For Alexa For Business Publishing
Alexa For Business requires certains fields in order for a skill to be accessible in the Alexa companion application privately.  

1. Navigate to your skill in the [Alexa Developer Portal](https://developer.amazon.com/) 
2. Click "Edit" to your skill's Interaction Model  

**Note: These lab instructions reflect the old Alexa Skills console.  If given the option, in the top right-hand corner of the screen, click "Your Alexa Console", then "Skills". This will bring you back to the traditional console experience**   

3. On the left side of the screen under "Publishing Information", please add values for the following fields:
- Short Skill Description
- Full Skill Desciprtion
- Example Phrases
4.  Upload thumbnail images for the Small (108px) and Large(512px) Icons. Note: Image sizes may need to be adjusted to the requirements listed.  Here are links to some samples to save time: [Small](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/VPA_Logo_108.jpeg), [Large](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/VPA_Logo_512.jpeg).
5.  Click "Next"
6. Answer the Global Fields about your app:
- Category
- Testing Instructions
- Countries & Regions
7.  Answer Yes/No for the following questions about your skill's Privacy:
- Does this skill allow users to make purchases or spend real money?
- Does this Alexa skill collect users' personal information?
- Is this skill directed to or does it target children under the age of 13?
8.  Answer Yes/No for the following questions about your skill's compliance:
 - Export Compliance
 - Does this skill contain advertising?
9.  Then click "Save"

In the next few minutes, you will receive an email with an update on your approval and instructions (as shown below) to configure your skill for private access in Alexa For Business.

**NOTE: It may take 90 minutes for your skill to be available for distribution**


#### Distribute To Alexa For Business Organizations

Within 90 minutes, your skill will be available for Alexa for Business distribution.  The instructions below show how to enable skill availability to Alexa For Business
 
 
1. First, **click on your skill** within the Amazon Developer Console. 
2. Next, **click on the *Distribution Link*** on the top menu bar.  Then **click on *Availability*** on the left side menu. 
This brings you the screen to link your Alexa skill to your AWS Alexa For Business organization. 
 
![Availability Screen](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_1a.png)
 
Next, we'll need to retrieve the IAM (Identity and Access Management) ARN (Amazon Resource Number) ID of our for Alexa For Business private skills. 
 
3.  To do this, *navigate to the **AWS Console***, then **choose Alexa For Business**. 
4.  On the left menu, **choose Skills**, then in the Skill screen, **choose the Private Skills tab** 
5.  Under the Private Skills tab, **click the *Show IAM ARN* button**.  This process will link your AWS Account ID and IAM user from Amazon Developer (where your skill is owned) to AWS account for skill/private user management 
6.  **Copy the ID** It will look similar to the following: *arn:aws:iam::123456789012:root** 
![A4B Screen](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_2a.png) 
 
7. *Navigate back to the Amazon Developer console screen* where you should be on the Availability Screen.  If you're not, then repeat Step 1 and 2 in this section. 
8. Scroll down to the *Manage Access to this Skill* section, and **enter the copied IAM ARN ID** under the section *Enter an Alexa for Business Organization* 
9. **Click the *Add* button** 
10.  **Click the *Save* button** 
 
![Adding ARN ID Screen](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_3a.png) 
 
You've now linked the skill to your Alexa For Business account.   Within a few seconds, you can refresh the Private Skills screen and see your skill listed below: 
 
![Adding ARN ID Screen](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_4a.png) 
 
#### (Optional) Account and IAM Permissions
##### Configure Email to invite Users 
After setting up their a4b account and iam permissions (in admin guide) as detailed in the [admin guide](https://docs.aws.amazon.com/a4b/latest/ag/manage-users.html) to invite users and enable in your Alexa companion app 
 
9.  In the bottom left of the Alexa For Business console, under settings **Settings**, choose **User invitations** then click **Edit**.
 
10. For **Company Name** then *enter the name of your company*.

Note: For Company contact email address, enter the full email address that your invited users can contact if they have any questions while going through the enrollment process.
 
11. Choose **Save**.
 
<details>
<summary><strong>Watch how to set up user enrollment</strong></summary><p>

![Watch how to set up user enrollment](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_6.gif)
</details>

##### Invite users 
12. In the left panel of the Alexa For Business Console, choose **Users** and select **Invite user**.
 
13.  Enter the First name, Last name, and Email address of the user to enroll, then click **send invite**
 
(Optional) Choose Add another user and add the information from the previous step. Repeat this step until you have entered all the information for the users to invite.
<details>
<summary><strong>Watch how to send invite</strong></summary><p>

![Watch how to send invite](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_7.gif)
</details>

Note:  After the invited user clicks on the link and signs up, the **Status** field in the console will show *enrolled* 

Finished! Now the user can enable the skill in their Alexa companion app.  User lifecycle and removal can also be managed within the console. 
