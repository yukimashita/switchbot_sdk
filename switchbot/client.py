import base64
import hashlib
import hmac
import json
import uuid
import time

import requests

from .devices import SwitchBotDevice
from .remotes import SwitchBotRemote
from .scenes import SwitchBotScene
from .webhooks import SwitchBotWebhook
from .version import __version__


API_VERSION = 'v1.1'
API_URL = 'https://api.switch-bot.com'
USER_AGENT = f'SwitchBot SDK/{__version__}'


class SwitchBotClient:
    def __init__(self, api_token,
                 api_secret,
                 api_version=API_VERSION,
                 api_url=API_URL,
                 request_interval_seconds=5):
        self.api_token = api_token
        self.api_secret = api_secret
        self.api_version = api_version
        self.api_url = api_url
        self._request_interval_seconds = request_interval_seconds
        self._devices = None
        self._remotes = None
        self._scenes = None
        self._webhooks = None

    def _auth(self, headers):
        nonce = uuid.uuid4()
        t = int(time.time() * 1000)
        string_to_sign = bytes(f'{self.api_token}{t}{nonce}', 'utf-8')
        secret = bytes(self.api_secret, 'utf-8')
        mac = hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256) \
            .digest()
        sign = base64.b64encode(mac)
        headers['Authorization'] = self.api_token
        headers['charset'] = 'utf-8'
        headers['t'] = str(t)
        headers['sign'] = str(sign, 'utf-8')
        headers['nonce'] = str(nonce)

    def _user_agent(self, headers):
        if 'User-Agent' not in headers:
            headers['User-Agent'] = USER_AGENT

    def _url(self, path):
        if path.startswith('/'):
            path = path[1:]
        return f'{self.api_url}/{self.api_version}/{path}'

    def get(self, path, headers=dict(), params=dict(), retries=3):
        url = self._url(path)
        headers = headers.copy()
        self._auth(headers)
        self._user_agent(headers)
        for i in range(retries):
            res = requests.get(url, headers=headers, params=params)
            time.sleep(self._request_interval_seconds)
            sc = int(res.status_code / 100)
            if sc in (4, 5):
                time.sleep(self._request_interval_seconds)
                continue
            return res
        res.raise_for_status()

    def get_json(self, path, headers=dict(), params=dict()):
        return self.get(path, headers, params).json()

    def post(self, path, data, headers=dict(), params=dict(), retries=3):
        url = self._url(path)
        headers = headers.copy()
        self._auth(headers)
        self._user_agent(headers)
        if isinstance(data, dict):
            data = json.dumps(data)
            headers['Content-Type'] = 'application/json'
        for i in range(retries):
            res = requests.post(url, headers=headers, data=data, params=params)
            time.sleep(self._request_interval_seconds)
            sc = int(res.status_code / 100)
            if sc in (4, 5):
                time.sleep(self._request_interval_seconds)
                continue
            return res
        res.raise_for_status()

    def post_json(self, path, data, headers=dict(), params=dict()):
        return self.post(path, data, headers, params).json()

    def devices(self, classes=None):
        if self._devices is None:
            res = self.get_json('devices')
            device_list = res['body']['deviceList']
            self._devices = SwitchBotDevice.from_device_list(self, device_list)
            remote_list = res['body']['infraredRemoteList']
            self._remotes = SwitchBotRemote.from_device_list(self, remote_list)
        if classes is None:
            return self._devices
        if isinstance(classes, list):
            classes = tuple(classes)
        return [d for d in self._devices if isinstance(d, classes)]

    def remotes(self, classes=None):
        if self._remotes is None:
            res = self.get_json('devices')
            device_list = res['body']['deviceList']
            self._devices = SwitchBotDevice.from_device_list(self, device_list)
            remote_list = res['body']['infraredRemoteList']
            self._remotes = SwitchBotRemote.from_device_list(self, remote_list)
        if classes is None:
            return self._remotes
        if isinstance(classes, list):
            classes = tuple(classes)
        return [r for r in self._remotes if isinstance(r, classes)]

    def scenes(self):
        if self._scenes is None:
            res = self.get_json('scenes')
            scene_list = res['body']
            self._scenes = SwitchBotScene.from_scene_list(self, scene_list)
        return self._scenes

    def webhooks(self):
        if self._webhooks is None:
            data = dict(action="queryUrl")
            res = self.post_json('webhook/queryWebhook', data)
            if res['statusCode'] == 190:
                return []
            webhook_list = res['body']['urls']
            self._webhooks = SwitchBotWebhook \
                .from_webhook_list(self, webhook_list)
        return self._webhooks
