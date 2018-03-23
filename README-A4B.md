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
4.  Upload thumbnail images for the "Small" and "Large" Icons. Note: Image sizes may need to be adjusted to the requirements listed
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

Now your skill has the necessary data to be private published to Alexa For Business.

#### Retrieve Alexa Skills Configuration

**Ensure you followed the instructions using *[ask init](https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html)* to initialize the Alexa Skills Kit (ASK) profile**
<details>
<summary><strong>Watch how to initialize the ASK CLI profile</strong></summary><p>

![Watch how init the ask CLI](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_1.gif)
</details>

1. First, let's list our skills.  Execute the command below using the ASK Profile created in the **ask init** step 
 
```BASH
ask api list-skills --profile <name of ASK profile>
```
<details>
<summary><strong>Watch how to list skills</strong></summary><p>

![Watch how to list skills](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_2.gif)
</details>

2.  When you have the skill id, use the following command to download your skill's manifest json into a file named **myskill.json**:

```BASH
ask api get-skill -s <skill id> -p <name of ASK profile> > myskill.json
```

**Note: this command could take 15-20 seconds to execute**
<details>
<summary><strong>Watch how to retrieve the skill manifest</strong></summary><p>

![Watch how to retrieve the skill manifest](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_3.gif)
</details>

#### Modify Skill Manifest Distribution Mode
3.   We're now going to modify that json file with your favorite Unix editor (e.g. vi)
```BASH
vi myskill.json
```

Note: If you haven't used vi (or it has been awhile), here's a [cheat sheet](https://www.thegeekdiary.com/basic-vi-commands-cheat-sheet/)

4.  Add a line in the json under the **publishingInformation** section:
```SQL
"distributionMode": "PRIVATE",
```
Note: This is what will mark the skill to be shipped for publishing to the Alexa Skills store.
<details>
<summary><strong>Watch how to edit the distribution mode within the skill manifest</strong></summary><p>

![Watch how to edit the skill manifest](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_4.gif)
</details>

#### Update and Submit your skill with the modified manifest
5.  Now we'll update your skill with the modified **myskill.json**:
```BASH
ask api update-skill -s <skill id> -p <name of ASK profile> -f myskill.json
```
**Note: this command could take 15-20 seconds to execute before receiving the message that the skill updated successfully** 
 
6.  Submit the skill via SMAPI
```BASH
ask api submit -s <skill id> -p <name of ASK profile>

Skill submitted successfully.
```
**Note that it may take a couple hours for the skill to be available in the "live" stage.**
 
#### Distribute and Enable Your Skill
 
7.  (This step requires a wait period of 2-3 hours for system propogation)
Distribute the skill to your AWS account so that you can enroll it in Alexa For Business
```BASH
ask api add-private-distribution-account -s <skill id> -p <name of ASK profile> --stage live --account-id arn:aws:iam::<aws account id of moneypenny org>:root

Private distribution account added successfully.
```
 
8.  Navigate into the Alexa For Business console and whitelist users the skill to enable it- for enrolled users they'll also check off the "available" checkbox
![Alexa For Business Console](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_5.gif)
#### (Optional) Account and IAM Permissions
##### Configure Email to invite Users 
After setting up their a4b account and iam permissions (in admin guide) as detailed in the [admin guide](https://docs.aws.amazon.com/a4b/latest/ag/manage-users.html) to invite users and enable in your Alexa companion app 
 
9.  In the bottom left of the Alexa For Business console, under settings **Settings**, choose **User enrollment** then click **Edit**.
 
10. For **Company Name** then *enter the name of your company*.

Note: For Company contact email address, enter the full email address that your invited users can contact if they have any questions while going through the enrollment process.
 
11. Choose **Save**.
 
<details>
<summary><strong>Watch how to set up user enrollment</strong></summary><p>

![Watch how to set up user enrollment](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_6.gif)
</details>

##### Invite users 
12. In the left panel of the Alexa For Business Console, choose **Users** and select **Invite new user**.
 
13.  Enter the First name, Last name, and Email address of the user to enroll, then click **send invite**
 
(Optional) Choose Add another user and add the information from step 3. Repeat this step until you have entered all the information for the users to invite.
<details>
<summary><strong>Watch how to send invite</strong></summary><p>

![Watch how to send invite](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_7.gif)
</details>

Note:  After the invited user clicks on the link and signs up, the **Status** field in the console will show *enrolled* 

Finished! Now the user can enable the skill in their Alexa companion app.  User lifecycle and removal can also be managed within the console. 
