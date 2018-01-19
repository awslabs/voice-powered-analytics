# Workshop Overview
In this workshop you will build a voice powered analytic engine that you can take back to your stakeholders to deliver valuable company insights.   Common questions that may be asked, “Alexa, how many Unique Users did our site have last month?” and “Alexa, how many orders have breached their delivery SLA this week?”.


## Section 4: Alexa For Business Deployment

Note, that the following dependencies are needed in order to successfully complete this section of the workshop.

- [ ] Successful completion of Alexa Skill Building Section
- [ ] Installation of the [Alexa Skills Kit (ASK) Command Line Interface (CLI)](https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html)


#### Retrieve Alexa Skills Configuration

**Ensure you followed the instructions using *[ask init](https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html)* to initialize the Alexa Skills Kit (ASK) profile**
<details>
<summary><strong>Watch how to initialize the ASK CLI profile</strong></summary><p>

![Watch how init the ask CLI](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_1.gif)
</details>

1. Download and modify your current skill config json to mark it for non publishing

Find the skill id of the skill you want to enroll.  Note, you can find the ASK profile name in the [Amazon Developer Portal](https://developer.amazon.com/alexa-skills-kit)

```BASH
ask api list-skills --profile <name of ASK profile>
```
<details>
<summary><strong>Watch how to list skills</strong></summary><p>

![Watch how to list skills](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_2.gif)
</details>

2.  When you have the skill id, use in the following command to download your skill json into a file named **myskill.json**:

```BASH
ask api get-skill -s <skill id> -p <name of ASK profile> > myskill.json
```

**Note: this command could take 15-20 seconds to execute**
<details>
<summary><strong>Watch how to retrieve the skill configuration</strong></summary><p>

![Watch how to retrieve the skill configuration](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_3.gif)
</details>

#### Modify Skill Configuration Distribution Mode
3.   We're now going to modify that json file in your favorite Unix editor (e.g. vi)
```BASH
vi myskill.json
```

Note: If you haven't used vi (or in awhile), here's a [cheat sheet](https://www.thegeekdiary.com/basic-vi-commands-cheat-sheet/)

4.  Add a line in the json under the **publishingInformation** section:
```SQL
"distributionMode": "PRIVATE"
```
Note: This is what will mark the skill to be skipped for publishing to the Alexa Skills store.
<details>
<summary><strong>Watch how to edit the distribution mode within the skill configuration</strong></summary><p>

![Watch how to edit the skill configuration](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_4.gif)
</details>

#### Update and Submit your skill with the modified configuration
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
Distribute the skill to your AWS account so that you can enroll it in Moneypenny
```BASH
ask api add-private-distribution-account -s <skill id> -p <name of ASK profile> --stage live --account-id arn:aws:iam::<aws account id of moneypenny org>:root

Private distribution account added successfully.
```

8.  Navigate into the Alexa For Business console and whitelist users the skill to enable it- for enrolled users they'll also check off the "available" checkbox
![Alexa For Business Console](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/a4b_5.gif)
#### (Optional) Account and IAM Permissions

9.  After setting up their a4b account and iam permissions (in admin guide) follow [this guide](https://docs.aws.amazon.com/a4b/latest/ag/manage-users.html) to invite users and enable in your Alexa companion app
