from typing import Dict

import json
from datetime import datetime, timezone
import uuid

import requests
import time

from internal.exceptions import ResourceNotFoundException, UnknownAPIException


class TeamsClient:

    def __init__(self, search_token: str, message_token: str, skype_token: str) -> None:
        self.search_token = search_token
        self.message_token = message_token
        self.skype_token = skype_token


    def get_user_by_email(self, email: str) -> Dict:

        url = "https://teams.live.com/api/mt/beta/users/searchUsers"

        payload = "{\"emails\": [\"%s\"]}" % email
        headers = {
            'x-ms-client-type': 'cdlworker',
            'authorization': f'Bearer {self.search_token}',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'content-type': 'application/json;charset=UTF-8',
            'x-skypetoken': self.skype_token,
            'accept': 'application/json',
            'Referer': 'https://teams.live.com/v2/worker/precompiled-web-worker-9fa4124376d71a9e.js',
            'x-ms-client-caller': 'SEARCH_SUGGESTIONS'
        }

        response = self.send_request("POST", url, headers, payload)

        if response.status_code != 200:
            raise UnknownAPIException(f"error {response.status_code} fetching user from api: " + response.text)
        
        response_json = response.json()
        user_profiles = response_json[email]["userProfiles"]
        if len(user_profiles) == 0:
            raise ResourceNotFoundException(f"User with email {email} not found")
        
        user_json = user_profiles[0]
        return user_json
    
    def create_chat(self, skype_id: str, user_id: str) -> str:

        url = "https://teams.live.com/api/groups/v1/threads"

        payload = json.dumps({
        "members": [
            {
            "id": f"8:{skype_id}",
            "role": "User"
            },
            {
            "id": user_id,
            "role": "User"
            }
        ],
        "properties": {
            "threadType": "chat",
            "isStickyThread": "true"
        }
        })
        headers = {
        'x-ms-client-type': 'cdlworker',
        'authorization': f'Bearer {self.message_token}',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'content-type': 'application/json',
        'x-skypetoken': self.skype_token,
        'Referer': 'https://teams.live.com/v2/worker/precompiled-web-worker-9fa4124376d71a9e.js'
        }

        response = self.send_request("POST", url, headers, payload)

        if response.status_code != 200:
            raise UnknownAPIException(f"error {response.status_code} fetching user from api: " + response.text)
        
        response_json = response.json()
        return response_json["value"]["threadId"]

    def send_message(self, chat_id: str, skype_id: str, message_text: str) -> None:

        url = f"https://teams.live.com/api/chatsvc/consumer/v1/users/ME/conversations/{chat_id}/messages"

        current_time = str(datetime.now(timezone.utc).isoformat())[:23] + "Z"

        clientmessageid = str(uuid.uuid4().int)[:19]


        payload = json.dumps({
            "id": "-1",
            "type": "Message",
            "conversationid": chat_id,
            "conversationLink": f"blah/{chat_id}",
            "from": f"8:{skype_id}",
            "composetime": current_time,
            "originalarrivaltime": current_time,
            "content": f"<p>{message_text}</p>",
            "messagetype": "RichText/Html",
            "contenttype": "Text",
            "clientmessageid": clientmessageid,
            "callId": "",
            "state": 0,
            "version": "0",
            "amsreferences": [],
            "properties": {
                "importance": "",
                "subject": "",
                "title": "",
                "cards": "[]",
                "links": "[]",
                "mentions": "[]",
                "onbehalfof": None,
                "files": "[]",
                "policyViolation": None
            },
            "crossPostChannels": []
        })
        headers = {
            'clientinfo': 'os=linux; osVer=undefined; proc=x86; lcid=en-us; deviceType=1; country=us; clientName=skypeteams; clientVer=1415/24102001545; utcOffset=+05:00; timezone=Asia/Karachi',
            'x-ms-request-priority': '0',
            'Referer': 'https://teams.live.com/v2/worker/precompiled-web-worker-9fa4124376d71a9e.js',
            'behavioroverride': 'redirectAs404',
            'authentication': f'skypetoken={self.skype_token}',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'content-type': 'application/json'
        }

        response = self.send_request("POST", url, headers, payload)

        if response.status_code != 201:
            raise UnknownAPIException(f"error {response.status_code} sending message: {response.text}")

    def send_request(self, method: str, url: str, headers: Dict, payload: Dict) -> requests.Response:
        try:
            return requests.request(method, url, headers=headers, data=payload)
        except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError):
            print("Connection error. Retrying request in 5 seconds...")
            time.sleep(5)
            return self.send_request(method, url, headers, payload)
    