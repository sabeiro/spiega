# app

# java

## Android connect sql - 2013

App to interact with a SQL database

## TantoSurvey - 2013

App to fill a livelihood survey on a remote database

![tanto_survey](../f/f_dauvi/njombe.svg "tanto survey")
_Tanto survey_

The survey is populated using a json template.

# cordova

Cordova is an early '10 cross platform application builder which allows to develop apps from web application. Functionalities like native SDK are mainly not included since the app is mainly rendering a web view.

## Canova and VeneziaÈUnica - 2014

**Canova** is an app wrote to log the completion of a cleaning server per bus. Features:

* loading workers' information
* log which bus was cleaned at what time
* store the information offline in case of low connectivity
* sync the information with the server
* admin login
* admin worker and bus entry change

![apps](../portfolio/f/apps.png "apps")
_canova and Venezia è unica_

**Venezia è unica** is an app (mock up) to purchase coupons and transportation tickets from a single place. Adding more purchase will activate a discount.

## Gardalì - 2014

A portal to connect professionals from the agricultural industry and an IoT server to monitor sensor data. Features:

* insert 

![gardali](../portfolio/f/services.png "gardali")
_gardalì portal_

# angular

Here are few examples of apps written in nodejs 

# geocode - 2020

[Geocode](https://github.com/intertino/app/nodejs/geocode/) is an app to anonymize addresses. It takes a list of addresses and parse line by line using a geocode service and applying the anonymization required: i.e. remove digits from coordinates or use geohash.

![geocode](../f/f_intertino/cover_geocode.png "geocode cover")
_geocode app_

The core or the application is a chain of promises 

```javascript
async function parse_row(row) {
  var initPromise = geocode(row['address_call']);
  initPromise.then(function(coord_call){
					 var initPromise2 = geocode(row['address_stroke_unit']);
					 initPromise2.then(
					   function(coord_unit){
						 var coord = {'lat_unit':coord_unit['lat'],'lng_unit':coord_unit['lng']
									  ,'lat_call':coord_call['lat'],'lng_call':coord_call['lng']};
						 row_db = key_row(row,coord);
						 row2db(row_db);
					   }, errHandler
					 )
					 return initPromise2;
				   }
				   , errHandler
				  ).then(function(data){
				  }, errHandler
	);
```

# text corrector - 2023

[text corrector](https://github.com/intertino/app/nodejs/text_corrector/) is an automated assistant to help writing outreach sales emails. 

![cover_corrector](../f/f_intertino/cover_corrector.png "text corrector")

_text corrector overview_

## usage

The user starts editing the draft in the left box, the draft is composed in different sections:

* subject
* greeting
* presentation
* value proposition
* personalization
* goodbye
* signature

![block_editor](../f/f_intertino/block_editor.png "block editor")

_the editor block composed in sections_

Every time a change is made an algo evaluates the distance from the previous version is computed. The current algo is a mixture of Levenshtein and time difference. 
If the change is consistent enough the current text is appended to a prompt for the language model which can be edited in this section:

![block_criteria](../f/f_intertino/block_criteria.png "block criteria")

_the criteria block with editable prompts_

The resquest is sent to the backend that appends the authentification and sends the request to the language model. Within few seconds the response is formated and displayed in the correction block:

![block_correction](../f/f_intertino/block_correction.png "block correction")

_the correction block with suggestions_

The correction block has an apply button that validates the correction and apply the change.

Alternatively there is an instruction section with editable prompts

![block_instruction](../f/f_intertino/block_instruction.png "block instruction")

_the instruction block with editable prompts_

That would send a request to the language model to generate the email following the instructions

![block_generated](../f/f_intertino/block_generated.png "block generated")

_the generated block with suggestions_

## technical implementation

The app is mainly written in `nodejs` using `express` and `ejs`. The main functions are written in `javascript` and executes on the frontend.

![front_back](../f/f_intertino/front_back.svg "front back")

_front- and back- end implementation_

The implementation is as following

![node_calls](../f/f_intertino/node_call.svg "node calls")

_structure of the calls_

## deployment

Create an `.env` file with:
```
export OPENAI_KEY=...
```
run

```
npm install
npm start
```

or

```
cd build/
docker-compose up -d
```

The app is then available at:

```
localhost:3000/correct
```
