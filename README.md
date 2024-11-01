# MS Teams (Personal Account) Bot

A bot designed to send messages to users in bulk for MS teams personal account. It takes in an excel file of users' emails and sends the given message to all the users.


## Instructions to run:

- Install requirements using `pip install -r requirements.txt`
- Get your SEARCH_TOKEN, MESSAGE_TOKEN, and SKYPE_TOKEN from the teams app. To do this, you need to login to Teams in your browser, and run the provided javascript code in the dev console. The code can be found at `scripts/extract_tokens.js`. This will give you the SEARCH_TOKEN and MESSAGE_TOKEN. For the SKYPE_TOKEN, you need to go to Dev console -> Application tab -> Cookies -> https://teams.live.com -> Search for "skypetoken", copy the cookie value.
- Create a new file `.env` and place the tokens inside this file. The file should look like `.env.example`
- Run the code using `python main.py`


# Video Instructions:

https://www.loom.com/share/db798307ed2244bc8379bc3edc3147ea?sid=9ce8d866-7332-4083-8b47-a13d2bcf55aa

To get skype token: https://www.loom.com/share/df4c55b95bb14dc9bff5c20d986bf0cb