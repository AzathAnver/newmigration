Campaign Management 201 Trafficking \& Mapping

Campaign Management for Reporting \& Advanced Analytics
Lesson 1 of 7
By now you have learned about Campaign Management's structure, how to create campaigns, media plans and plan lines, as well as about the importance of media plan approvals. Now it's time to master the fundamentals of trafficking and mapping in Campaign Management which is crucial to accurately report on campaign performance.

One of the most powerful capabilities of Campaign Management is to centralize and structure data which allows you to provide a unified view of the media budget and prepare meaningful insights in client reporting.

Campaign Management consolidates campaign performance in a single platform, with data coming in from a range of sources.

We generally differentiate between 2 types of data:

1
Performance data

2
Activity data

LET'S TAKE A CLOSER LOOK AT PERFORMANCE DATA

A close-up, side profile view of a human eye, with green digital code and numbers overlaid or reflected on the iris and surrounding skin, suggesting concepts of data, artificial intelligence, or digital vision. The background is a blurred blue and purple gradient
What is performance data?

Performance data such as clicks, impressions, spend, and platform-specific metrics come into our systems via one of the following paths:

Automatically
Campaign Management has API integrations with all major digital platforms across channels as well as the CM360 ad server. Campaign Management users need to follow trafficking and mapping instructions to ensure performance data is collected and reported on correctly.



Manually

For non-integrated platforms or offline campaigns, data needs to be manually uploaded into Campaign Management.

Learn more about this topic in our deep dive training course. You can also find instructions on how to manually upload stats on the

Campaign Management allows users to manually upload data into Campaign Management before the media plan reaches the Reconciled stage and is locked by Client Finance. This is common practice in the following scenarios:



A platform is not integrated with Campaign Management. Fully integrated platforms do not require manual uploads as they are supported by Campaign Management auto-mapping. This means data can be automatically pulled in via mappings. Refer to this knowledge base section for more information on how to correctly map and report on data from platforms that Campaign Management has an API integration with.
To overwrite automatically collected data from Campaign Manager 360 or other platforms.
There are system issues causing data inaccuracies.



This article focuses on describing the steps required to:



manually upload stats into Campaign Management using our GSheet solution
deleting manually uploaded stats
correcting manually uploaded stats
Uploading Stats Manually
To manually upload stats into Campaign Management:



1. Navigate to Campaign Management and click on Apps in the top right corner.



1. Click on Download Manual Upload Template. Here’s the link for you to bookmark.



1. Make a copy of the template and save in your GDrive.



1. Download the GSheet add-on Campaign Management3 Manual Uploads.



1. Authorize your worksheet.



1. Select the GSheet tab based on whether you want to upload stats against Campaign Management placement ID or Campaign Manager 360 placement ID. Please keep in mind the priority order in which Campaign Management decides what data to display in reporting:



Manually uploaded data against Campaign Management Placement ID (OPID)
Data automatically collected from DSPs (e.g. Facebook, DV360, LinkedIn, etc.)
Manually uploaded data against Campaign Manager 360 placement ID
Data automatically collected from the ad server (Campaign Manager 360)

7. Add your supplier stats to the GSheet. Only complete the columns that you want to upload. You can leave unwanted cells blank but ensure that you keep the formatting from the template.



Date: Date of supplier stats (Ensure that your GSheet settings "Locale" are correct and set to your local region. You should input the date using the format that is normally used for your region, e.g. MM/DD/YYYY for NA, DD/MM/YYYY for EMEA.)
Campaign Management Placement Id/DCM Placement Id: Campaign Management Placement ID can be found after the (OPID-xxxx) in the Placement name or in the Placement details screen in Campaign Management. The DCM Placement ID can be found in the Campaign Management DCM T-sheet export after AdOps has created and trafficked the Campaign Manager 360 placements. The DCM Placement Id is in column C of the export.
Impressions: Number of impressions tracked by the supplier.
Clicks: Number of clicks tracked by the supplier.
Cost: Media cost to the supplier.
Input \[n] Name: The input Tag Name as set up on Campaign Management campaign level. This field is case sensitive. \[n] refers to the Campaign Management input number you want to upload stats to.
Input \[n] Type: The input Value Type as set up on Campaign Management campaign level. Select from these options: PC, PI, PC Revenue, PI Revenue.
Input \[n] Value: The number of conversions (count of events) you want to upload.



8. Highlight the cells with values that you want to upload, including the headers.



1. In the GSheet menu, click on Add-ons.



1. Select the Campaign Management Sync with validation add-on.



1. Click on Upload selected stats with validation.



Once data has been uploaded, you will receive a success message on your screen. If the upload was unsuccessful, GSheet cells with errors will be highlighted along with a reason for the error.



It doesn't work?!
Occasionally, the GDoc add-on might get a little glitch and the manual upload doesn't appear to work. If you encounter this problem, please try the following steps:



Authorize your worksheet, following step 5 from these instructions.
Reload your worksheet.
Re-upload your stats.



Watch the tutorial video below for a demo of the manual stats upload feature.

Manual Stats Uploads9:34.
Deep Dive: Manually Uploading Conversions
When manually uploading total conversions into Campaign Management, the upload for PC and PI conversions needs to be done in separate rows of the GSheet. The GSheet add-on will automatically sum up the data for reporting on total conversions. The number of total conversions in the below example will show as 27:

Date	DCM Placement Id	Input 1 Name	Input 1 Type	Input 1 Value
02/21/2020	1234	Buy Now Clicks	PC	7
02/21/2020	1234	Buy Now Clicks	PI	20
The below image shows which fields from the Campaign Management input are required in the GSheet to upload conversion stats:



Deleting Manually Uploaded Stats
To delete previously uploaded data:



1. In the GSheet you have previously used to upload data, select the cells for Dates and IDs you want to delete data for.



1. In the GSheet menu, click on Add-ons.



1. Select the Campaign Management Sync with validation add-on.



1. Click on Delete selected stats.



ALL data for the selected dates and IDs will be deleted. If you would like to delete only certain stats, e.g. impressions only, users will need to manually upload stats for clicks, spend and conversions again, following the steps above.

Correcting Manually Uploaded Stats
To correct previously uploaded data:



1. In the GSheet you have previously used to upload data, correct the data where necessary.



1. Highlight the cells with values that you want to correct, including the headers.



1. In the GSheet menu, click on Add-ons.



1. Select the Campaign Management Sync with validation add-on.



1. Click on Upload selected stats with validation.



This new stats upload will overwrite previously uploaded data. Multiple uploads for the same date and IDs will NOT duplicate data for reporting.

Spend as well as other performance data can also be viewed in your reporting tool of choice, such as Datalab.
You will see spend reflected for example in the spend column in your Campaign Management media plan. Spend data will be either automatically pulled from each platform into Olive, or manually uploaded to Campaign Management by the Activation team.

How does Campaign Management know what campaign or plan line to allocate delivery data to?
Stay tuned! This is what this training is all about. We'll shortly teach you about the concept of mapping and you'll learn about Campaign Management placement which play a crucial role in the mapping process.

How does Campaign Management handle duplicate data?
For example: Clicks \& impressions for your Meta campaign are pulled from both the Meta platform AND CM360, right? Aren't we duplicating data here!?

If Campaign Management receives data such as clicks and impressions for the same campaign from multiple sources, it automatically deduplicates data for reporting based on this hierarchy:

Manually uploaded data against Campaign Management placement ID (OPID)

Data automatically collected from activation platforms (e.g. Meta, DV360, LinkedIn, etc.)

Manually uploaded data against CM360 placement ID

Data automatically collected from the ad server (CM360)

Following this hierarchy, your data from the Meta platform takes priority over that same data from CM360. And manually uploaded stats against Campaign Management placements have the power to overwrite data from all other sources.

You'll learn about Campaign Management placements shortly.

How is spend calculated?

Some platforms don't provide this info, such as ad servers (CM360). So spend in Campaign Management or in your reporting is shown based on the cost model set at the Campaign Management plan line level. There are two types of cost models:

Biddable
Also referred to as variable cost model, and typically used for media that is bought in an auction. As we already learned earlier, spend comes into Campaign Management via one of the following paths:

Automatically: If the 3rd party platform has been integrated with Campaign Management, spend data is collected automatically, provided mappings to Campaign Management are correct. You'll find out more about mapping later in this chapter.

Manually: For non-integrated platforms, data needs to be manually uploaded into Campaign Management. Find out about manual stats upload in our deep dive training course or on the Campaign Management KB(opens in a new tab).

Fixed
Typically used for non-biddable/reserved  or offline media buys for which the platform field on Olive plan line level needs to be set to "Other", as well as for some programmatic guaranteed buys.

Spend is calculated based on the unit cost specified on Olive plan line level and the number of clicks/impressions/conversions tracked in the ad server. The calculations for the available cost models in Olive are:

Fixed CPM: Spend = plan line unit cost \* ad server impressions / 1000

Fixed CPC: Spend = plan line unit cost \* ad server clicks

Fixed CPA: Spend = plan line unit cost \* ad server conversions
An input needs to be set up in Olive to specify which CM360 floodlight tracks the conversions that are needed to calculate spend. Find out more about setting up inputs on the Olive KB(opens in a new tab) (or in the dedicated deep dive eLearning we're launching soon).

Fixed Cost: Spend = plan line budget / number of days within plan line start and end dates
Spend is equally distributed across each associated Olive placement for each day in the plan line date range.





What is activity data?

In short - activity data refers to conversion data. More specifically, there are three types of activity data that is typically added to Campaign Management for reporting purposes:

Conversions tracked via CM360 floodlights
Provided CM360 placements have been correctly mapped to Campaign Management, floodlight-tracked conversions are automatically collected. To report on them in a cross-channel dashboard, you need to set them up as inputs in Campaign Management.



Rich media engagement metrics



Rich media is a term for an ad that includes interactive features such as video, audio etc. that encourage the targeted audience to interact and engage with the content. Their reporting metrics (rich media engagement metrics) can be set up as inputs in Campaign Management for reporting.

Any other conversions
These can be manually uploaded into Campaign Management using “dummy floodlights”. Dummy floodlights are essentially non-trafficked Campaign Management placements; they are not linked to any placements in CM360.



Set up Campaign Management to report on conversions

You can find out more about how to correctly set up Campaign Management to report on conversions. We're also soon going to launch a dedicated eLearning course on the topic.

using inputs to report on conversions
Published 4/9/2025
With inputs, Campaign Management allows users to define conversion metrics for their campaign that are used in reporting as a standalone metric alongside performance data, or to report on a media plan performance goal. There are three (3) scenarios for when to use inputs:



Cross-channel reporting on floodlight-tracked conversions
Reporting on rich media engagement metrics
Reporting on any other metric that Campaign Management doesn’t already collect from an integrated data source (e.g. 1st party data, offline data) can be enabled via dummy floodlights



Up to 45 inputs can be set up on Campaign Management campaign level.



This article describes how to set up inputs and ensure data is collected correctly for the above scenarios.

Floodlight-Tracked Conversions
Provided Campaign Manager 360 placements have been correctly mapped to Campaign Management, floodlight-tracked conversions are automatically collected via the Campaign Manager 360 API that Campaign Management is integrated with. To report on them in a cross-channel dashboard, users need to set them up as inputs in Campaign Management. To do so:



1. Navigate to your Campaign Management campaign.



1. On the right-hand side of the Campaign screen, in the Input section, click on Add first input.



1. In the new window that opens, complete the fields:



Slot: The input number you can use to view your conversion data in Campaign Management Datalab.
Name: Specify a name for your input.
Action Type: Select the type of user action that is tracked by the floodlight tag. If you can’t find the option that best fits your conversion event, select Custom and specify an Action name.
Source: Select the data source of your tracking tag that the conversion data will be collected from. E.g. choose DCM Floodlights for ad server tags, or AdWords Events for Google Ads conversion tags.
Tag Name: Select the Campaign Manager 360 floodlight tag from the dropdown.
Value Type: Select the value type of the conversion event that is being tracked, e.g. Total Conversions, Post Impression, Post Click Revenue
Weight: Set a value between -1 and 1 for composite inputs that contain multiple tags in order to indicate the weight of each, if e.g. one tag is worth more than another. By default, the value is set to 1. Set to -1 if a particular floodlight should be subtracted from the rest, e.g. to calculate signups minus cancellations.
Reporting date: Specify a time range, e.g. when your floodlight tag has changed, and you no longer want to count its value towards the input total.
Add Another Tag: You can choose to add multiple tags. The values tracked for each tag will be summed up to the total input value, taking into account the Weight specified for each tag above.

4. Click on Create Input.

Create inputs in Olive3:26.
Rich Media Engagement Metrics
Rich media is a term for an ad that includes interactive features such as video, audio etc. that encourage targeted users to interact and engage with the content. Their reporting metrics (rich media engagement metrics) can be set up as inputs in Campaign Management for reporting. To do so:



1. Navigate to your Campaign Management campaign.



1. On the right-hand side of the Campaign screen, in the Input section, click on Add first input.



1. In the new window that opens, complete the fields:



Slot: The input number you can use to view your conversion data in Campaign Management Datalab.
Name: Specify a name for your input.
Action Type: Select the type of user action that is tracked by the floodlight tag. If you can’t find the option that best fits your conversion event, select Custom and specify an Action name.
Source: Select DCM Rich Media as the data source of your tracking tag that the conversion data will be collected from.
Tag Name: Select the rich media engagement metric from the dropdown.

Weight: Set a value between -1 and 1 for composite inputs that contain multiple tags in order to indicate the weight of each, if e.g. one tag is worth more than another. By default the value is set to 1. Set to -1 if a particular floodlight should be subtracted from the rest, e.g. to calculate signups minus cancellations.
Reporting date: Specify a time range, e.g. when your floodlight tag has changed and you no longer want to count its value towards the input total.
Add Another Tag: You can choose to add multiple tags. The values tracked for each tag will be summed up to the total input value, taking into account the Weight specified for each tag above.



4. Click on Create Input.

Dummy Floodlights
For users who want to report on any other metric that Campaign Management doesn’t already collect automatically from an integrated data source (e.g. 1st party data, offline conversion data), Campaign Management enables them to manually upload stats for that metric into a dummy floodlight that is linked to an Campaign Management input.



Reporting on metrics from dummy floodlights is a 3-step process:



Request a dummy floodlight from Campaign Management Support
Create your Campaign Management input
Manually upload your stats into the dummy floodlight

1. Requesting a Dummy Floodlight
Dummy floodlights need to be requested from the Campaign Management Support team:



1. Submit a ticket to Campaign Management Support.



1. Include the following information in the ticket:



What Campaign Management client are the dummy floodlights for?
What Campaign Management campaigns will you be using the dummy floodlights for?
Names of your dummy floodlights.
Are the value types of the conversions post-click or post-impression?
2. Creating an Campaign Management Input
Once the dummy floodlights have been created, you can set up your Campaign Management input:



1. Navigate to your Campaign Management campaign.



1. On the right-hand side of the Campaign screen, in the Input section, click on Add first input.



1. In the new window that opens, complete the fields:



Slot: The input number you can use to view your conversion data in Campaign Management Datalab.
Name: Specify a name for your input.
Action Type: Select the type of user action that is tracked by the floodlight tag. If you can’t find the option that best fits your conversion event, select Custom and specify an Action name.
Source: Select Client Events as the data source of your tag.

Tag Name: Select the dummy floodlight name created by Campaign Management Support from the dropdown.
Weight: Set a value between -1 and 1 for composite inputs that contain multiple tags in order to indicate the weight of each, if e.g. one tag is worth more than another. By default the value is set to 1. Set to -1 if a particular floodlight should be subtracted from the rest, e.g. to calculate signups minus cancellations.
Reporting date: Specify a time range, e.g. when your floodlight tag has changed and you no longer want to count its value towards the input total.
Add Another Tag: You can choose to add multiple tags. The values tracked for each tag will be summed up to the total input value, taking into account the Weight specified for each tag above.



4. Click on Create Input.
3. Manual Stats Upload
The final step for reporting on your metric is to manually upload stats for that metric into the dummy floodlight that has been linked to an Campaign Management input in the above steps.



Please refer to the knowledge base article on Manual Stats Upload for instructions.



Introduction to Trafficking \& Mapping
Lesson 2 of 7
Mapping is not to be confused with trafficking:

Trafficking

The process of setting up a campaign within an ad server in order to run activity and capture performance data.

Campaign Management supports with streamlining the campaign trafficking process in CM360. You'll learn the how-to in the next lesson in this course.

Mapping

The process of connecting data sources. Mapping happens after a campaign has been trafficked in the ad server and/or after campaigns have been set up in the activation platforms.



Why do we map?

•
As you have learned, Campaign Management is our proprietary campaign management system that acts as the spine for our operations. However, Campaign Management itself does not contain the actual campaign data like impressions, clicks, spend, conversions, etc. but is rather a conduit into the database where we have collected this data from the various data sources (you have learned about data sources in the previous lesson of this course).

•
The different platforms don't speak to each other; they have nothing in common that allows us to easily compare their data, but Campaign Management allows us to connect them together and report on everything in one place - across all platforms, campaigns and clients, so we can generate a unified view of our spend and campaign performance.

•
Because we are working off this data to distill valuable insights for clients, our data must always be accurate, which is achieved by correctly mapping activation platforms to Campaign Management.

How does it work?

To create this link between the various data sources (e.g. between Campaign Management and the activation platforms, or Campaign Management and CM360), we need one common variable between Campaign Management and the 3rd party systems which in most cases is the Campaign Management placement. The Campaign Management placement acts as the join key to stitch performance data across all our activation platforms to campaign meta data in Campaign Management.

Sometimes we need to find another variable because Campaign Management Placement may not be the most granular level of detail. The below chart provides an overview of platforms that are currently integrated with Campaign Management and on what level they should be mapped to ensure we are automatically associating campaign data to the correct Campaign Management information.



We maintain API integrations with all major digital platforms across channels incl. Google Campaign Manager, Google Search, SA360, DV360, Amazon, Criteo, LinkedIn, Meta, Snapchat, TTD. Once a campaign has been mapped, data will appear in Campaign Management and your dashboards, so you can monitor performance, check pacing, and make optimizations.



AdMob
Mapping Expectations

Via OPID in AdWords ad name, or

CM360 click tracker in destination URL

Scenarios excepted for manual stats uploads

AdMob text ads where the (OPID-xxxx) cannot be used in the ad name to auto-map

campaign management mapping to google ads: admob
Published 4/1/2025
Campaign Management has an integration with Google Ads and receives daily data on the performance of our AdMob campaigns. In order to assign this data to the correct Campaign Management media plan and enable reporting, Media Activation teams need to map their Campaign Management placements to entities of the Google Ads platform.



This article provides instructions for:



onboarding a new Google Ads AdMob account/client to Campaign Management
mapping AdMob to Campaign Management
Account/Client Onboarding
If our agency has won a new client or you’re running an AdMob campaign on the Google Ads platform for an existing client for the first time, the new client account will need to be onboarded to Campaign Management first to ensure we’re collecting its data on a daily basis.



Please reach out to the Choreograph Enablement team and provide them with the following information:



Our agency point of contact
Google Ads parent account name \& ID
Google Ads child account names \& IDs
Onboarding date
Any requirements for backdating data
Confirm that your account has been linked to our agency's MCC (CID 761-762-1486)
Grant Read-only access to our @dp.choreograph.com account for their Google Ads Accounts. You can look up your client-specific service account email in the emDP Starter Kit.



The Choreograph engineering team will then onboard the account to Campaign Management and confirm with you once complete.

Mapping AdMob to Campaign Management
The way of mapping your AdMob data to Campaign Management depends on how your ads are served. You can find mapping instructions for the following options below:



Site-served text ads through Google Ads (click trackers): In the majority of cases, full 3PAS ad serving is not possible for AdMob. In this case you will use impression and/or click trackers that allow those actions on your ads to be tracked centrally alongside any 3PAS media, and is included in the de-duplication and attribution of conversions.
Non ad-served ads (no tracking): This media will not be tracked by our ad server CM360, so it won't be attributed any conversions and will need to rely on its own tracking pixels.
Banner ads served via CM360 (3PAS): Fully ad-served 3PAS ads allow us to manage and control all creative assets across a campaign centrally from our ad server Campaign Manager 360. However, this type of ad serving is uncommon for AdMob campaigns.
Manual mapping: Use this option if you're unable to map via any of the options above.
Site-Served Text Ads
In order to ensure that your AdMob data for site-served ads is correctly mapped to Campaign Management, please follow the below steps:



1. When Campaign Management, set the Platform field to Admob.



1. Create your AdMob campaign and ad groups through the Google Ads interface.



1. Create Campaign Management placements and placement tags. The likely option to select for the trafficking configuration is AdMob - In-app.



1. Export a DCM t-sheet from Campaign Management and request placements to be trafficked in CM360 from our agency AdOps team.



1. Create your text ads in the Google Ads interface and add the click tracker in the Tracking Template field

Non Ad-Served Ads
In order to ensure that your AdMob data for non ad-served ads is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to Admob.



1. Create your AdMob campaign and ad groups through the Google Ads interface.



1. Create Campaign Management placements. The likely option to select for the trafficking configuration is AdMob - App installs or AdMob - App engagement.



1. Create your text ads in the Google Ads interface and map your AdMob entities on either of the below levels:



Include the Campaign Management placement ID (OPID) at the end of the corresponding AdMob ad name in the format Ad name (OPID-XXXXXX).
Include the Campaign Management placement ID (OPID) at the end of the corresponding AdMob ad group Name in the format Ad group name (OPID-XXXXXX).
Fully Ad-Served 3PAS Ads
In order to ensure that your Google Ads Display data for fully ad-served 3PAS ads is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to Admob.



1. Create your AdMob campaign and ad groups through the Google Ads interface.



1. Create Campaign Management placements and placement tags. The likely option to select for the trafficking configuration is AdMob - In-app (3PAS).



1. Export a DCM t-sheet from Campaign Management and request placements to be trafficked in CM360 from our agency AdOps team.



1. Complete any additional documents for our agency AdOps team required for them to create AdMob ads and upload their tags into the Google Ads platform.

Manual Mapping
If you are unable to map your AdMob ads using one of the methods above, you can also map your ads manually to an Campaign Management placement in the Campaign Management platform. To do so:



1. Navigate to your media plan and select Published View.



1. Click on the Placements tab.



1. Use the filter and search bar to find the placement that you want to map an AdMob ad to.



1. Click on the name of the placement to edit it.



1. In the External Platform Mappings section at the bottom of the page, click on Add external platform mapping.



1. In the pop-up window that opens, complete all fields:



Platform: Please select Google Ads.
Entity type: This will be automatically set to Ad.
Google Ads Account: Select the Google Ads account that has been onboarded for your Campaign Management client. Please follow these onboarding instructions if you cannot find your account.
Entity ID: Enter your ad’s ad group ID and ad ID separated by a pipe (|) in the format Ad group ID|Ad ID. You can add multiple AdMob ads to a Campaign Management placement by entering a comma-separated list.

7. Click on Add.

Once mapped, data will be downloaded daily and will be available in Campaign Management as well as in Datalab for reporting and analysis. Check out this knowledge base article for guidance on how to troubleshoot data integrity issues.

AdWords UAC
Mapping Expectations

Account must be onboarded via Choreograph

Via OPID at the end of UAC Campaign name, or

Include OPID in UAC CM360 click tracker

Scenarios excepted for manual stats uploads

ACe campaigns
campaign management mapping to google ads: UAC
Published 4/1/2025
Campaign Management has an integration with the Google Ads platform and is able to download performance data for UAC campaigns on a daily basis. In order to assign this data to the correct Campaign Management media plan and enable reporting, Media Activation teams need to map their Campaign Management placements to UAC entities of the Google Ads platform.



Please note that the Google Ads UAC integration only includes UAC (app campaigns for installs). Data for ACe campaigns is not available via this integration. This means that you will have to manually upload stats for ACe.



This article provides instructions for:



onboarding a new Google Ads UAC account/client to Camapaign Management
mapping Google Ads UAC to Campaign Management
Account/Client Onboarding
If our agency has won a new client or you’re running a UAC campaign on the Google Ads platform for an existing client for the first time, the new client account will need to be onboarded to Campaign Management first to ensure we’re collecting its data on a daily basis.



Please reach out to the Choreograph Enablement team and provide them with the following information:



Our agency point of contact
Google Ads UAC parent account name \& ID
Google Ads UAC child account names \& IDs
Region \& marketplace of the account
Timezone of the account
Onboarding date
Any requirements for backdating data
Confirm that your account has been linked to our agency MCC (CID 761-762-1486)
Grant Read-only access to our @dp.choreograph.com account for their Google Ads Accounts. You can look up your client-specific service account email in the emDP Starter Kit.



The Choreograph engineering team will then onboard the account to Campaign Management and confirm with you once complete.

Mapping Google Ads UAC to Campaign Management
In order to ensure that your Google Ads UAC data is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management lines, set the Platform field to AdWords UAC.



1. Create Campaign Management placements and placement tags.



1. Export a DCM t-sheet from Campaign Management and request placements to be trafficked in CM360 from our agency AdOps team.



1. Apply the following Google Ads UAC campaign settings:



Advertising\_channel: Multi Channel
Advertising\_sub\_channel: Universal App Campaign



5. Map your Google Ads UAC entities on either of the below levels:



Include the Campaign Management placement ID (OPID) at the end of the corresponding UAC CM360 click tracker in the format CM360 click tracker (OPID-XXXXXX).
Include the Campaign Management placement ID (OPID) at the end of the corresponding Google Ads UAC campaign name in the format Campaign name (OPID-XXXXXX).
Once mapped, data will be downloaded daily and will be available in Campaign Management as well as in Datalab for reporting and analysis. Check out this knowledge base article for guidance on how to troubleshoot data integrity issues.



Amazon DSP
Mapping Expectations

Account must be onboarded via Choreograph

Via OPID at the end of Amazon Creative name, or

Via OPID at the end of Amazon Line\_item name

Scenarios excepted for manual stats uploads

When account has not been onboarded to Campaign Management

When integrated spends are zero (Note: Spends on Campaign Management are calculated by Supply Cost + AAP Audience Fee)

Campaign Management has an integration with the Amazon DSP and receives daily data on the performance of our campaigns. In order to assign this data to the correct Campaign Management media plan and enable reporting, Media Activation teams need to map their Campaign Management placements to entities of the Amazon DSP.



This article provides instructions for:



onboarding a new Amazon DSP account/client to Campaign Management
mapping Amazon DSP to Campaign Management
Account/Client Onboarding
If our agency has won a new client or you’re running a campaign on the Amazon DSP for an existing client for the first time, the new client account will need to be onboarded to Campaign Management first to ensure we’re collecting its data on a daily basis.



Please reach out to the Choreograph Enablement team and provide them with the following information:



Our agency's point of contact
Amazon DSP account name \& ID
Amazon DSP advertiser names \& IDs
Region of the account
Timezone of the account
Onboarding date
Any requirements for backdating data
Grant Manager access to our @dp.choreograph.com account for your Amazon DSP advertiser accounts. You can look up your client-specific service account email in the emDP Starter Kit.



The Choreograph engineering team will then onboard the account to Campaign Management and confirm with you once complete.

Mapping Amazon DSP to Campaign Management
In order to ensure that your Amazon DSP data is correctly mapped to Olive, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to Amazon.



1. Create Campaign Management placements and placement tags.



1. Export a DCM t-sheet from Campaign Management and request placements to be trafficked in CM360 from our agency AdOps team.



1. Map your Amazon DSP entities on either of the below levels (in priority order):



Include the Campaign Management placement ID (OPID) at the end of the corresponding Amazon creative name in the format Creative name (OPID-XXXXXX). This is the preferred method of mapping for greater granularity of reporting data.
Include the Campaign Management placement ID (OPID) at the end of the corresponding Amazon line item name in the format Line item name (OPID-XXXXXX). Please ensure to use the same OPID for line items that belong to the same Amazon creative to prevent data duplication issues.

Once mapped, data will be downloaded daily and will be available in Campaign Management as well as in Datalab for reporting and analysis. Check out this knowledge base article for guidance on how to troubleshoot data integrity issues.



Amazon Search
Mapping Expectations

Account must be onboarded via Choreograph

Via OPID at the end of Campaign name

Scenarios excepted for manual stats uploads

Sponsored Brand Video

Sponsored Display Ads

Campaign Management has an integration with Amazon Search and receives daily data on the performance of our campaigns. In order to assign this data to the correct Campaign Management media plan and enable reporting, Media Activation teams need to map their Campaign Management placements to entities of the Amazon Search platform.



Please note that Sponsored Brand Video or Sponsored Display Ads (not DSP) campaigns are not included in this integration. These products were in beta launch when this API integration was developed. This means that you will have to manually upload stats for sponsored brand video and sponsored display campaigns.



This article provides instructions for:



onboarding a new Amazon Search account/client to Campaign Management
mapping Amazon Search to Campaign Management
Account/Client Onboarding
If our agency has won a new client or you’re running a campaign on the Amazon Search platform for an existing client for the first time, the new client account will need to be onboarded to Campaign Management first to ensure we’re collecting its data on a daily basis.



Please reach out to the Choreograph Enablement team and provide them with the following information:



Our agency's point of contact
Your client’s name in Campaign Management
Specify the Amazon Search platform (Sponsored Products or Brands or Both)
Amazon Search account name \& ID
Amazon Search portfolio name \& ID
Region \& marketplace of the account
Timezone of the account
Onboarding date
Any requirements for backdating data - Note that Amazon only hold 60-90 days' worth of historical data at all reporting levels for both SP and SB (except SP campaign level data). Please reach out to your Amazon Rep if you need a greater historical backfill.
Grant Editor access from your MASTER Amazon Advertising Account to our @dp.choreograph.com account. You can look up your client-specific service account email in the emDP Starter Kit. Note that you need to link all subsequent accounts to your MASTER account.
Limitation on data retention from platform.



The Choreograph engineering team will then onboard the account to Campaign Management and confirm with you once complete.

Onboarding a New Amazon Search Account for Google
Due to the vast amount of data we collect for Google on Amazon Search campaigns, we have already built integrations to the regional Amazon Search master accounts below. If you would like to onboard a new Amazon Search account for Google, simply link your new account to one of the regional master accounts. No separate onboarding request to the Choreograph team is needed, and you can proceed straight away to the mapping instructions below.



EMEA: EMEA Manager Account Google
Admin: naomi.boonin@essenceglobal.com, malina.zarb@essenceglobal.com, essence.googleemea@service.2sixty.io

NA: B2C - APAC
Admin: brigitte.lee@essenceglobal.com, essence.googleapac@service.2sixty.io

NA: tbc
Mapping Amazon Search to Campaign Management
In order to ensure that your Amazon Search data is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to Amazon Search.



1. Create Campaign Management placements and placement tags.



1. Export a DCM t-sheet from Campaign Management and request placements to be trafficked in CM360 from our agency AdOps team.



1. Map your Amazon Search entities on either of the below levels:



Include the Campaign Management placement ID (OPID) at the end of the corresponding Amazon Sponsored Product campaign name in the format Campaign name (OPID-XXXXXX).
Include the Campaign Management placement ID (OPID) at the end of the corresponding Amazon Sponsored Brands campaign name in the format Campaign name (OPID-XXXXXX).
Once mapped, data will be downloaded daily and will be available in Campaign Management as well as in Datalab for reporting and analysis. Check out this knowledge base article for guidance on how to troubleshoot data integrity issues.

Criteo
Mapping Expectations

Via OPID at the end of the corresponding Criteo campaign name

Scenarios excepted for manual stats uploads

none
Campaign Management has an integration with Criteo and receives daily data on the performance of our campaigns. In order to assign this data to the correct Campaign Management media plan and enable reporting, Media Activation teams need to map their Campaign Management placements to entities of the Criteo platform.



This article provides instructions on how to map Criteo to Campaign Management.

Mapping Criteo to Campaign Management
In order to ensure that your Criteo data is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to Criteo.



1. Create Campaign Management placements and placement tags.



1. Export a DCM t-sheet from Campaign Management and request placements to be trafficked in CM360 from our agency AdOps team.



1. Include the Campaign Management placement ID (OPID) at the end of the corresponding Criteo campaign name in the format Campaign name (OPID-XXXXXX).

Once mapped, data will be downloaded daily (follow this link for info on data availability), and will be available in Campaign Management as well as in Datalab for reporting and analysis. Check out this knowledge base article for guidance on how to troubleshoot data integrity issues.

DV360
Mapping Expectations

Include CM360 click tracker in “dcm\_placement\_id” field (preferred), or

Via OPID at the end of the DV360 ad name

Scenarios excepted for manual stats uploads

Tracking Creatives

ampaign Management has an integration with DV360 and receives daily data on the performance of our campaigns. In order to assign this data to the correct Campaign Management media plan and enable reporting, Media Activation teams need to map their Campaign Management placements to entities of the DV360 platform.



Please note that data for TrueView is not available through the DV360 integration but through our YouTube (TrueView) integration only. The DV360 integration also doesn't include data for Tracking Creatives. This means that you will have to manually upload stats for Tracking Creatives.



This article provides instructions for:



onboarding a new DV360 account/client to Campaign Management
mapping DV360 to Campaign Management
Account/Client Onboarding
If our agency has won a new client or you’re running a campaign on the DV360 platform for an existing client for the first time, the new client account will need to be onboarded to Campaign Management first to ensure we’re collecting its data on a daily basis.



Please reach out to the Choreograph Enablement team and provide them with the following information:



Our agency point of contact
DV360 partner name \& ID
Onboarding date
Any requirements for backdating data; please provide the date (Note to Choreograph team: this requires a separate ticket)
Grant Read-only access to our @dp.choreograph.com account for your DV360 Partner Accounts. You can look up your client-specific service account email in the emDP Starter Kit.



The Choreograph engineering team will then onboard the account to Campaign Management and confirm with you once complete.

Mapping DV360 to Campaign Management
There are two (2) ways of mapping DV360 to Campaign Management, depending on how DV360 creatives are created:



Automatically: DV360 creatives are typically automatically generated when our agency's AdOps team traffics CM360 placements which results in automated mapping between Campaign Management and DV360.
Manually: Creating DV360 creatives manually is common practice for Celtra or MOAT. You may choose to manually upload data against the Campaign Management placement or alternatively follow the mapping instructions below.
Mapping Instructions for Automatically Generated DV360 Creatives
In order to ensure that your DV360 data from automatically generated creatives is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to DBM.



1. Create Campaign Management placements and placement tags.



1. Export a DCM t-sheet from Campaign Management and request placements to be trafficked in CM360 from our agency's AdOps team. This will generate DV360 creatives that are automatically mapped to Campaign Management placements.

Mapping Instructions for Manually Generated DV360 Creatives
In order to ensure that your DV360 data from manually generated creatives is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to DBM.



1. Create Campaign Management placements and placement tags.



1. Export a DCM t-sheet from Campaign Management and request placements to be trafficked in CM360 from our agency's AdOps team.



1. Create your DV360 creatives and include the Campaign Management placement ID (OPID) at the end of the corresponding DV360 creative name in the format Creative name (OPID-XXXXXX).

Once mapped, data will be downloaded daily and will be available in Campaign Management as well as in Datalab for reporting and analysis. Check out this knowledge base article for guidance on how to troubleshoot data integrity issues.

CM360
Mapping Expectations

Via OPTID in external placement ID field

Scenarios excepted for manual stats uploads

none

This article describes the steps required in Campaign Management to:



onboarding a new CM360 account to Campaign Management
traffic placements in Campaign Manager 360, and
map Campaign Manager 360 placements to Campaign Management placement tags
Account Onboarding
If EssenceMediacom has won a new client, the new CM360 account will need to be onboarded to Campaign Management first to ensure we’re collecting its data on a daily basis.



Please reach out to our Choreograph team and provide them with the following information:



EssenceMediacom point of contact
CM360 network and parent advertiser
CM360 account name \& ID
Onboarding date
Any requirements for backdating data
Grant Read-only access to our @auth.groupm.tech or @auth.choreograph account for your CM360 Accounts. You can look up your client-specific service account email in the emDP Starter Kit.



The Choreograph engineering team will then onboard the account to Campaign Management and confirm with you once complete.

Trafficking Campaign Manager 360 Placements
Mapping is not to be confused with trafficking:



Trafficking: The process of setting up a campaign within an ad server in order to run activity and capture performance data.
Mapping: The process of connecting data sources. Mapping happens after a campaign has been trafficked.



In order to create Campaign Manager 360 placements, ads and creatives, a trafficking sheet (t-sheet) needs to be prepared for each Campaign Management media plan and submitted to Essence AdOps via a Jira ticket for trafficking. The t-sheet provides AdOps all the info they need to traffic Campaign Manager 360 placements which will then be mapped to Campaign Management placement tags. This is essential for cross-channel reporting.



To prepare the trafficking sheet for AdOps:



1. Create Campaign Management placements and placement tags. Refer to this knowledge base article for instructions.



1. Select the Published View of your media plan.



1. Click on the Placements tab.



1. Click on Export.



1. Select DCM T Sheet - for AdOps (All) from the dropdown. A csv file will be downloaded that includes one row per user-requested Campaign Manager 360 placement which relates to one Campaign Management Placement tag. If your media plan has more than 10,000 placements, the csv export will be emailed to you.



1. In the trafficking sheet from AdOps, complete the following information in the T-sheet tab:



Copy/paste the placement names from the csv file (column E) into column C of the t-sheet.
Copy/paste the site names from the csv file (column B) into column A of the t-sheet.
Copy/paste the Campaign Management placement tag ID (OPTID) from the csv file (column D) into column B of the t-sheet.
Copy/paste the dimensions from the csv file (column K) into column D of the t-sheet.



7. Complete all other columns and tabs in the trafficking sheet.



1. Submit both the CSV file and trafficking sheet to AdOps in a Jira ticket for trafficking.



1. AdOps creates and traffics the campaigns and placements in Campaign Manager 360. If any changes to Campaign Management placements are being made, please submit an updated trafficking sheet to AdOps.

Create and traffic placements in CM3606:05.
Mapping Campaign Management to Campaign Manager 360
To map Campaign Management to Campaign Manager 360, one Campaign Management placement tag is linked to one Campaign Manager 360 placement. The below graph shows the relationship between entities in Campaign Management and Campaign Manager 360.



Campaign Management placement tags can be mapped to Campaign Manager 360 placements via two (2) methods:



automatically
manually

Automatically Mapping Campaign Management to Campaign Manager 360
Once Campaign Manager 360 placements have been trafficked following the instructions above in this article, Campaign Manager 360 placements are automatically mapped to Campaign Management placement tags via the external ID (Campaign Management placement tag ID, OPTID). No further action to map the two data sources is needed.



Manually Mapping Campaign Management to Campaign Manager 360
There may be (rare) cases in which placements have been created and trafficked in Campaign Manager 360, however they do not include the external ID and hence cannot be automatically mapped to an Campaign Management placement tag. In those cases, Campaign Management allows users to manually map a Campaign Manager 360 placement to a Campaign Management placement.



To manually map Campaign Management to Campaign Manager 360:



1. Navigate to your media plan and select Published View.



1. Click on the Placements tab.



1. Click on the name of the placement you want to map to a Campaign Manager 360 placement. The Placement Details page opens.



1. In the Placement Tags section, click on Add DCM placement mapping.



1. Enter the ID of the Campaign Manager 360 placement.



1. Click on Find. The Campaign Manager 360 placement will be mapped to the Campaign Management placement and a new Campaign Management placement tag will be generated.

Facebook
Mapping Expectations

Via OPID at the end of Facebook Ad name, or

CM360 click tracker in external URL field

Scenarios excepted for manual stats uploads

If all clicks / app clicks need to be taken into account instead of link clicks

Campaign Management has an integration with Facebook \& Instagram (selected Instagram dimensions only) and receives daily data on the performance of our campaigns. In order to assign this data to the correct Campaign Management media plan and enable reporting, Media Activation teams need to map their Campaign Management placements to entities of the Facebook platform.



Please note that the cross-channel dashboard in Datalab includes link clicks (to the landing page) instead of ad clicks. You won't need to manually upload link click data for reporting.



This article provides instructions for:



onboarding a new Facebook account/client to Campaign Management
mapping Facebook to Campaign Management
Account/Client Onboarding
If our agency has won a new client or you’re running a campaign on the Facebook platform for an existing client for the first time, the new client account will need to be onboarded to Campaign Management first to ensure we’re collecting its data on a daily basis.



To onboard data for a new ad account:



1. Link your new FB/Meta accounts to our FB Business Manager Organization GroupM Data and Technology (697575350851112).



1. Grant Analyst (View Reports) access to our @dp.choreograph.com account for both the Platform and the Business Manager. You can look up your client-specific service account email in the emDP Starter Kit.



1. Submit a ticket to our Campaign Management Support team to complete data onboarding.



The Choreograph engineering team will then onboard the account to Campaign Management and confirm with you once complete.

Mapping Facebook to Campaign Management
In order to ensure that your Facebook data is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to Facebook.



1. Create Campaign Management placements and placement tags.



1. Export a DCM t-sheet from Campaign Management and request placements to be trafficked in CM360 from our agency AdOps team.



1. Map your Facebook entities on either of the below levels (in priority order):



Include the Campaign Management placement ID (OPID) at the end of the corresponding Facebook ad name in the format Ad name (OPID-XXXXXX). This is the preferred method of mapping for greater granularity of reporting data.

Insert the Campaign Manager 360 click tracker into the external URL field of your Facebook ads.
Manual Mapping
If you are unable to map your Facebook ads using one of the methods above, you can also map your ads manually to an Campaign Management placement in the Campaign Management platform. To do so:



1. Navigate to your media plan and select Published View.



1. Click on the Placements tab.



1. Use the filter and search bar to find the placement that you want to map a Facebook ad to.



1. Click on the name of the placement to edit it.



1. In the External Platform Mappings section at the bottom of the page, click on Add external platform mapping.



1. In the pop-up window that opens, complete all fields:



Platform: Please select Facebook.
Entity type: This will be automatically set to Ad.
Entity ID: Enter your Facebook ad ID. You can add multiple Facebook ads to an Campaign Management placement by entering a comma-separated list.

7. Click on Add.

Once mapped, data will be downloaded daily and will be available in Campaign Management as well as in Datalab for reporting and analysis. Check out this knowledge base article for guidance on how to troubleshoot data integrity issues.



Google Ads Display
Mapping Expectations

Include the CM360 click tracker in “CreativeTrackingUrlTemplate” field (preferred), or

Via OPID at the end of the Google Ads ad name

Scenarios excepted for manual stats uploads

Sometimes in case of "Unknown Ads" \& Performance Max (PMax) campaigns



Campaign Management has an integration with Google Ads and receives daily data on the performance of our display (GDN) campaigns. In order to assign this data to the correct Campaign Management media plan and enable reporting, Media Activation teams need to map their Campaign Management placements to entities of the Google Ads platform.



This article provides instructions for:



onboarding a new Google Ads Display account/client to Campaign Management
mapping Google Ads Display to Campaign Management
Account/Client Onboarding
If our agency has won a new client or you’re running a display campaign on the Google Ads platform for an existing client for the first time, the new client account will need to be onboarded to Campaign Management first to ensure we’re collecting its data on a daily basis.



Please reach out to the Choreograph Enablement team and provide them with the following information:



Our agency point of contact
Google Ads parent account name \& ID
Google Ads child account names \& IDs
Region \& marketplace of the account
Timezone of the account
Onboarding date
Any requirements for backdating data
Confirm that your account has been linked to our agency MCC (CID 761-762-1486)
Grant Read-only access to our @dp.choreograph.com account for their Google Ads Accounts. You can look up your client-specific service account email in the emDP Starter Kit.



The Choreograph engineering team will then onboard the account to Campaign Management and confirm with you once complete.

Mapping Google Ads Display to Campaign Management
The way of mapping your Google Ads Display data to Campaign Management depends on how your ads are served. You can find mapping instructions for the following options below:



Banner ads served via CM360 (3PAS): Fully ad-served 3PAS ads are the preferred option, as it allows us to manage and control all creative assets across a campaign centrally from our ad server Campaign Manager 360.
Site-served text ads through Google Ads (click trackers): If full 3PAS ad serving is not possible, you should use impression and/or click trackers. Using click and impression trackers allows those actions on your ads to be tracked centrally alongside all 3PAS media, and is included in the de-duplication and attribution of conversions.
Non ad-served ads (no tracking): This media will not be tracked by our ad server CM360, so it won't be attributed any conversions and will need to rely on its own tracking pixels.
Manual mapping: Use this option if you're unable to map via any of the options above.
Fully Ad-Served 3PAS Ads
In order to ensure that your Google Ads Display data for fully ad-served 3PAS ads is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to GDN.



1. Create your Google Ads campaign and ad groups through the Google Ads interface.



1. Create Campaign Management placements and placement tags. Likely options to select for the trafficking configuration are GDN - Display (3PAS) or GDN - In-stream non-skippable video (3PAS).



1. Export a DCM t-sheet from Campaign Management and request placements to be trafficked in CM360 from our agency AdOps team.



1. Complete any additional documents for our agency AdOps team required for them to create Google Ads display ads and upload their tags into the Google Ads platform.

Site-Served Text Ads
In order to ensure that your Google Ads Display data for site-served ads is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to GDN.



1. Create your Google Ads campaign and ad groups through the Google Ads interface.



1. Create Campaign Management placements and placement tags. Likely options to select for the trafficking configuration are GDN - Text ad or GDN - Non full ad-served.



1. Export a DCM t-sheet from Campaign Management and request placements to be trafficked in CM360 from our agency AdOps team.



1. Create your text ads in the Google Ads interface and add the click tracker in the Tracking Template field.



Non Ad-Served Ads
In order to ensure that your Google Ads Display data for non ad-served ads is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to GDN.



1. Create your Google Ads campaign and ad groups through the Google Ads interface.



1. Create Campaign Management placements. The likely option to select for the trafficking configuration is GDN - Non ad-served.



1. Create your text ads in the Google Ads interface and map your Google Ads Display entities on either of the below levels:



Include the Campaign Management placement ID (OPID) at the end of the corresponding Google Ads Display ad name in the format Ad name (OPID-XXXXXX).
Include the Campaign Management placement ID (OPID) at the end of the corresponding Google Ads Display ad group name in the format Ad group name (OPID-XXXXXX).

Manual Mapping
If you are unable to map your Google Ads Display ads using one of the methods above, you can also map your ads manually to an Campaign Management placement in the Campaign Management platform. To do so:



1. Navigate to your media plan and select Published View.



1. Click on the Placements tab.



1. Use the filter and search bar to find the placement that you want to map a Google Ads Display ad to.



1. Click on the name of the placement to edit it.



1. In the External Platform Mappings section at the bottom of the page, click on Add external platform mapping.



1. In the pop-up window that opens, complete all fields:



Platform: Please select Google Ads.
Entity type: This will be automatically set to Ad.
Google Ads Account: Select the Google Ads account that has been onboarded for your Campaign Management client. Please follow these onboarding instructions if you cannot find your account.
Entity ID: Enter your ad’s ad group ID and ad ID separated by a pipe (|) in the format Ad group ID|Ad ID. You can add multiple Google Ads ads to an Campaign Management placement by entering a comma-separated list.

7. Click on Add.

Once mapped, data will be downloaded daily and will be available in Campaign Management as well as in Datalab for reporting and analysis. Check out this knowledge base article for guidance on how to troubleshoot data integrity issues.

LinkedIn
Mapping Expectations

Account must be onboarded via Choreograph

Via OPID at end of LinkedIn Ad name, or

Via OPID  at end of LinkedIn Campaign name

Scenarios excepted for manual stats uploads

Text ads / Dynamic ads / spotlights ad formats



Campaign Management has an integration with LinkedIn and receives daily data on the performance of our campaigns. In order to assign this data to the correct Campaign Management media plan and enable reporting, Media Activation teams need to map their Campaign Management placements to entities of the LinkedIn platform.



Please note that the ad formats Dynamic and Spotlight ad formats are not currently available through the LinkedIn API. This means that you will have to manually upload stats against placements. One placement corresponds to one LinkedIn ad for these formats.



This article provides instructions for:



onboarding a new LinkedIn account/client to Campaign Management
mapping LinkedIn to Campaign Management
Account/Client Onboarding
If our agency has won a new client or you’re running a campaign on the LinkedIn platform for an existing client for the first time, the new client account will need to be onboarded to Campaign Management first to ensure we’re collecting its data on a daily basis.



The below instructions cover the "old" process for onboarding new LinkedIn accounts, as well as the new route via LinkedIn's Business Manager.

"Old" Account Onboarding Process
Please reach out to the Choreograph Enablement team and provide them with the following information:



Our agency point of contact
LinkedIn account name \& ID
Region of the account
Timezone of the account
Onboarding date
Any requirements for backdating data
Grant Viewer access to our LinkedIn Profile from your required Ad Account Profiles. Please reach out to Choreograph for the 'LinkedIn Profile Name' specific to your client, agency or market at the time of onboarding and we will send you the link to our profile.



The Choreograph engineering team will then onboard the account to Campaign Management and confirm with you once complete.

Onboarding Process via LinkedIn Business Manager
To onboard data for a new ad account:



Link your new accounts to the Choreograph Partner ID in your Business Manager (ID: 6975430175245160449). Please refer to this document for instructions.
Grant Viewer access for the Choreograph partner ID.
Submit a ticket to our Campaign Management Support team to complete data onboarding.



The Choreograph engineering team will then onboard the account to Campaign Management and confirm with you once complete.

Mapping LinkedIn to Campaign Management
In order to ensure that your LinkedIn data is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to LinkedIn.



1. Create Campaign Management placements and placement tags.



1. Export a DCM t-sheet from Campaign Management and request placements to be trafficked in CM360 from our agency AdOps team.



1. Map your LinkedIn entities on either of the below levels (in priority order):



Include the Campaign Management placement ID (OPID) at the end of the corresponding LinkedIn creative name in the format Creative name (OPID-XXXXXX). This is the preferred method of mapping for greater granularity of reporting data.

Include the Campaign Management placement ID (OPID) at the end of the corresponding LinkedIn campaign name in the format Campaign name (OPID-XXXXXX).

Once mapped, data will be downloaded daily and will be available in Campaign Management as well as in Datalab for reporting and analysis. Check out this knowledge base article for guidance on how to troubleshoot data integrity issues.
Snapchat
Mapping Expectations

Account must be onboarded via Choreograph

Via OPID at the end of the Snapchat Ad name (preferred), or

Via OPID at end of Snapchat Ad Set name

Scenarios excepted for manual stats uploads

none

campaign Management has an integration with Snapchat and receives daily data on the performance of our campaigns. In order to assign this data to the correct Campaign Management media plan and enable reporting, Media Activation teams need to map their Campaign Management placements to entities of the Snapchat platform.



This article provides instructions for:



onboarding a new Snapchat account/client to Campaign Management
mapping Snapchat to Campaign Management
Account/Client Onboarding
If our agency has won a new client or you’re running a campaign on the Snapchat platform for an existing client for the first time, the new client account will need to be onboarded to Campaign Management first to ensure we’re collecting its data on a daily basis.



Please reach out to the Choreograph Enablement team and provide them with the following information:



Our agency point of contact
Snapchat account name \& ID
Region of the account
Timezone of the account
Onboarding date
Any requirements for backdating data
Grant Data Analyst access to our @dp.choreograph.com account for your Snapchat Ad Accounts. You can look up your client-specific service account email in the emDP Starter Kit.



The Choreograph engineering team will then onboard the account to Campaign Management and confirm with you once complete.

Mapping Snapchat to Campaign Management
In order to ensure that your Snapchat data is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to Snapchat.



1. Create Campaign Management placements and placement tags.



1. Export a DCM t-sheet from Campaign Management and request placements to be trafficked in CM360 from our agency AdOps team.



1. Map your Snapchat entities on either of the below levels (in priority order):



Include the Campaign Management placement ID (OPID) at the end of the corresponding Snapchat ad name in the format Ad name (OPID-XXXXXX). This is the preferred method of mapping for greater granularity of reporting data.

Include the Campaign Management placement ID (OPID) at the end of the corresponding Snapchat ad set name in the format Ad squad name (OPID-XXXXXX).
Once mapped, data will be downloaded daily and will be available in Campaign Management as well as in Datalab for reporting and analysis. Check out this knowledge base article for guidance on how to troubleshoot data integrity issues.

SA360
Mapping Expectations

Mapping SA360 Account to Campaign Management Insertion Order

Mapping SA360 Campaign to Campaign Management Plan Lines

Scenarios excepted for manual stats uploads

none
Campaign Management has an integration with Google SA360 and receives daily data on the performance of our search campaigns. In order to assign this data to the correct Campaign Management media plan and enable reporting, Media Activation teams need to map Campaign Management entities to entities of SA360.



This article provides instructions for:



onboarding a new SA360 agency to Campaign Management
mapping SA360 to Campaign Management
Agency Onboarding
If our agency has won a new client or you’re running a campaign on SA360 for an existing client for the first time, the new client account will need to be onboarded to Campaign Management first to ensure we’re collecting its data on a daily basis.



Please reach out to the Choreograph Enablement team and provide them with the following information:



Our agency point of contact
SA360 agency name \& ID
SA360 advertiser names \& IDs
Region of the account
Timezone of the account
Any requirements for backdating data
Grant Read-only access to our @dp.choreograph.com account for your SA360 Accounts. You can look up your client-specific service account email in the emDP Starter Kit.



The Choreograph engineering team will then onboard the account to Campaign Management and confirm with you once complete.

Mapping SA360 to Campaign Management
Unlike most other integrated platforms, mapping SA360 to Campaign Management is a manual process that consists of two (2) major steps which are explained below:



Mapping SA360 account(s) to a Campaign Management insertion order
Mapping SA360 campaign(s) to a Campaign Management plan line

1. Mapping SA360 Account(s) to an Campaign Management IO
Once you have your SA360 account, campaigns and keywords set up in the SA360 platform, please follow the below steps to map your account(s) to an Campaign Management insertion order:



1. Log into Campaign Management.



1. Click on the menu icon in the top-left corner.



1. Select All campaigns.



1. Use the search bar to find the Campaign Management campaign you want to map SA360 to.



1. Click on the name of your Campaign Management campaign.



1. On top of the page, toggle to Media Plans



1. Click on the name of the media plan you want to create SA360 mappings for.



1. Select the Published View of your media plan.



1. Click on the Insertion orders tab.



1. Find the Campaign Management insertion order for SA360 that you want to create mappings for and click on the insertion order name.



1. On the new page that opens, in the External platforms section, click on Add external platform.



1. Select the SA360 account you want to link to this Campaign Management IO.



1. Click Save.



1. Repeat steps 11 - 13 for each SA360 account that you want to link to this Campaign Management IO.
2. Mapping SA360 Campaign(s) to an Campaign Management Plan Line
Continuing from the previous step, please follow the below instructions to link the SA360 campaigns that belong to the already mapped SA360 accounts to your Campaign Management plan lines:



1. In your Campaign Management insertion order, in the Plan lines section, select the first plan line that needs to be linked to SA360 campaigns and click on Manage mappings.



1. On the new page that opens, select all SA360 campaigns that you want to link to this Campaign Management plan line.



1. Click on Save.



1. Repeat steps 1 to 3 for all other Campaign Management plan lines belonging to this Campaign Management IO that need to be linked to SA360 campaigns.

Once mapped, data will be downloaded daily and will be available in Campaign Management as well as in Datalab for reporting and analysis. Check out this knowledge base article for guidance on how to troubleshoot data integrity issues.



Twitter (X)
Mapping Expectations

Account must be onboarded via Choreograph

Include the CM360 tracking tag in the “DoubleClick tracking” field of the platform, or

Via OPID at the end of the Twitter campaign name

Scenarios excepted for manual stats uploads

In-stream video ad format

App clicks / all clicks

Campaign Management has an integration with Twitter and receives daily data on the performance of our campaigns. In order to assign this data to the correct Campaign Management media plan and enable reporting, Media Activation teams need to map their Campaign Management placements to entities of the Twitter platform.



Please note that the ad format In-stream video is not currently available through the Twitter API. This means that you will have to manually upload stats against placements. One placement corresponds to one Twitter ad group for these formats.



If you wish to report on link clicks (to the landing page), these are available in the cross-channel dashboard in Datalab instead of ad clicks. You won't need to manually upload link click data for reporting.



This article provides instructions for:



onboarding a new Twitter account/client to Campaign Management
mapping Twitter to Campaign Management
Account/Client Onboarding
If our agency has won a new client or you’re running a campaign on the Twitter platform for an existing client for the first time, the new client account will need to be onboarded to Campaign Management first to ensure we’re collecting its data on a daily basis.



Please reach out to the Choreograph Enablement team and provide them with the following information:



Our agency point of contact
Twitter account names \& IDs
Region of the account
Timezone of the account
Onboarding date
Any requirements for backdating data
Grant Campaign Analyst access to our @dp.choreograph.com account for your Twitter Ad Accounts. You can look up your client-specific service account email in the emDP Starter Kit.



The Choreograph engineering team will then onboard the account to Campaign Management and confirm with you once complete.

Mapping Twitter to Campaign Management
In order to ensure that your Twitter data is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to Twitter.



1. Create Campaign Management placements and placement tags.



1. Export a DCM t-sheet from Campaign Management and request placements to be trafficked in CM360 from our agency AdOps team.



1. Map your Twitter entities on either of the below levels (in priority order):



Include the CM360 impression tracker in the DoubleClick tracking field in the Ad group details section of your Twitter Ads Manager. This is the preferred method of mapping for greater granularity of reporting data.

Include the Campaign Management placement ID (OPID) at the end of the corresponding Twitter campaign name in the format Campaign name (OPID-XXXXXX).
Once mapped, data will be downloaded daily and will be available in Campaign Management as well as in Datalab for reporting and analysis. Check out this knowledge base article for guidance on how to troubleshoot data integrity issues.

YouTube
Mapping Expectations

Include the CM360 click tracker in “CreativeTrackingUrlTemplate” field (preferred), or

Via OPID at the end of the Google Ads ad name

Scenarios excepted for manual stats uploads

TrueView Creatives (TrV)

Campaign Management has an integration with Google Ads and receives daily data on the performance of our YouTube (TrueView) campaigns. In order to assign this data to the correct Campaign Management media plan and enable reporting, Media Activation teams need to map their Campaign Management placements to entities of the Google Ads platform.



This article provides instructions for:



onboarding a new YouTube account/client to Campaign Management
mapping TrueView to Campaign Management
Account/Client Onboarding
If our agency has won a new client or you’re running a TrueView campaign on the Google Ads platform for an existing client for the first time, the new client account will need to be onboarded to Campaign Management first to ensure we’re collecting its data on a daily basis.



Please reach out to the Choreograph Enablement team and provide them with the following information:



Our agency point of contact
Google Ads parent account name \& ID
Google Ads child account names \& IDs
Onboarding date
Any requirements for backdating data
Confirm that your account has been linked to our agency MCC (CID 761-762-1486)
Grant Read-only access to our @dp.choreograph.com account for their Google Ads Accounts. You can look up your client-specific service account email in the emDP Starter Kit.



The Choreograph engineering team will then onboard the account to Campaign Management and confirm with you once complete.

Mapping TrueView to Campaign Management
The way of mapping your TrueView data to Campaign Management depends on whether or not you are using Campaign Manager click trackers to track performance of your campaign. You can find mapping instructions for the following options below:



Click trackers: Use this method to map in-stream ads.
No click trackers: Use this method to map app installs or in-display ads.
Manual mapping: Use this option if you're unable to map via any of the options above.
TrueView In-Stream (Click Trackers)
In order to ensure that your TrueView data is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to YouTube.



1. Create your TrueView campaign and ad groups through the Google Ads interface.



1. Create Campaign Management placements and placement tags. The likely option to select for the trafficking configuration is YouTube - In-stream with placement type In-Stream (Skippable).



1. Export a DCM t-sheet from Campaign Management and request placements to be trafficked in CM360 from our agency AdOps team.



1. Create your TrueView in-stream ads in the Google Ads interface and add the click tracker in the Tracking Template field.



TrueView In-Display \& App Installs (No Click Trackers)
In order to ensure that your TrueView data is correctly mapped to Campaign Management, please follow the below steps:



1. When creating Campaign Management plan lines, set the Platform field to YouTube.



1. Create your TrueView campaign and ad groups through the Google Ads interface.



1. Create Campaign Management placements. Likely options to select for the trafficking configuration are TrueView - In-display or TrueView App installs.



1. Create your TrueView ads in the Google Ads interface and map your TrueView entities on either of the below levels:



Include the Campaign Management placement ID (OPID) at the end of the corresponding TrueView ad name in the format Ad name (OPID-XXXXXX).
Include the Campaign Management placement ID (OPID) at the end of the corresponding TrueView ad group Name in the format Ad group name (OPID-XXXXXX).
Manual Mapping
If you are unable to map your TrueView ads using one of the methods above, you can also map your ads manually to an Campaign Management placement in the Campaign Management platform. To do so:



1. Navigate to your media plan and select Published View.



1. Click on the Placements tab.



1. Use the filter and search bar to find the placement that you want to map a TrueView ad to.



1. Click on the name of the placement to edit it.



1. In the External Platform Mappings section at the bottom of the page, click on Add external platform mapping.



1. In the pop-up window that opens, complete all fields:



Platform: Please select Google Ads.
Entity type: This will be automatically set to Ad.
Google Ads Account: Select the Google Ads account that has been onboarded for your Campaign Management client. Please follow these onboarding instructions if you cannot find your account.
Entity ID: Enter your ad’s ad group ID and ad ID separated by a pipe (|) in the format Ad group ID|Ad ID. You can add multiple TrueView ads to a Campaign Management placement by entering a comma-separated list.

7. Click on Add.

Once mapped, data will be downloaded daily and will be available in Campaign Management as well as in Datalab for reporting and analysis. Check out this knowledge base article for guidance on how to troubleshoot data integrity issues.

Creating Campaign Management Placements
Lesson 3 of 7
Campaign Management placements are specific ad units within a property, and they house the most granular meta data around formats and targeting such as which audiences we’re going to buy against and what media types we are using to buy those audiences.

There are a few things you need to know about Campaign Management placements. Once we've got these covered, we'll jump right in and create a few examples.

Campaign Management placement tags
Campaign Management placements can have multiple placement tags  - those are used for trafficking placements in the ad server which you'll learn more about in the next lesson.

The size of Campaign Management placements refer to reporting dimensions. These may differ to the dimensions of placements in CM360. For that reason, Campaign Management placements can have multiple Campaign Management  placement tags that will be trafficked as placements in CM360.

Some typical examples to best explain this logic include:

Homepage takeover: For a HPTO, you may create only one Campaign Management placement with creative size "No fixed size" that has multiple Campaign Management placement tags (e.g. 300x600, 1x1, 300x250). Those individual placement tags will be trafficked as placements in CM360.

Site-served video ad: You may create only one Campaign Management placement but with multiple Campaign Managementplacement tags for trafficking as placements in CM360 that fire on impression and completed view.

Don't worry, it'll all make more sense shortly as we create placements for those examples!

Placement builder
Campaign Management allows you to create placements in bulk. This is achieved via the placement builder. The placement builder enables you to create literally thousands of placements at once - within only a few minutes, and following your client’s or Nexus naming convention.

The two fields that are standard across all custom naming conventions and Campaign Management placement builders for all clients are:

Trafficking config: This field helps Campaign Management know the type of placements you will need trafficked in the ad server, if any. Options include:

Fully ad-served placement: The publisher accepts third party display or video tags that will serve creatives.

Site-served: The publisher will serve the creative themselves (e.g. text ads) but can accept third party click trackers and impression pixels.

Non ad-served: No creative or landing page will be third-party ad-served (no ad tags required). This option can also be used for dummy placements to manually upload stats for reporting. Basically, you will only create an Campaign Management placement without Campaign Management placement tags (like a shell), and you won't create any placements in CM360.

Creative size: Select the most appropriate sizes that describe the visual dimensions of the ad as a whole.

Custom naming conventions
To enforce a globally consistent taxonomy and enable cross-channel reporting, Campaign Management supports custom naming conventions, allowing each client to have its own placement builder that can even be custom per platform.

As part of the onboarding process of a new client to Campaign Management, we’re establishing together with the Choreograph team what this naming convention is and configure the custom placement builder for your client.

No placements for SA360
For SA360 campaigns, you won't need to create Campaign Management placements. That's because there's no link between SA360 and CM360 either - i.e. you won't need to traffic SA360 campaigns in the ad server.

As a result, there's a dedicated process of mapping Campaign Management to SA360 that differs from all other activation platforms. You'll learn about it later in this course.

Trafficking \& Mapping to CM360

Lesson 4 of 7

GOOD NEWS: Trafficking placements in CM360 and mapping Campaign Management to CM360 is like two for one - one streamlined process that completes both tasks. Hooray!

Well done. Let's get into it



Once you have created Campaign Management placements for all relevant plan lines in your media plan, the next step will be for you to prepare a trafficking sheet (aka T-sheet) for your media plan and send that to your local AdOps team who will be creating placements, ads and creatives in CM360. 



The T-sheet provides AdOps all the info they need to create and traffic CM360 placements which will then be automatically linked (aka "mapped") to Campaign Management  placement tags. This is essential for reporting on your campaign performance across multiple channels.

Mapping to SA360

Lesson 5 of 7

Campaign Management has an integration with Google SA360 and receives daily data on the performance of your search campaigns. In order to assign this data to the correct Campaign Management media plan and enable reporting, you need to map Campaign Management entities to entities of SA360. 



Unlike most other integrated activation platforms, mapping SA360 to Campaign Management is a more manual process that consists of two (2) key steps: 







Before we go ahead and map SA360 to Campaign Management, there are a couple of things you need to do first.

Any new SA360 accounts need to be onboarded to Campaign Management first to ensure we’re able to collect its data on a daily basis. This is typically done as part of the client onboarding to Campaign Management, however if your SA360 account hasn't yet been onboarded, please reach out to the Choreograph team to assist you. 



Mapping SA360 entities to Campaign Management is directly done in the Campaign Management UI. But in order for there to be anything to map, you will first need to go into the SA360 platform and set up your SA360 account, campaigns and keywords. Wait a day until data from SA360 has been pulled into Campaign Management, and then mapping in Campaign Management will be possible.

