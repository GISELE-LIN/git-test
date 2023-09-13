import hashlib
import json
import logging
import random
import time
import uuid

from typing import Any, Dict, List

from locust.contrib.fasthttp import FastHttpUser

from common.lazy_propery import lazyproperty
from common.constants import (
    ANDROID,
    ANDROID_MODEL,
    ANDROID_VERSION,
    IOS,
    IOS_MODEL,
    IOS_VERSION,
    USER_AGENT,
)


class User(FastHttpUser):
    def __init__(self, environment):
        super().__init__(environment)
        self.open_id: str = ""
        self.api_headers: Dict[str, Any] = {
            "content-type": "application/json",
            "user-agent": USER_AGENT,
        }
        self.device_id = str(uuid.uuid4())
        self.device_type: str = random.choice([IOS, ANDROID])
        if self.device_type == IOS:
            self.api_headers["deviceType"] = IOS
            self.api_headers["version"] = IOS_VERSION
            self.device_model = IOS_MODEL
            self.app_version = IOS_VERSION
        else:
            self.api_headers["deviceType"] = ANDROID
            self.api_headers["version"] = ANDROID_VERSION
            self.device_model = ANDROID_MODEL
            self.app_version = ANDROID_VERSION

        langs = ["TW", "JP", "EN_US"]
        self.api_headers["language"] = random.choice(langs)

        regions = ["TW", "JP", "US"]
        self.api_headers["userSelectedRegion"] = random.choice(regions)
        self.api_headers["userIpRegion"] = random.choice(regions)
        self.api_headers["deviceID"] = self.device_id

    @lazyproperty
    def user_id(self) -> str:
        return self._user_info.get("userID", "")

    def _gen_open_id(self) -> str:
        open_id_pfx = ["lcuz1", "lcuz2"]
        chrs: str = "abcdefghijklmnopqrstuvwxyz"
        nums_1: List[int] = [8, 9, 10, 11, 15, 18, 19]  # for lcuz1
        nums_2: List[int] = [6, 7, 8, 9, 10, 16, 17, 18]  # for lcuz2

        o_pfx = random.choice(open_id_pfx)
        open_id = ""
        if o_pfx == "lcuz1":
            open_id = f"{o_pfx}{str(random.choice(nums_1))}{str(random.randint(0,9))}{random.choice(chrs)}{str(random.randint(1,200))}"
        if o_pfx == "lcuz2":
            open_id = f"{o_pfx}{str(random.choice(nums_2))}{str(random.randint(0,9))}{random.choice(chrs)}{str(random.randint(1,200))}"

        return open_id

    def _do_login(self, open_id: str, password: str) -> None:
        resp = self.post_api_gateway(
            action="loginAction2", open_id=self.open_id, password=password
        )

        data = {}
        i = 0
        if resp.status_code != 200:
            while i < 3:
                i += 1
                time.sleep(2**i)
                resp = self.post_api_gateway(
                    action="loginAction2", open_id=self.open_id, password=password
                )
                if resp.status_code == 200:
                    break
            else:
                logging.error(f"login failed - {resp.status_code}: {resp.text}")
                self.stop(force=True)

        obj = json.loads(resp.text)
        data = json.loads(obj["data"])

        self.jwt_access_token = data["jwtAccessToken"]
        self._user_info = data["userInfo"]

        self.api_headers["Authorization"] = f"Bearer {self.jwt_access_token}"

    def login(self, open_id: str = None, password: str = None) -> None:
        """do 17 login via openID/password"""
        self.open_id = self._gen_open_id() if open_id is None else open_id.strip()

        if password is None:
            password = "ba327879b8d1287857ff8881bf3498e5"
        else:
            password = hashlib.md5(password.encode()).hexdigest()

        time.sleep(random.random() * 2)

        self._do_login(open_id=self.open_id, password=password)

    def post_api_gateway(
        self,
        action: str,
        open_id: str = None,
        password: str = None,
    ):
        payload: str = ""

        if action == "loginAction2":
            payload = (
                '{"action":"%s","apiVersion":"v2","openID":"%s","password":"%s","deviceID":"%s"}'
                % (action, open_id, password, self.device_id)
            )

        body: Dict[str, str] = {
            "key": "",
            "data": payload,
            "cypher": "0_v2",
        }

        resp = self.client.post(
            "/apiGateWay",
            headers=self.api_headers,
            data=json.dumps(body),
            name=f"/apiGateWay/[{action}]",
        )

        return resp
