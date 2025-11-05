# Padi log importer
It imports a bundle of diving logs to the Padi platform, so you don't need to fill the logbook one by one.

## Why would you use it?
- It loads a csv file to import logs, which can be used with Google Sheets
- Replicating data is much easier with Sheets than Padi app
- A group of divers can work on the same sheet
- Handy after diving safari, no need to submit dives one by one
- Sheet can be shared with your diving buddy and group members

## How to use?

1. Fill out the dives.csv file, located in the folder

### Get auth token

1. Before opening logbook at learning.padi.com (but after login), right click in the browser -> inscpect
2. Click **Application** on top menu
3. Click **Local Storage** and select "https://learning.padi.com"
4. Then copy the value of the following key: "CognitoIdentityServiceProvider...**idToken**"

Insert your auth token into **insert_padi_log.py**:

```
auth_token = "YOUR_JWT_AUTH_TOKEN_GOES_HERE"
```

### Run script:

Install requirements:

`pip3 install -r requirements.txt`

Run script:

`python3.13 insert_padi_log.py`