# DSP-Project-Django

# Project specification

## Goal 
Build a toy DSP (tDSP) based on the specification below and compete with other DSPs for impressions in Real-Time Bidding auctions. 

## Glossary
* **Real-Time Bidding (RTB)** - It is a technology used in programmatic advertising that allows for the buying and selling of digital ad inventory in real-time. It is an automated auction process that takes place in milliseconds, allowing advertisers to bid on ad impressions as they become av ailable.

* **Demand-Side Platform (DSP)** - It is a software platform used in programmatic advertising that allows advertisers and agencies to purchase digital ad inventory from multiple ad exchanges and ad networks through a single interface. DSPs automate the process of bidding on ad inventory in real-time, using data and algorithms to optimize the buying process.

* **Supply-Side Platform (SSP)** - It is a software platform used in programmatic advertising that allows publishers and media companies to sell their digital ad inventory to multiple ad exchanges and ad networks through a single interface. SSPs automate the process of managing and selling ad inventory, optimizing the process for maximum revenue generation.

* **Advertiser** - A company paying for an advertisement. Example, Coca-Cola, Toyota, Zappos, Sony, eCommerce sites and online stores, mobile apps etc.

* **Publisher** - A website owner, mass media or mobile apps developer, who want to sell their advertising inventory and earn money. Example, Facebook, New York Times etc.

* **Creative** - An advertising item. It can be an image, video, flash animation and the like.

* **Impression (Imp)** - A single display of online content to a user’s web-enabled device. Many websites sell advertising space by the number of impressions displayed to users. An online advertisement impression is a single appearance of an advertisement on a web page. Each time an advertisement loads onto a user's screen, the ad server may count that loading as one impression.

* **Click** - A process, when the user clicks on the creative and system redirects a user to the advertiser’s site.

* **Conversion** -  A technical term identifying the point, when a user performs any action, that advertiser sets as a campaign goal, for example - clicking on the “Buy” button, leaving feedback, landing on the particular page and the like. Conversions  are often tracked by a  tracking pixel , called a conversion pixel.

* **Advertising campaign (Campaign)** -  In digital advertising, a  campaign  will refer to a set of units relates to a particular product. In this project Campaign has only linked creatives which are related to the particular product.

* **Frequency capping** - It is a technique used in digital advertising to limit the number of times a particular ad is displayed to a user within a given time period. The purpose of frequency capping is to avoid overexposure of an ad to a user, which can lead to ad fatigue, reduced effectiveness, and potential annoyance.

* **Ads.txt** - It is an initiative aimed at improving transparency and reducing fraud in programmatic advertising. It is a simple, flexible, and secure method that publishers can use to publicly declare the companies (SSP) authorized to sell their digital ad inventory. A publisher creates an ads.txt file that lists the companies authorized to sell their digital ad inventory and hosts it on their site.

* **Bid floor** - Usually it is the minimum price that a publisher sets for the ad inventory they are selling in a programmatic advertising auction. In the project it is mostly related to ad campaign to make some restrictions on DSP side to raise probability of impression win.

* **IAB Category** - A segment of interests (e.g. cars, movies, books, computers, etc.) by which ad networks and SSPs target a user. In the project will be used IAB categories v1 [link](https://iabtechlab.com/wp-content/uploads/2021/10/Content-Taxonomy-1.0.xlsx)

* **Auction**:
	* **1st Price Auction** - First price auction is a type of auction used in programmatic advertising where the highest bidder pays the exact amount they bid to win the auction
	* **2nd Price Auction** - A second price auction is a type of auction used in programmatic advertising where the highest bidder wins the auction, but pays only slightly more than the second-highest bid. In a second price auction, the winning bidder pays the price of the second-highest bid plus a small increment, rather than the exact amount they bid.

* **AdOps** - AdOps, short for Advertising Operations, is a team responsible for the technical aspects of digital advertising campaigns, including the planning, setup, optimization, and reporting of ad campaigns.

* **AdRequest(+AdResponse)** - An ad request is a signal sent from a website or app to an ad server to request an ad to be served on the page or app screen. When a user visits a website or opens an app, the site or app sends an ad request to an ad server, indicating that an ad slot is available to be filled. The ad server then evaluates the request based on various criteria, such as the targeting parameters and available inventory, and responds with an ad to be displayed to the user.

* **BidRequest(+BidResponse)** - A bid request is a signal sent from an SSP to a DSP to request a bid value for an Advertisement impression.

* **NoBid** - In programmatic advertising, a nobid (or no-bid) occurs when a demand-side platform (DSP) or advertiser decides not to bid on an ad impression after receiving a bid request from an ad exchange or publisher.

* **CPC or Cost per Click** - The cost of advertising based on the number of clicks received, i.e. `spent budget` divided by `click count`.


## Game

### Preparations
The game starts with the initialization of tSSP, tDSPs, additional services (creative serving server for each tDSP, single `ads.txt` server):
* Set up `ads.txt` server, get its IP address.
* Set up creative serving services, tDSPs (creative service address and `<ads.txt.server_ip>` should be passed to its configuration).
* Set up tSSP:
	* Pass `<ads.txt.server_ip>` to establish control during the game
	* Add tDSPs IP addresses to enable RTB process

### Game initialization
tSSP unites two UIs in itself:
* Game management UI (reset a game, set up impression parameters).
* Publisher UI for advertisement impressions.

In the tSSP UI new game is created, the following parameters should be set up:

* **`game goal`** - `total sum` or `CPC`. It defines the parameters which should be optimized by tDSP during the game.

* **`number of impressions`** - it is a number of game rounds(from business point it means that all budget should be spent during this period with maximum yield), each impression contains:
	* `click base probability`.
	* `impression base probability`.

* **`total budget`** - every DSP will have this budget (across all campaigns inside, i.e. if each campaign has its own budget then their sum should be equal to **total budget**).

* **`game type`**:  `script` or  `free`.

* **`auction type`**:  `1st price` or `2nd price`

* **`impression/click/conversion`** base revenue amount. It means how much money successful event brings without any fines.
	* Fines are defined in the tSSP spec.

* **`frequency capping`** number (bonus feature) - it describes how many impressions is allowed to win for the same campaign for the same user (`user_id` is passed in `BidRequest`) without `frequency capping` fine. 

### Game types
There are 2 game types as it was mentioned above:

* **`script`** - all creatives and campaign are created by script (via API) provided by IPONWEB side. During the game you are only allowed to manage budget spending parameters (i.e. restrict bid values) and to enable/disable campaigns. You can't manage creatives, their parameters and budget distribution across campaigns.

* **`free`** - you can create/delete/update campaigns, creatives and distribute a budget on your own.

### RTB process (game round/one impression)

![Overall RTB process](attachments/rtb_game_total.png)

![[RTB Game - Page 3 (3).png]]

Given 3 `DSPs`, one `tSSP`, and one `publisher site`. The budget for each DSP is `50`. 
1. A random user comes to the publisher site and their browser initiates `Ad Request` to the `tSSP`.
2. The `tSSP` receives the `Ad Request` and calculates all parameters for a `Bid Request`.
3. The `tSSP` sends `Bid Requests` to all DSPs.
4. DSPs receive the `Bid Requests`, extract information from the body, calculate bid value and choose appropriate creative (image).
4. DSPs send bid amount and creative link in responses:
	1. `DSP Alpha` -> *Dog food* banner link with bid value `4`.
	2. `DSP Beta` -> *Cat food* banner link with bid value `9`.
	3. `DSP Gamma` -> *Parrot food* banner link with bid value `10`.
5. The tSSP receives all responses and chooses the one with the highest bid value (impression winner).
	1. It is the bid response from `DSP Gamma`.
6. Since it is a toy tSSP it calculates:
	* The final probability of a click (different fines could be applied). Based on the probability the tSSP calculates if the event has happened.
	* If the click is happened then it calculates the final probability of the conversion and calculates whether the event happened. 
	* Then the tSSP sends to `DSP Alpha` and `DSP Beta` `loss notifications` and sends `win notification` with `click` and `no conversion` to `DSP Gamma`. The budget of the `DSP Gamma` will become:
		* `50 - 10 => 40` in the 1st price auction 
		* `50 - 9 = > 41`  in the 2nd price type auction (it is important to emphasize that tSSP takes zero fees).  
7. After that the tSSP returns a creative link from a Bid Response of `DSP Gamma` to the UI
8. `Parrot food` advertisement is shown for the user on the publisher's site.

## How winner is determined
The are two options for the goal score:

**Total revenue**
At the end of the game the score for each DSP is calculated by summing up all revenues from impressions, clicks, conversions (and it DOES NOT include the rest of the budget.)

**Minimal CPC**
The winner is chosen by minimal CPC, i.e.:
* `spent budget` / `number of clicks`

---
## How does toy SSP work
Actually tSSP aggregates on its side the following components:
* Game control panel
* SSP part 
* Publisher Site
* `ads.txt` service

### BidRequest/BidResponse stage
When tSSP receives AdRequest from the Publisher UI it starts BidResponse body building:
* Generates `id` for `Bid Request`.
* Fills  `imp` section  `banner` parameters with the following distributions for the size option (`creative size` feature):
	* `80%` predefined values: `200x200`, `300x200`, `200x300.`
	* `10%` scaled predefines values: for instance `400x400`, ....
	* `10%` random values.
* Sets `site.domain`, `click.prob`, `conv.prob` from game impression configuration.
* Sets `user.id` with `20%` probability that previously used values may repeat (related to the  `frequency capping` feature).
* Random set of `blocked categories`: `IAB-1`, ..., `IAB-25` (`blocked creatives` feature).

Then it sends `Bid Requests` to tDSPs and waits for HTTP responses for `5` seconds. In case of timeout - it is considered as `NoBid` response.

### Auction, click and conversion
When all responses are collected:
* tSSP checks bids and available budgets of DSP: if the bid exceeds the rest of the budget then the bid is ignored (same as `NoBid` situation).
* If a bid has a forbidden creative category -> the bid is ignored (same as `NoBid` situation).

The bid with the highest value is considered to be a winner. A creative from such `Bid Request` will be shown on the UI of a Publisher
* If multiple `Bid Requests` have such bid value then a random `Bid Request` will be chosen.
* If the creative has a wrong size -> click probability could be increased/decreased by 0.05 and the conversion probability is decreased by 0.03.
* If the campaign of the creatives exceeds recommended frequency capping -> click probability is de creased by 0.05.
* If tSSP is not authorized to be a reseller or direct seller for the publisher site (`ads.txt` feature) -> impression revenue is reduced to zero.

### Win/Loss notification
Every tDSP which didn't send `nobid` and is not a winner will receive `loss notification` with BidRequest ID.
The winner will receive `win notification`:
* Bid request ID.
* Charged bid amount.
* Has click or not.
* Has conversion or not.
* Impression revenue.
* Click revenue.
* Conversion revenue.
---

## tDSP MVP
![DSP scheme](attachments/rtb_game_small_dsp.png)
The tDSP should meet the following minimal requirements: 
- tDSP endpoints (all handlers are required to meet the the specificaton):
	- Game initialization handler (Management part).
	- Bid request handler (RTB part).
	- Notification handler (RTB part).
	- Advertising campaign handler (Management part).
	- Creative handler (Management part).
- Must have own separate part for creative serving, one of the following options:
	- Integrated into the main application.
	- Separated service.
- Should have UI for campaigns/creatives creation/deletion.
- Must respect `budget` restrictions - you can't make bids with amount higher than your budget.

## tDSP RTB part (endpoints)

**Game configuration**
`/game/configure/` - should:
* Override previous game configuration.
* Delete all previous campaigns and creatives:
	* It should be done at least in case of `"game_mode": "script"`.

**Bid request endpoint**
`/rtb/bid/` - should receive bid request and return `BidResponse`

**Notify endpoint**
`/rtb/notify/` - should be able to receive and parse notification data (win/loss) and make corresponding changes in the current budget.


## tDSP Management part
The following UI endpoints are required for `script` mode game:
* `/api/campaigns/` (HTTP POST method must be supported for creation).
* `/api/creatives/` (HTTP POST method must be supported for creation).

### Entities
##### Creative
* `external_id` - must be a unique field.
* `categories` - should be consistent with IAB categories from the file in Appendix.
* Each creative is allowed to be linked to only one campaign
###### Campaign
* `budget` - should be consistent with the overall game budget (i.e. sum of all campaign budgets should be less or equal to `total_budget`)

To play `free` game mode you should implement the following UI parts:
* Login (actually it is not required but could be very useful if you don't want other teams can manage your UI too :) )
* Create/Delete/Update campaigns
* Create/Delete/Update creatives (with image upload)
* Link/Unlink creatives to/from campaigns

Some example mockups for these pages:

**Login**

![1](attachments/20230227214916.png)

**Campaigns**

![1](attachments/20230228004158.png)
![2](attachments/20230228005521.png)

**Creatives**

![1](attachments/20230228004120.png)
![2](attachments/20230228005444.png)

## Configurable features from UI side (optional)
You can add any kind of functionality to control, tune and limit your budget spending during the game. It is not required and not needed at all but is very-very useful when something happens with youqr algorithm and you cannot do anything except straight restriction. Examples of such features:

##### * Bid floor
You can add `bid_floor` input field to the campaign form to configure which bid value is minimal for that campaign.
This thing could be useful during both `script` and `free` modes. 

##### * Campaigns activation
You can add checkboxes for campaigns to enable/disable them during the game.
This feature could be useful mostly for `script` mode.

## Creative service
The part of tDSP (separate service) which serves creatives (images) uploaded/managed from the tDSP UI.

The creative `url` (received by the tSSP in `BidResponse` ) is passed to the publisher site without any change. So you can build it in any way you want (any kind of additional query parameters). 

---
## Additional business features
As a bonus, you may implement the following features which help you to get better click and conversion probabilities.

### Respect blocked categories (for `script` mode)
Each creative is created with its own IAB creative category (as 'Automobile' or 'Heath&Care').
A list of forbidden IAB categories comes in each `BidRequest`. If you send `BidResponse` with creative whose category is forbidden then the impression will be lost for you.

### Respect creative size (`free` and `script` modes)
All creatives uploaded to your platform have fixed size but it is not possible to predict which size of `AdSlots` is going to be in `BidRequest`. To support random sizes you can resize images and fill the empty background with some color. 

### ads.txt sync (`free` and `script` mode`)
`ads.txt` is a file that is located in the root path of the publisher site, for instance:
* `https://armeniasputnik.am/ads.txt`
* `https://www.nytimes.com/ads.txt`

This file announces which tSSPs are authorized to sell traffic from this publisher site to DSPs.

The content looks like this (for `armeniasputnik.am`):
```
google.com, pub-8309773808661346, RESELLER, f08c47fec0942fa0
aol.com, 53392, RESELLER
appnexus.com, 3364, RESELLER
freewheel.tv, 799841, RESELLER
...
```

But the real world is not so simple. SSP which are not listed in this file may send `BidRequests` too. It could be fraud or some SSPs are forgotten to be added to this file.

**If SSP does not have any connection with Publisher domain then `impression_revenue` is reduced to zero**

To make correct calculations you should check `ads.txt` for that publisher and check if the SSP id is there.

`ads.txt` will be served at a separate server.

The content of the file will have the following format:
```
%SSP_NAME%, %SSP_ID%, DIRECT
...
```

You can extract the correct %SSP_ID% and %publisher domain% from the `Bid Request` body and get `ads.txt` with the following link: `%server%/ads.txt?publisher=%publisher_domain%`. The response will have the format presented above.

Approximate scheme of such interaction is the following:

![ads.txt](attachments/ads.txt.png)

### Frequency capping
Sometimes it is very annoying for a user that you show him the same advertisement very often. You should store in your DB how many times each advertisment (to be exact - campaign id) is shown for each user and make correct decisions. User id comes as a field in every `BidRequest`. 

**NOTE:** frequency capping works per campaign (i.e. freq. cap = 4, creative_1 from campaign_1 has 4 impressions, creative_2 from the same campaign have 0 impression, next impressions for creative_1 and creative_2 will be fined because they exceed freq.cap. for the campaign).

----
## Additional tech features
Since the project is not only about the business part but also about the technical one the following improvements could be done:

### Separate Role or separate UI for AdOps 
AdOps workers in this case are not admins and should be able to change a restricted set of parameters:
* activate/deactivate campaigns
* change bid_floors and other parameters which affect budget spending

They are not allowed to create/delete creatives/campaigns.

There are some possible ways to make it:
* Create separate role for django admin.
* Create separate UI pages.

### Tracking events/statistics
Make some functionality/UI page/separate logs to track all historical changes:
* information about BidRequests/Wins/Losses
* extra information about bid decisions
* etc (for instance user (AdOps) actions)

Such information is needed to debug the moment when something went wrong.

### Docker
Wrap work environment with `docker` and `docker compose` exposing two services - `DSP` and `Creative serving service`.
Would be nice if you configure it through NGINX and "any uwsgi proxy server".

### Tests coverage
Cover all your endpoints with tests.

### Configure Github CI
Configure CI pipelines for automated testing and checking against linting rules.

---

# API Specification
API format below describes all endpoints which could be used by tSSP that's why it is needed to be extra cautious when you implement them (otherwise tSSP couldn't interact with your tDSP and you will lose) 


## DSP API (RTB part)
### Bid request
##### `> POST /rtb/bid/`

##### `Body:`
``` json
{ 
  // Bid request id, <string>, mandatory
  "id": "some_id",
  // impression slot information with size, mandatory
  "imp": {
    "banner": {
      "w": 300,
      "h": 250
    },
  },
  "click": {
  // click probability, <float>, mandatory
	  "prob": 0.1
  },
  "conv": {
  // conversion probability, <float>, mandatory
    "prob": 0.89
  },
  "site": {
	// publisher domain, <string/URL>, mandatory
    "domain": "www.example.com",
  },
  "ssp": {
  	  // SSP ID, used for ads.txt, <string>, mandatory
	  "id": "0938831" 
  },
  // used in frequency capping, <string>, mandatory
  "user": { 
    "id": "u_cq_001_87311"
  },
  // blocked categories, optional
  "bcat": [
    "IAB2-1",
    "IAB2-2"
  ],
}
```

##### Response

| http code     | content-type                      | response                                                           |
|---------------|-----------------------------------|---------------------------------------------------------------------|
| `200`         | `application/json`        | `Body description is located below`         
| `204` | `text/plain;charset=UTF-8` | `No bid`

##### `Body:`
```json

{
  // All fields below are mandatory
  // creative external id, <string>
  "external_id": "food_001_image",
  // bid amount, <float>
  "price": 2.5,
  // creative url, <string/URL>
  "image_url": "https://www.creatives.com/food/1?width=300&height=250",
  // creative category, list of strings, could be empty
  "cat": [
    "IAB2-1"
  ],
}
```

**IMPORTANT**: "price" should have no more than 2 decimal places otherwise Bid Response is considered as No Bid.


### Notification URL
##### `> POST /rtb/notify/` 

##### `Body:`
```json
{
// Bid Request ID, <string>, mandatory
"id": "br_8747ha",
// win of loss flag, <bool>, mandatory  
"win": true,

// All fields below are mandatory if "win" is "true", in case if loss they are absent
// impression cost (since there could be 2nd price auction), <float>
"price": 2.5,
// has click, <bool>
"click": false,
// has conversion, <bool>
"conversion": false,
// total revenue for this round, <int>
"revenue": 5
}
```

##### Response
| http code     | content-type                      | response                                                           |
|---------------|-----------------------------------|---------------------------------------------------------------------|
| `200`         | `text/plain;charset=UTF-8`        | ``                |


### Creative
##### `> GET /%creative_url%` 

| http code     | content-type                      | response                                                           |
|---------------|-----------------------------------|---------------------------------------------------------------------|
| `200`         | `image/png`  or `image/jpeg`      | `Creative image`                |

## DSP API (UI/Management part)

### Creative
##### `> POST /api/creatives/`
It will be sent with `Content-Type: application/json`
```json
// creative external id to track it in external systems, <string>, mandatory, should be unique across all creatives
"external_id": "external_id",
// creative name, string, mandatory
"name": "name",
// creative categories, list of <category objects with <string> 'code' field>, mandatory but it is allowed to pass empty list
"categories": [{"code": "IAB_7"}, {"code": "IAB_1-11"}],
// campaign object, <object with <int> 'id' field>, mandatory
"campaign": {"id": 1}
// base64 string with encoded image data, <string>, mandatory
"file": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M/wHwAEBgIApD5fRAAAAABJRU5ErkJggg=="

```

##### Response:
| http code     | content-type                      | response                                                           |
|---------------|-----------------------------------|---------------------------------------------------------------------|
| `201`         | `application/json`      | `The format is located below`               |

**Example:**
```json
{
// Internal ID of the creative object
"id": 10,
"external_id": "external_id",
"name": "name",
"categories": [{"id": 2, "code": "IAB_7"}, {"id":3, "code": "IAB_1-11"}],
"campaign": {"id": 11, "name": "campaign name"},
// URL of the uploaded creative ready for serving
"url": "http://127.0.0.1:3030/1/"
}
```

### Campaign/`
##### `> POST /api/campaigns/`

``` json
{
// <string>, mandatory
"name": "campaign name",
// <int>, mandatory
"budget": 60
// other fields must be optional
}
```

##### Response
| http code     | content-type                      | response                                                           |
|---------------|-----------------------------------|---------------------------------------------------------------------|
| `201`         | `application/json`      | `The format is located below`               |

```json
{
	// Campaign internal ID
	"id": 1,
	"name": "campaign name",
	"budget": 60,
	// ... your other fields
}
```

### Categories
All categories will be given in a file. You should write a management command to load all these categories into DB.

Categories should have the following fields:
```json
{
	// Internal ID of the category
	"id": 1,
	// Code of the category from IAB file
	"code": "IAB1",
	// Name of the category from IAB file
	"name": "Arts & Entertainment"
}
```

File with categories could be taken from here:  [link](https://iabtechlab.com/wp-content/uploads/2021/10/Content-Taxonomy-1.0.xlsx)


## Game initialization
##### `> POST /game/configure/`

```json
{
	// ALl fields are mandatory
	
	// number of rounds of the game, <int>
	"impressions_total": 10,
	// 1st or 2nd price auction, <int>, value must be 1 or 2
	"auction_type": 1,
	// game goal, <string>, "revenue" or "cpc"
	"game_goal": "revenue",
	// game mode, <string> - "free" or "script"
	"mode": "free",
	// total budget for every team, <int>
	"budget": 60,
	// revenue for every won impression, <int> 
	"impression_revenue": 3,
	// revenue for every click, <int>
	"click_revenue": 7,
	// revenue for every conversion, <int>
	"conversion_revenue": 30,
	// how many times one campaign could be shown to the same user without any fines, <int>
	"frequency_capping": 3,
}
```

### Response
| http code     | content-type                      | response                                                           |
|---------------|-----------------------------------|---------------------------------------------------------------------|
| `200`         | `application/json`      |              |
