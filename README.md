#Photobomb

Capture SMS/MMS data sent to a phone number into a Dropbox folder.  Dropbox folder will contain one directory for each
sender's phone number, which will amount to a log/store of messages and media.

## Installation (brief)
1. Configure a Dropbox app and note the API token
2. Deploy this code to a remote server (set `DROPBOX_TOKEN` env var) and note the URL
3. Configure Twilio to send `POST` messages to the URL

## Installation using Heroku (detailed)
1. configure Dropbox
  - sign up for a Dropbox and log in
  - go to https://www.dropbox.com/developers (see link in footer of Dropbox)
  - go to My Apps (see nav links at left)
  - click Create App button
  - Choose an API: **"Dropbox API"**
  - Choose type of access you need: **"App Folder"**
  - Name your app: type in a name, like "my-law-office-photobomb"
  - Finish the form by clicking "Create App" button at bottom
  - Now seeing the app's config screen (titled, as per previous example, "my-law-office-photobomb", scroll down to section called OAuth2
  - Under "Generate access token", click "Generate" button
2. configure Heroku
  - sign up for $7/mo "hobby" (can't do free plan, because it will miss some of the callback requests)
  - install up Heroku CLI: https://devcenter.heroku.com/articles/heroku-command-line
  - git clone this repository: `$ git clone <repo-address-here>`
  - navigate into the app's code: `$ cd <repo-name>`
  - set 'heroku' git remote `$ git add remote heroku <heroku-app-git-address-here>`
  - set `DROPBOX_TOKEN` env var in heroku app: `$ heroku config:set DROPBOX_TOKEN=<token>`
  - push code to heroku remote: `$ git push heroku`
3. configure Twilio
  - set up a Twilio account (cost is $50 for the number, $1/month, $.01/message)
  - configure callback URL for `POST` based on Heroku URL

## Environment variables
 - `DROPBOX_TOKEN` - Dropbox OAuth2 Token (required)
 - `TWILIO_ACCOUNT_SID` - Twilio Account SID (required)
 - `TWILIO_AUTH_TOKEN` - Twilio Auth Token (required)
 - `TWILIO_DELETE_MEDIA` - Whether to remove media from Twilio after retrieval. Default: `False`
 - `TWILIO_DELETE_MESSAGES` - Whether to remove messages from Twilio after retrieval. Default: `False`
