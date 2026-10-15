Introduction to Media Optimizations
Course Summary:
The course introduces Media Optimizations, an AI-powered optimization platform within WPP Open. It explains how Media Optimizations enhances campaign performance by automating media optimization tasks, analyzing campaign data across connected buying platforms, and providing actionable insights to support better decision‑making.

Learning Objectives:
Upon completion of this course, you will be able to:

Define Media Optimizations and explain its purpose in improving media campaign performance.
Explain how Media Optimizations fits within the DPAM workflow.
Describe how Media Optimizations works, including its AI‑driven optimization process, optimization levers, campaign strategies, and integrations with buying platforms.
Identify the key benefits of using Media Optimizations, including operational efficiency, performance improvements, and data‑driven insights for campaign optimization.

What is Media Optimizations?
Lesson 1 of 7


Getting Started with Media Optimizations!

Media Optimizations is a self-service, AI-powered optimization platform designed to improve your campaign's performance across connected media buying platforms. It functions as an optimization layer on top of the buying platforms you use to manage and deliver digital advertising campaigns.


Always On, Always Optimized!
Media Optimizations continuously analyzes campaign performance and automatically applies optimization adjustments. These include refining bidding strategies, reallocating budgets across campaign components based on performance signals, and optimizing targeting parameters. This process helps improve campaign efficiency and overall performance.

Media Optimizations uses multiple optimization methods to achieve campaign goals. These methods work together continuously to improve performance rather than operating independently.

Media Optimizations operates within the broader media workflow that supports campaign planning, activation, and measurement.

The Media Operations follow the Discover, Plan, Activate, and Measure (DPAM) framework, which structures the lifecycle of media campaigns.

Within this framework, Media Optimizations primarily supports the Activate phase, where campaigns are executed and continuously optimized to deliver better results.



DPAM Structure

Supported Platforms refer https://knowledge-base.wppopen.com/hc/en-us/articles/21866961154972-Supported-Buying-Platforms

Supported Buying Platforms
Export as PDF Export as PDF
Quick summary
Media Optimizations connects with six major buying platforms so you can optimize campaign performance across your digital media spend. This guide shows you which platforms are available, what each one offers, and how they integrate with Media Optimizations.

Platform comparison at a glance
Platform	Campaign-Level Optimization	Cross-Platform Optimization	Intelligent Line Items	Availability
Amazon DSP	Yes	Yes	Closed Beta	Global*
DV360	Yes	Yes	Yes	Global
Microsoft Invest	Yes	Yes	Yes	Global (until Feb 2026)
The Trade Desk	Yes	Yes	Yes	Global
Pulsepoint	Yes	Yes	Varies	US only
Meta	Yes	Yes	No	Global
*In markets where Amazon DSP is available


Global platforms
Amazon DSP
Availability: Global (in markets where Amazon DSP is available)

What you can do:

Campaign-Level Optimization (CLO)
Cross-Platform Optimization (CPO)
Budget optimization across line items
Advanced goal types including ROAS, CPA, CVR, and more
Track performance with 34+ conversion goal metrics
How we connect: Campaign Management API

Supported goal types: CPA, CVR, CPC, VCR, CPCV, vCPCV, CPM, vCPM, CTR, Create Any Goal, ROAS, Engagement Score, Upload External Measurement, Customize Revenue Calculation

Amazon-specific conversion metrics:

Action metrics: addToCart, totalPurchases, totalNewToBrandPurchases, detailPageView, totalUnitsSold, newSubscribeAndSave
Revenue metrics: totalSales, newToBrandProductSales, sales, totalNewToBrandSales
Budget optimization settings enforced:

Level	Setting	Value
Campaign	Automatic Budget Allocation	Disabled
Campaign	Bid Strategy	Spend Budget in Full
Ad Group	Budget Caps	None
Ad Group	Automatic Budget Allocation	Disabled
Ad Group	Delivery Profile	Even
Ad Group	Catch-Up Boost Percentage	0
Current limitations:

Intelligent Line Items (ILIs) are in closed beta
Secondary In-View-Rate (IVR) Goal Optimization is not supported
For connection instructions, see How to connect your Amazon DSP partner to Media Optimizations


DV360 (Google Display & Video 360)
Availability: Global

What you can do:

Campaign-Level Optimization (CLO) with Intelligent Line Items (ILIs)
Cross-Platform Optimization (CPO)
Custom SDF automation for advanced campaign management
YouTube optimization across Video Reach, Video Views, and Video Action line items
How we connect: Structured Data Files (SDF) and DV360 APIs

Supported goal types: CPA, CPC, CPM, vCPM, CPCV, vCPCV, CVR, CTR, VCR, ROAS, Create Any Goal, Engagement Score, Upload External Measurement, Custom revenue calculations

Key requirement: SDF v10 must be enabled at both the Partner and Advertiser levels. SDF v9.2 is also supported but v10 is recommended as the latest version.

For DV360 configuration details, SDF limitations, ILI behavior, and known platform constraints, see DV360 configuration reference and known limitations. For connection instructions, see How to connect your DV360 partner to Media Optimizations.


Microsoft Invest (Xandr)
Availability: Global

Important notice: Microsoft will no longer support media buying through Microsoft Invest DSP starting February 28, 2026. Plan your platform transitions accordingly.

What you can do:

Campaign-Level Optimization (CLO) with Intelligent Line Items (ILIs)
Cross-Platform Optimization (CPO)
Custom Bidlist strategies for advanced targeting
Line item and insertion order level optimization
API and Custom Bidding interface integration
How we connect: Xandr API and Custom Bidding interface (Bonsai language)

Supported goal types: Standard Media Optimizations goal types including cost-based, rate-based, and revenue goals

Key requirements:

API credentials with specific format
User roles: APB Bonsai, APB Genie
Required feeds: APB v8, standard_feed, segment_feed, video_events_feed, enhanced_viewability_feed, custom_model_feed, pixel_feed
Legacy features (still available but no longer updated):

Helios - Line Item Level: Prospecting through intelligent targeting exploration
Custom Tree - Line Item Level: Custom Bonsai models for advanced optimization
For connection instructions, see How to connect Microsoft Invest (Xandr) in Media Optimizations


The Trade Desk (TTD)
Availability: Global

What you can do:

Campaign-Level Optimization (CLO) with Intelligent Line Items (ILIs)
Cross-Platform Optimization (CPO)
Custom Bid List for targeted bid feature optimization
Budget allocation between line items
Intelligent targeting focus for better performance
How we connect: Dimensional Bidding interface and TTD API

Supported goal types: CPA, CPC, CPM, vCPM, CPCV, vCPCV, CVR, CTR, VCR, ROAS, Create Any Goal, Engagement Score, Upload External Measurement, Custom revenue calculations

Key requirement: API credentials with UI login access, plus required data feeds enabled by your TTD representative.

For TTD configuration details, Intelligent Ad Group behavior, and known platform constraints, see TTD configuration reference and known limitations. For connection instructions, see How to Connect Your TTD Partner in Media Optimizations.


Meta
Availability: Global

Meta is a fully supported buying platform in Media Optimizations, enabling AI-powered budget optimization across the entire Meta Business Suite — including Facebook, Instagram, WhatsApp, and Messenger. MO integration is enabled via the self-serve Campaign Connect workflow.

What you can do:

Campaign-Level Optimization (CLO) — single-platform Meta strategies
Cross-Platform Optimization (CPO) — Meta combined with other integrated buying platforms
Budget optimization across campaigns and ad sets based on performance
Optimization across feeds, reels, stories, messages, and search formats
Advantage+ campaign support
How we connect: Self-serve Campaign Connect workflow

Supported goal types: CPA, CPC, CPM, vCPM, CPCV, vCPCV, CPV, Conversion Rate, CTR, Video Completion Rate, In View Rate, ROAS, Engagement Score, Impact, Create Any Goal, Upload External Measurement

Not supported: Intelligent Line Items (ILI), Viewability goals, Bulk campaign creation

For connection instructions, see How to connect Meta to Media Optimizations


US-only platforms
Pulsepoint
Availability: US only

Pulsepoint is a healthcare-focused Demand-Side Platform specialized for healthcare and pharmaceutical advertising.

What you can do:

Campaign-Level Optimization (CLO)
Cross-Platform Optimization (CPO)
Platform connection and optimization support
Integration with Media Optimizations strategies
How we connect: Platform-specific API

Contact Choreograph Support for connection instructions


Important integration details
Data onboarding timing
Media Optimizations onboards data starting 5 days before your connection date. Historical data from before the connection date will not be managed.

Processing time
Allow a minimum of 3 business days for seat integration. Incomplete information may extend processing time.

Business model selection
When connecting any platform, you must specify your business model:

All-Inclusive (Media Solutions): Usage included in existing service agreement
Disclosed: Agency charges a service fee; requires fee amount specification
Connecting multiple platforms
You can connect multiple buying platforms to Media Optimizations and run optimization strategies across them using Cross-Platform Optimization.

Platform-specific requirements
Each platform has unique configuration requirements and optimization settings. We recommend reviewing the platform-specific guide before connecting.

How does Media Optimizations fit into the DPAM Workflow?
Lesson 2 of 7


Media Optimizations operates from the Activate phase of the DPAM framework. 
It acts as the AI optimization layer between your campaign strategy and its execution.

Activate Pillar

Navigate the steps to explore how Media Optimizations supports campaign execution and optimization during campaign activation.


Campaign Setup ( in Buying Platforms)

Activation teams configure the campaign in the Buying Platform, followed by the setup of a media optimization strategy.


Media Optimizations Optimization Layer

Activation teams create a Media Optimization strategy in the Media Optimizations product to connect it to the previously created campaign.

Campaign Performance Monitoring and Optimization

The Media Optimizations platform continuously monitors delivery, pacing, and campaign performance across connected campaigns. AI-powered optimizations are applied to improve campaign performance.

Utilizing Insights Package

Performance insights are generated after the strategy has been live for three days, and you can utilize them to inspect current performance and as a feedback loop to improve current and future campaign strategies.

Important! Media Optimizations operates within the campaign boundaries set during the original setup, ensuring that campaigns are continuously optimized during the Activate phase while generating insights to inform future planning.

How does Media Optimizations work?
Lesson 3 of 7

Media Optimizations Workflow

Media Optimizations connects to your buying platforms and applies AI‑driven strategies to continuously improve campaign performance.

Follow this workflow that shows how Media Optimizations analyses campaign data and applies AI-driven adjustments to improve campaign performance.

Connect Buying Platforms
Media Optimizations connects to supported buying platforms where campaigns are already running. This allows the platform to access campaign performance data

Create Optimization Strategy
Campaign managers create an optimization strategy and attach campaigns or insertion orders to that strategy.

The strategy defines:

Optimization goals

Budget management approach

Campaign scope

AI Performance Analysis
The AI continuously analyses campaign data such as:

Bidding performance

Audience engagement

Delivery pacing

Platform‑level signals

This helps identify opportunities to improve campaign outcomes. The system evaluates these signals together to determine the most effective optimization actions across multiple levers.

Automated Optimization Adjustments
Based on performance analysis, Media Optimizations automatically makes adjustments, such as:

Reallocating budgets across campaign components based on performance signals

Adjusting bidding strategies

Refining audience targeting

Optimizing inventory for viewability

These adjustments are executed through system-managed components such as Intelligent Line Items (ILIs), which dynamically refine delivery within the defined campaign scope.

Note: These adjustments happen continuously throughout the campaign lifecycle.
Performance Monitoring and Insights


You can monitor performance using the Media Optimizations dashboard, which provides:

Performance monitoring

Optimization tracking

Visual insights into campaign performance

These insights help you understand what is driving results and how to improve future campaigns.

Click the image to expand.

While the workflow explains the overall process, Media Optimizations uses specific strategies and mechanisms to continuously optimize campaign performance.

Optimization Strategies in Media Optimizations

Media Optimizations supports two main optimization approaches.

Campaign-Level Optimization (CLO)

This approach optimizes a single campaign within one buying platform. Budget management remains within the buying platform. It is useful when you are focusing on improving performance for an individual campaign.

Cross-Platform Optimization (CPO)

This approach optimizes multiple campaigns across different buying platforms simultaneously. You manage budget allocation directly within Media Optimizations. It allows you to shift budget toward the best-performing opportunities across all connected platforms.


To support these strategies, Media Optimizations applies multiple optimization methods that work together to improve campaign performance.

Optimization Levers in Media Optimizations

Media Optimizations does not rely on a single optimization method. 
The system dynamically coordinates multiple optimization levers across the campaign to achieve the primary KPI.

One of the key mechanisms that enables these optimization actions is Intelligent Line Items (ILIs).

Intelligent Line Items (ILIs)

Intelligent Line Items (ILIs) are AI-managed components. They enable the Media Optimizations AI to apply optimizations adjustments dynamically.

For every Original Line Item (OLI) created in the buying platform, Media Optimizations generates a corresponding Intelligent Line Item (ILI). This creates a 1:1 relationship.


Original Line Items

Original Line Items (OLIs) define setup such as targeting, bidding, and other parameters.

Intelligent Line Items

Intelligent Line Items (ILIs) are a subset of the Original Line Item, focusing on high-performing feature combinations.

Intelligent Line Items can be identified in buying platforms using the _CP_INT suffix.

IMPORTANT!

Intelligent Line Items are directly controlled by the AI Optimization engine.

Manually editing an Intelligent Line Item can break its connection with the AI engine, cause synchronization issues, and impact campaign performance.

REMEMBER! 
All updates must be made to the Original Line Item (OLI).
The AI will automatically apply updates to the corresponding Intelligent Line Item.

Key Features of Media Optimizations

Advanced Homepage
A centralized interface that lets you monitor and manage optimization strategies across connected platforms. It provides real-time visibility into campaign pacing, performance, and optimization actions.

AI-Driven Optimization
Media Optimizations automatically adjusts campaign parameters such as:

Bidding strategies

Targeting parameters

Budget allocation

Delivery pacing

These adjustments improve campaign performance without requiring manual intervention.

Insights Package
The Insights Package converts campaign data into clear visual insights and reports.

These insights help you:

Understand campaign performance drivers

Identify optimization opportunities

Share results with clients and stakeholders

Reports can also be exported as PowerPoint presentations for client reporting.


What are the benefits of using Media Optimizations?
Lesson 4 of 7

Using Media Optimizations provides several advantages for you and your clients.


1. Improved Campaign Performance
The AI continuously analyzes campaign data and optimizes delivery to improve performance metrics such as:

Click‑through rate

Conversion rate

Cost efficiency

Video completion rate

View the complete list of standard goal types(https://knowledge-base.wppopen.com/hc/en-us/articles/24097445584028-Supported-Standard-Goal-Types#section-1).

Supported Standard Goal Types
Export as PDF Export as PDF
Quick summary
Media Optimizations supports a range of standard goal types that work with data readily available in your buying platforms. Standard goals cover clicks, conversions, video views, impressions, viewability, and return on ad spend. This guide explains each goal type, its formula, when to use it, and how to select the right goal for your campaign objectives.

 

What are goal types?
Goal types define what Media Optimizations optimizes for in your campaigns. When you select a goal, you're telling the AI what success looks like so it can make decisions to achieve that outcome.

In simple terms, your goal is the target metric the platform works to improve. Everything the AI does, from budget allocation to bid adjustments to targeting refinements, aims to optimize performance against your chosen goal.

Standard goals work out of the box using data readily available from your DSP. Choose standard goals for fast activation and most campaign types.

 

Click goals
Optimize for click volume and click efficiency.

Goal	Optimizes For	Formula	When to Use
CPC	Lower cost per click	revenue / clicks	Drive clicks efficiently
CTR	Higher click-through rate	clicks / impressions	Maximize engagement
 

Conversion goals
Optimize for conversion volume and conversion efficiency.

Goal	Optimizes For	Formula	When to Use
CPA	Lower cost per conversion	revenue / conversions	Performance campaigns
Net CPA	Lower media cost per conversion	spend / conversions	Media cost efficiency
CVR	Higher conversion rate	conversions / impressions	Maximize conversion efficiency
CPA (Goal Pixel)*	Lower cost per goal pixel conversion	revenue / goal pixel conversions	Specific pixel optimization
Net CPA (Goal Pixel)*	Lower media cost per goal pixel conversion	spend / goal pixel conversions	Specific pixel efficiency
CVR (Goal Pixel)*	Higher goal pixel conversion rate	goal pixel conversions / impressions	Specific pixel rate
*Xandr (Microsoft Invest) only

 

Video goals
Optimize for video completion and video view efficiency.

Goal	Optimizes For	Formula	When to Use
CPCV	Lower cost per completed view	revenue / video completions	Video completion focus
VCR	Higher video completion rate	video completions / video starts	Maximize completion percentage
vCPCV	Lower cost per viewable completed view	revenue / viewable video completions	Viewability + completion
Net vCPCV	Lower media cost per viewable completed view	spend / viewable video completions	Viewable completion efficiency
CPV YouTube	Lower cost per YouTube view	spend / YouTube views	YouTube campaigns
VCR YouTube	Higher YouTube view rate	YouTube views / impressions	Maximize YouTube views
 

Impression goals
Optimize for reach and impression volume.

Goal	Optimizes For	Formula	When to Use
CPM	Lower cost per 1,000 impressions	(revenue / impressions) — 1000	Reach campaigns
Net CPM (Margin CPM)	Lower media cost per 1,000 impressions	(spend / impressions) — 1000	Reach cost efficiency
 

Viewability goals
Optimize for viewable impressions and viewability rates.

Goal	Optimizes For	Formula	When to Use
vCPM	Lower cost per 1,000 viewable impressions	(revenue / viewable impressions) — 1000	Viewability focus
Net vCPM	Lower media cost per 1,000 viewable impressions	(spend / viewable impressions) — 1000	Viewable cost efficiency
IVR	Higher viewable impression rate	viewable impressions / impressions	Maximize viewability percentage
IVR (Measured)	Higher viewable impression rate (measured only)	viewable impressions / measured impressions	Viewability of measured impressions
View Measured Rate	Higher measurable impression rate	measured impressions / impressions	Maximize measurability
 

Revenue goals
Optimize for return on ad spend.

Goal	Optimizes For	Formula	When to Use
ROAS	Higher revenue return per ad spend	conversion revenue / revenue	E-commerce, revenue-focused campaigns
 

Understanding cost goals vs rate goals
Cost goals
Cost goals (CPA, CPC, CPCV, CPM, vCPM) optimize to lower the average cost.

Best for efficiency and budget control
Example: CPA optimizes to get more conversions at a lower cost per conversion
Rate goals
Rate goals (CVR, CTR, VCR, IVR) optimize to increase the percentage or rate.

Best for performance and engagement maximization
Example: CVR optimizes to get a higher percentage of impressions converting
ROAS
ROAS is unique, it optimizes to maximize revenue return relative to spend.

Best for revenue-focused campaigns
 

Understanding gross vs net goals
Many goals come in two versions based on how cost is calculated:

Standard version (gross)
Uses "revenue" (advertiser cost—what the client pays)
Examples: CPC, CPA, CPCV, CPM
Net/Margin version
Uses "spend" (media cost—what's paid to publishers)
Prefixed with "Net" or "Margin"
Examples: Net CPC, Net CPA, Margin CPCV, Net CPM
Note: Revenue is pulled from your buying platforms.

 

Revenue types (pacing to events)
Revenue types let you pace campaigns to specific success events rather than budget amounts. This changes what counts as your "unit of delivery" for pacing.

Available for:

CPC: Pace to a target number of clicks
CPCV: Pace to a target number of completed views
CPM: Pace to a target number of impressions
Important: This feature requires a monetary budget set in your buying platform and is configured during strategy creation.

 

How to choose the right goal
Step 1: Identify your campaign objective
Objective	Recommended Goals
Awareness	CPM, vCPM, IVR
Engagement	CTR, VCR, CPCV
Performance	CPA, CVR, ROAS
Efficiency	CPC, Net CPA, Margin CPM
Step 2: Consider your data availability
DSP data available: Use standard goals
External measurement needed: Use Upload External Measurement (advanced goal)
Custom weighting needed: Use Engagement Score or Create Any Goal (advanced goals)
Step 3: Align with client KPIs
Choose a goal that matches what your client measures success by. This ensures your Media Optimizations performance directly supports client reporting.

 

Setting your goal target
Your goal target is the desired performance level from your media plan.

How Media Optimizations uses it:
Media Optimizations always optimizes for the best possible result, regardless of your target. Your goal target creates accurate visualizations in the Insights package.

What to enter:
Enter the desired performance target from your media plan for the most accurate reporting.

Examples:

For CPA goal: Enter your target cost per acquisition (e.g., $25.00)
For ROAS goal: Enter your target return on ad spend (e.g., 4.0)
For CTR goal: Enter your target click-through rate (e.g., 0.5%)
 

Advanced goals
When standard goals don't match your objectives, Media Optimizations offers advanced goals for complex optimization needs:

Create Any Goal: Custom weighted outcomes
Upload External Measurement: Third-party success events
Cost Per Impact: Cross-channel quality optimization
Engagement Score: Multi-touchpoint campaigns with funnel weighting
Cost Per Impression Value: DV360 Custom Bidding optimization
NCS New Buyer Goal: Retail customer acquisition
Advanced goals require additional data input or consultation with Marketing/Data Science teams. Learn more in the Advanced Goal Types guide. 


2. Advanced Cross-Platform Activation
Consolidate campaign activation from one central place to execute daily optimizations across any channel, buying platform, or inventory source.

Leverage unique audiences and inventory

Streamline your investment decisions

Gain insights into cross- platform optimizations


3. Operational Efficiency
Many routine campaign optimization tasks are automated, including:

Budget allocation

Bid adjustments

Targeting refinement

This automation reduces manual effort, saving your valuable time.


4. Smarter Budget Allocation
Media Optimizations identifies high‑performing campaign elements and automatically shifts budgets toward them. This ensures your advertising spend is used more efficiently.


5. Continuous Optimization
Media Optimizations operates continuously. The AI evaluates campaign performance, applying improvements automatically.


6. Centralized Campaign Management
You can monitor and optimize multiple campaigns across platforms from a single dashboard. This provides better visibility and control over your campaign’s performance.


7. Data Driven Insights
The platform provides detailed reporting that helps you:

Understand performance drivers

Identify optimization opportunities

Improve future campaign strategies

