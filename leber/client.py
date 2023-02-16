import requests
import json
from .utility import *
from typing import List, Dict
from .logger import Logger
import random

class LeberClient:
    host = "https://api.leber11.com:443"
    need_update = False

    def __init__(self, mobile: str = "", password: str = "", info: Dict = {}):
        self.logger = Logger()
        
        if len(info):
            self.user = info
        
        else:
            session_id = random.randint(0, 10000)

            if not mobile.startswith('+'):
                mobile = to_global_mobile(mobile)

            headers = {
                "Content-Type": "application/json"
            }

            payload = {
                "login": mobile, 
                "password": password
            }

            res = requests.post(self.host + "/v9//users/sign_in", headers=headers, data=json.dumps(payload))

            self.log_response(res, session_id)

            if res.status_code != 200:
                self.logger.error(f"({session_id}) Failed to login (code: {res.status_code})")
                raise Exception

            resj = json.loads(res.text)

            if resj['status'] != 1:
                self.logger.error(f"({session_id}) Failed to log in (status: {resj['status']})")
                raise Exception

            self.user = resj['result']['user']

            self.session_id = -1
        
        if not "auto_submit" in self.user:
            self.need_update = True
            self.user["auto_submit"] = False

    def getTemprtureQuestion(self, session_id = -1) -> Dict:
        if session_id == -1:
            session_id = random.randint(0, 10000)

        headers = {
            "x-user-token": self.user['authentication_token']
        }

        params = {
            "language_code": "ja",
            "patient_id": self.user['patients'][0]['id']
        }

        res = requests.get(self.host + "/v9//temperature_questions", params=params, headers=headers)

        self.log_response(res, session_id)

        if res.status_code != 200:
            self.logger.error(f"({session_id}) Failed to get temperture question (code: {res.status_code})")

        res = json.loads(res.text)

        if res['status'] != 1:
            self.logger.error(f"({session_id}) Failed to get temperture question (message: {res['message']})")

        return res

    def submitTemperture(self, answer: List[int], session_id = -1):
        if session_id == -1:
            session_id = random.randint(0, 10000)
        
        headers = {
            "content-type": "application/json",
            "x-user-token": self.user['authentication_token']
        }

        payload = {
            "company_id": self.user['patients'][0]['company_id'],
            "temp_answers_attributes":[
                {
                    "additional_comment": "",
                    "answer_id": [data],
                    "question_id": idx+1,
                    "question_number": idx+1
                }
                for idx, data in enumerate(answer)
            ]
        }

        res = requests.post(
            self.host + f"/v9//patients/{self.user['patients'][0]['id']}/submit_temperatures", 
            headers=headers, 
            data=json.dumps(payload)
            )

        self.log_response(res, session_id)

        if res.status_code != 200:
            self.logger.error(f"({session_id}) Failed to submit health data (code: {res.status_code})")

        res = json.loads(res.text)

        if res['status'] != 1:
            self.logger.error(f"({session_id}) Failed to submit health data (status: {res['status']})")

    def log_response(self, res: requests.Response, session_id: int):
        self.logger.info(f"({session_id}) Request to       : {res.request.url}")
        self.logger.info(f"({session_id}) Request Header   : {res.request.headers}")
        self.logger.info(f"({session_id}) Request Data     : {res.request.body}")
        self.logger.info(f"({session_id}) Response Status  : {res.status_code}")
        self.logger.info(f"({session_id}) Response Preview : {res.text[:100]}")