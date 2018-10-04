# Workshop Overview
In this workshop you will build a voice powered analytic engine that you can take back to your stakeholders to deliver valuable company insights.   Common questions that may be asked, “Alexa, how many Unique Users did our site have last month?” and “Alexa, how many orders have breached their delivery SLA this week?”.

## Section 3: Alexa Skill Building

Note, that the following dependencies are needed in order to successfully complete this section of the workshop.

- [ ] Successful completion of Athena Query Building Section
- [ ] [Amazon Developer account](http://developer.amazon.com/) (free)

## Section 3: Alexa Skill Building
### Step 1: Setting up Your Voice User Interface
There are two parts to an Alexa skill. The first part is the Voice User Interface (VUI). This is where we define how we will handle a user's voice input, and which code should be executed when specific commands are uttered. The second part is the actual programming logic for our skill.   Both will be configured in this step-by-step guide.
![](./media/images/Alexa_Arch.png)

Alexa fits into your Voice Powered Analytics architecture as the interaction interface for retrieving metrics.  Alexa determines what metrics to retrieve through intents (which we'll describe and configure in the next steps).  The intents correspond to metrics in your DynamoDB data store, which Lambda functions retrieve and send back to the Alexa-enabled device to communicate back to the user:
![](./media/images/Alexa_Arch2.png)
<details>
<summary><strong>Full solution - Setting up VUI (expand for details)</strong></summary>

1.	Go to the [Amazon Developer Portal](http://developer.amazon.com/)
2.	Click the **Alexa button** on the left portion of the screen.

![](./media/images/Alexa_Lab_v2_1.png)

3.	In the top-right corner of the screen, **click the Sign In button**. (If you don't already have an account, you will be able to create a new one for free.)
4.	Once you have signed in, on the Alexa page, **click the Alexa Skills Kit button**, which is what we'll use to create our custom skill.

![](./media/images/Alexa_Lab_v2_2.png)

5.	Next **Click on Start a Skill Button**

![](./media/images/Alexa_Lab_v2_3.png)

6.	Click on Create Skill button to start creating a custom skill.

![](./media/images/Alexa_Lab_v2_4.png)

7.	Type in the **Skill name** *Voice Powered Analytics*, Select the **Custom** button and finally click the **Create Skill** button:

![](./media/images/Alexa_Lab_v2_5.png)


8.	Select the option **Start From Scratch**,then select the **Choose** button in the top righthand corner:

![](./media/images/Alexa_Lab_v2_6.png)


9.	Next, **Click on 1. Invocation Name >**

![](./media/images/Alexa_Lab_v2_8.png)

10.	Ensure the skill innvocation name is entered (if not, type:) **voice powered analytics*** (all lower case)

![](./media/images/Alexa_Lab_v2_9.png)

11.	**Click on + Add button** next to Intent.

![](./media/images/Alexa_Lab_v2_10.png)

12.	**Type the custom tntent name** *WhatsMyMetric* and **click Create Custom Intent button**

![](./media/images/Alexa_Lab_v2_11.png)

13.	Next we're going Add utterances to our intent. This triggers an invoke of your intent through your user's voice. You'll want to add a few different variations based upon how users will interact with the different types of metrics available to query.
- **Type the *What’s my {metric}*** (ignore the popup box) and **Click + sign** to add the utterance.

![](./media/images/Alexa_Lab_v2_12.png)

14.	Now we'll configure our Slots. Slots allow you to parameterize different variable attributes when invoking your intent. For this workshop, the slot will be our metric(s) that we've created with the Athena query. This is why we've put the {metric} slot name in our utterances.
- **Click on + Add** on the left menu, next to Slot.

![](./media/images/Alexa_Lab_v2_13.png)

- **Type *available_metrics*** and **click Create custom slot type**

![](./media/images/Alexa_Lab_v2_14.png)

- For the slot value, **enter the value of the metric** used from the *Athena_Poller* Lambda function's environment variable: metric (e.g. *reinvent twitter sentiment*. Then **click the + button**. Note: The DynamoDB item that is used as our key in the backend lambda function uses this value to query our metric's value.

**Note: Don't worry about adding ID (Optional) or Synonyms. They can be added later after you test.**

![](./media/images/Alexa_Lab_v2_15.png)

15.	**Click on *WhatsMyMetric*** on the left menu under Intents. Then **select *available_metrics*** in the dropdown menu next to metric.

![](./media/images/Alexa_Lab_v2_16.png)
16.	Now **click on Build Model**. This will save your model and build it.

![](./media/images/Alexa_Lab_v2_17.png)

- You should see: ![](./media/images/Alexa_Lab_v2_18.png)
- It may take a minute or two to build, if your interaction model builds successfully you'll see a successful build message added to the dialog: ![](./media/images/Alexa_Lab_v2_19.png)

**Troubleshooting** If you get an error from your interaction model, check through this list:
   - Did you copy & paste the provided code into the appropriate boxes?
   - Did you accidentally add any characters to the Interaction Model or Sample Utterances?

In our next step of this guide (Configure Alexa Backend), we will be linking a Lambda function in the AWS developer console.
</details>

### Step 2: Configure Alexa Backend
Now that we've configured the voice interaction, let's set up your Lambda function to be triggered by your Alexa Skills Kit and leverage your DynamoDB metrics.
Note: When you ran the initial setup CloudFormation in Module 1, a Lambda function with the name starting with **::Stack Name::-AlexaMetricSkill** was deployed.
<details>
<summary><strong>Full solution - Setting up Alexa Backend (expand for details)</strong></summary>

1. Check your **AWS region** as the Lambda function needs to be in the same region that your previous resources created in Module 2 were created.

![](./media/images/Alexa_Lab_9.png)

2. **Open the Lambda function, starting with ::Stack Name::-AlexaMetricSkill** that was deployed with the Setup Cloudformation.
  Then we'll **Configure your trigger**: Under Configuration, and in **Add Triggers** pane, **select Alexa Skills Kit** from the list. It will then add this trigger to your Lambda function.

  2a.  **Scroll down to Configure Triggers**, **click  Skill ID verification disable**.   Note: optionally you can use the Alexa SkillID to lock down the lambda function to your specific Alexa Skill; this is a best practice.  Next, click the **Add** button, then scroll to the top of the Lambda function and click **Save**

  ![](./media/images/Alexa_Lab_10.gif)

3. **Copy your Lambda function's ARN value to a separate text editor** The *ARN value* is in the top right corner.  We'll use this in the next section of the guide.

  ![](./media/images/Alexa_Lab_11.png)

  4. Next, **click the Configuration Tab**, then click on the Lambda function icon and name button **.starting with ::Stack Name::-AlexaMetricSkill**  to go back to your code.
  
   ![](./media/images/Alexa_Lab_10a.png)
   
  5.  Scroll down beneath the code and navigate to **Environment Variables**.
  6. **Validate/or change the environment variables**:
    - **intent_name** matches what's configured for your *intent* in the Alexa Skill's Interaction Configuration
    - **slot_name** matches what's configured for your *slot name* in the Alexa Skill's Interaction Configuration
    - (Optional) You can modify the greeting and exit message for your Alexa skill by changing the value of two environment variables: **greeting_msg** and **exit_msg**
  <details>
<summary>Example</summary>

  greeting_msg *Welcome to the Voice Powered Analytics.  Please tell me what metrics you'd like to hear. To hear available metrics, ask Alexa tell me my metrics*
  and
  exit_msg *Thank you for trying the Voice Powered Analytics.  Have a nice day!*
</details>
-  There's also an environment variable called: metrics_table with the value VPA_Metrics_Table.  This references the DynamoDB table that the Alexa skill will be querying for your metric
<details><summary>Hint</summary>

  ![](./media/images/Alexa_Lab_11b.png)
</details>


  7. **Bonus (Time permitting)**: can you add a skill to the Lambda function which enables users to "List My Metrics"
</details>

### Step 3: Connecting Your Voice User Interface to Your Lambda Function

In Step 1 "Setting up Your Voice User Interface", we created a voice user interface for the intents and utterances we expect from our users.

On "Step 2 Configure Alexa Backend", we created a Lambda function that contains all of our logic for the skill.
In this step, we need to connect those two pieces together.
<details>
<summary><strong>Full solution - Connecting VUI to Lambda (expand for details)</strong></summary>

1.	**Go back to the [Amazon Developer Portal](http://developer.amazon.com/)** and **select your skill (*Voice Powered Analytics*)** from the list. You may still have a browser tab open if you started at the beginning of this tutorial.
2.	**Click on Endpoint** on the left menu. Then **Select the AWS Lambda ARN**.

![](./media/images/Alexa_Lab_v2_23.png)

3.	**Paste the ARN** you copied in number 3 of Step 2 to Default Region.

![](./media/images/Alexa_Lab_v2_24.png)

4.	Click **Save Endpoints**

![](./media/images/Alexa_Lab_v2_25.png)

Note: For this skill, we won't be using Account Linking, but you can learn more about [Linking an Alexa User with a User in Your System](https://developer.amazon.com/docs/custom-skills/link-an-alexa-user-with-a-user-in-your-system.html)

5.	Congratulations: You are all set to test your skill.
</details>

### Step 4: Testing Your Alexa Skill
You've now created a Voice User Interface and a Lambda function, and connected the two together. Your skill is now ready to test.
<details>
<summary><strong>Full Solution - Testing Your Alexa Skill</strong></summary>

1.	In the [Amazon Developer Portal](http://developer.amazon.com/), **select your skill (e.g. *Voice Powered Analytics*)** from the list. You may still have a browser tab open if you started at the beginning of this tutorial.
2.	**Click on "Test"** tab on the top.

![](./media/images/Alexa_Lab_v2_26.png)

3.	Enable testing for the skill by clicking slider button

![](./media/images/Alexa_Lab_v2_27.png)

4.	Once enabled, type *“ask Voice Powered Analytics”* and **click the Mic button**

![](./media/images/Alexa_Lab_v2_28.png)

Note: You should see the results on the right window

![](./media/images/Alexa_Lab_v2_29.png)

5.	You can have an entire conversation with your skill with the Service Simulator. Try the following commands:
- *"what is my reinvent twitter sentiment"*
<details>
<summary><strong>Service Simulator Tips</strong></summary>

 - Click the **Listen** button in the bottom right corner to hear Alexa read the response.
 - You can have an entire conversation with your skill with the Service Simulator. Try the following commands:
 - "ask Voice Powered Analytics" then "what is my reinvent twitter sentiment"
</details>
![](./media/images/Alexa_Lab_v2_30.png)

6.  (Optional) Other testing methods to consider:
- [Echosim.io](https://echosim.io/) - a browser-based Alexa skill testing tool that makes it easy to test your skills without carrying a physical device everywhere you go.
- [Unit Testing with Alexa](https://github.com/alexa/skill-sample-nodejs-city-guide/blob/master/unit-testing.md) - a modern approach to unit testing your Alexa skills with [Postman](http://getpostman.com/) and [Amazon API Gateway](http://aws.amazon.com/apigateway).

Note: If your sample skill is working properly, you can now customize your skill.

 #### Troubleshooting
 - If you receive a response that reads: *"The remote endpoint could not be called, or the response it returned was invalid,"* this is an indication that something is broken. Copy the JSON from the Alexa skill and insert it as a test event to our Lambda function **VoiceAlexaSkillFull-AlexaMetricSkill-1**.  You can then see the specific output from the Lambda function as to why it is not executing successfully.
 - It is most likely due to either the Alexa Skills Kit: **slot name** or **intent name** does not match the Lambda environment variables.
- Also make sure that the DynamoDB has an entry with a value for your metric.

</details> 

  
**Thank you Bobby Malik** for his contributions to this section.

### (Optional) Step 5: Deploy to Alexa For Business
To make the skill private for your organization.  You can optionally follow the following steps to deploy: [Alexa For Business](https://github.com/awslabs/voice-powered-analytics/blob/master/README-A4B.md)

### Bonus Step: What Utterances and Intents Are Needed For a "List My Metrics" skill
**Tweet @chadneal and @WestrichAdam** with a description of the custom skill that you've created from this workshop. It may be added below to our **Voice Powered Analytics Attendee Submissions**

<details>
<summary><strong>Hints and Attendee Submissions</strong></summary>
   Intent: ListMetrics
   Utterance(s):
   - ListMetrics List My Metrics
   - ListMetrics What are my metrics
</details>
