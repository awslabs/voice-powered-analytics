##**Note that this workshop is not yet live.  It will be live at reinvent 2017 Wednesday 11/29**

# Workshop Overview
In this workshop you will build a voice powered analytic engine that you can take back to your stakeholders to deliver valuable company insights.   Common questions that may be asked, “Alexa, how many Unique Users did our site have last month?” and “Alexa, how many orders have breached their delivery SLA this week?”.

## Section 2: Alexa Skill Building

Note, that the following dependencies are needed in order to successfully complete this section of the workshop.

- [ ] Successful completion of Athena Query Building Section
- [ ] Amazon Developer account

- [ ] AWS Account with root access or full access
or
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


### Step 1: Setting up Your Voice User Interface

There are two parts to an Alexa skill. The first part is the Voice User Interface (VUI). This is where we define how we will handle a user's voice input, and which code should be executed when specific commands are uttered. The second part is the actual programming logic for our skill.   Both will be configured in this step-by-step guide.<br>
<IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Arch.png?raw=true" width="80%" height="80%"><br><br>
Alexa fits into your Voice Powered Analytics architecture as the interaction interface for retrieving metrics.  Alexa determines what metrics to retrieve through intents (which we'll describe and configure in the next steps).  The intents correspond to metrics in your DynamoDB data store, which Lambda functions retrieve and send back to the Alexa-enabled device to communicate back to the user:<br>
<IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Arch2.png?raw=true" width="80%" height="80%"><br><br>   
<details>
<summary><strong>Full solution - Setting up VUI (expand for details)</strong></summary><p>
  
  1. Go to the <a href="http://developer.amazon.com/" target="_blank">Amazon Developer Portal</a>.  
  2. Click the <b>Alexa button</b> on the left portion of the screen.<br>
  <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_1.png?raw=true" width="80%" height="80%"><br>
  2. In the top-right corner of the screen, click the <b>"Sign In"</b> button. <br>(If you don't already have an account, you will be able to create a new one for free.)<br>
  3. Once you have signed in, on the Alexa page, click the <b>"Alexa Skills Kit"</b> button, which is what we'll use to create our custom skill.<br>
  <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_2.png?raw=true" width="40%" height="40%"><br>
  4.  Select <b>"Start A Skill."</b> This will get you to the first page of your new Alexa skill.
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
8.  Click on the <b>"Dashboard"</b> button.
9.  Click <b>"Add Intent"</b> on the Dashboard screen.  An intent allows you to define 'what to do' when your custom skill is invoked.  
 <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_5_5.png?raw=true" width="80%" height="80%"><br>
10.  Type in a name for the intent under <b> Create a new custom intent</b>  
<IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_5_6.png?raw=true" width="80%" height="80%"><br>
11.  Next we're going <b>Add utterances</b> to our intent.  This triggers an invoke of your intent through your user's voice.  You'll want to add a few different variations based upon how users will interact with the different types of metrics available to query.     
  - Some sample utterances for your newly generated intents. These are the things a user would say to make a specific intent happen. Here are a few examples:
    - <i>What's my {metric}</i> or <i>What is the value for {metric}</i> (More on what the <i>{metric}</i> means on the next step)
    <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_6.png?raw=true" width="80%" height="80%"><br>
12. Now we'll <b>configure our Slots</b>.  Slots allow you to parameterize different variable attributes when invoking your intent.  For this workshop, the slot will be our metric(s) that we've created with the Athena query.  This is why we've put the {metric} slot name in our utterances.
    - Type in the name of the slot under <b>Create a new intent slot</b> and then <b>Click the + button</b> to add it.  Then click the <b>plus(+)</b> button on the utterances dialog to add the utterance.  Give your slot the name {<b>metric</b>}.  Note: If you want to give it a different name, then log the name in a separate text editor so we can adjust our backend Lambda function later.  If you do this, also remember to change the name of the slot referenced in your utterance so they match.        
    - Note: Alternatively, you can create a new slot on the right side of the screen in the section titled <i>Intent Slots</i>
13. Our slot is now created and will be added to the <i>Intent Slots</i> area on the right side of the screen.  In this section, under the slot, click the area <i>choose a slot type</i>. We’ll create a new slot type for our list of metrics.  Let's call this <b>available_metrics</b> and click the <b>+</b> button to add it.<br>
<IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_6_5.png?raw=true" width="80%" height="80%"><br> 
14.  On the bottom left side of the screen, click on the <b>available_metrics</b> slot type that was just created.   Then enter the value of the metric used in the environment variable called <i>Metric</i> from the Athena_Poller lambda function as the <i>slot value</i>. Then click the <b>+</b> button.  Note: The DynamoDB item that is used as our key in the backend lambda function uses this value to query our metric's value.
    - Note: Don't worry about adding <b>ID (Optional)</b> or <b>Synonyms</b>.  They can be added later after you test. 
<IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_6_6.png?raw=true" width="80%" height="80%"><br>
15. Now you're ready to Click <b>"Build Model"</b> and <b>"Save"</b><br>
<IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_7.png?raw=true" width="80%" height="80%"><br>
16. If your interaction model builds successfully, click on <b>Configuration button</b> to move on to Configuration. In our next step of this guide, we will be creating our Lambda function in the AWS developer console, but keep this browser tab open, because we will be returning here on <a href="https://github.com/voicehacks/setup-local-recommendations/blob/master/step-by-step/3-connect-vui-to-code.md">Page #3: Connect VUI to Code</a>. <br>
<IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_8.png?raw=true" width="80%" height="80%"><br>
<br>If you get an error from your interaction model, check through this list:
   - Did you copy & paste the provided code into the appropriate boxes?
   - Did you accidentally add any characters to the Interaction Model or Sample Utterances?
</details>

### Step 2: Configure Alexa Backend
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
<td> <center><a href="https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=VoiceAlexaSkill&templateURL=https://s3.amazonaws.com/cf-templates-kljh22251-eu-west-1/skill_template_partial.yaml"><img src="/media/images/CFN_Image_01.png" alt="Launch Alexa Skill into Ireland with CloudFormation" width="65%" height="65%"></a></center></td></tr></tbody></table>
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
  6.  Also <b>validate the environment variables</b>: 
   - <b>metric_name</b> matches your slot's value(s)
   - <b>intent_name</b> matches what's configured for your <i>intent</i> in the Alexa Skill's Interaction Configuration
   - <b>slot_name</b> matches what's configured for you <i>slot name</i> in the Alexa Skill's Interaction Configuration
   
  7.  We'll also add an environment variable called: <b>metrics_table</b> called <i>VPA_Metrics_Table</i>.  This references the DynamoDB table that the Alexa skill will be querying for your metric 
<details>
<summary>Hint</summary><p>
  <IMG SRC="https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/Alexa_Lab_11b.png?raw=true" width="80%" height="80%">
  </p></details>
  7. Bonus (If time): can you add a skill to the Lambda function which enables users to "List My Metrics"
<details>
<summary>If you couldn't complete the steps for this Section above, optionally, you can deploy the following CloudFormation for the AWS configuration:</summary><p>
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
<b>TODO: 8.  Click on the "<b>Code Editor"</b> item under Dashboard on the top left side of the skill builder.</b>

</details>

### Step 3: Connecting Your Voice User Interface to Your Lambda Function
In Step 1 "Setting up Your Voice User Interface", we created a voice user interface for the intents and utterances we expect from our users. On "Step 2 Configure Alexa Backend", we created a Lambda function that contains all of our logic for the skill. On this page, we need to connect those two pieces together.<br>
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

### Step 4: Testing Your Alexa Skill
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

### Bonus Step: What Utterances and Intents Are Needed For a "List My Metrics" skill
<details>
<summary><strong>Hints</strong></summary><p>
  <br>Intent: ListMetrics
  <br>Utterance(s): 
  <br>- ListMetrics List My Metrics
  <br>- ListMetrics What are my metrics
</p></details>
