Although the cost of this workshop is less than $1 a week, if you'd like to minimize or delete the resources created, this can be done in multiple ways

# Workshop Cleanup options
 * Reduce size of fleet
 * Delete stack through CloudFormation
 * Delete cost components
 
## Reduce Size of Fleet 
1. If you want to keep the main building blocks around, but make it a "colder footprint", you can cleanup through reducing the size of your fleet. 
- The main cost component of this workshop is the DynamoDB ($3.29 + $.25 per GB per month at 5 Reads and 5 Writes).  Since the data size is nominal, you can reduce the footprint to around $~.66 by switching the Read and Write Capacity Units to 1 and 1. 
- To do this, navigate to *Services* > **DynamoDB**.  Then select the **VPA_Metrics** table.  Then navigate to *Capacity* Tab in the right pane.  Then under *Provisioned Capacity*, switch the values to **1 for Read and Write Capacity**, then click **Save**.  
2. Athena and Lambda have a very small cost when run, but no charge when not run. The scheduled *Cloudwatch event* is what triggers both of these services.  This can be disabled by navigating to *Services* > **Cloudwatch**.  Then on the left navigation, under *Events*, choose **Rules**.  Then find the *VPAPoller*, select it, and from *Actions* choose **Disable**.

## Delete Stack Through CloudFormation
If you'd like to delete the components created through the setup template, this can be deleted through **deleting the CloudFormation Stack**.   While many of the components won't result in a charge when sitting idle, deleting through CloudFormation allows for a blank slate.  
![Delete Through Cloudformation](https://github.com/awslabs/voice-powered-analytics/blob/master/media/images/VPA_Cleanup_1.png "Delete Through Cloudformation")

## Delete Cost Components
You can also delete the components manually.  While during the workshop, participants are free to add on additional components, here is a summary of the components to delete:
- [ ] 2 IAM Roles (begining with **VPA**)
- [ ] Athena Table (**Tweets** table under the *default* database)
- [ ] 2 Lambda Functions (Poller and Alexa Skill)
- [ ] DynamoDB Table (VPA_Metrics_Table)
- [ ] Cloudwatch Event

## Modules

You can redo this workshop by going back to any of the main modules:
1. [Voice Powered Analytics](https://github.com/awslabs/voice-powered-analytics/)
