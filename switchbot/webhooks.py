class SwitchBotWebhook:
    def __init__(self, client,
                 url,
                 createTime=None,
                 lastUpdateTime=None,
                 deviceList=None,
                 enable=None):
        self.client = client
        self.url = url
        self.createTime = createTime
        self.lastUpdateTime = lastUpdateTime
        self.deviceList = deviceList
        self.enable = enable

    def _path(self, path):
        if path.startswith('/'):
            path = path[1:]
        return f'webhook/{path}'

    def details(self):
        if self.lastUpdateTime is None:
            path = self._path('queryWebhook')
            data = dict(action='queryDetails', urls=[self.url])
            res = self.client.post_json(path, data)
            details = res['body']
            assert len(details) == 1
            detail = details[0]
            assert self.url == detail['url']
            self.createTime = detail['createTime']
            self.lastUpdateTime = detail['lastUpdateTime']
            self.deviceList = detail['deviceList']
            self.enable = detail['enable']
        return self.dict()

    def update(self, enable):
        action = 'updateWebhook'
        path = self._path(action)
        data = {
            'action': action,
            'config': {
                'url': self.url,
                'enable': enable
            }
        }
        res = self.client.post_json(path, data)
        if res['statusCode'] == 100:
            self.lastUpdateTime = None
        return res

    def delete(self):
        action = 'deleteWebhook'
        path = self._path(action)
        data = {
            'action': action,
            'url': self.url
        }
        res = self.client.post_json(path, data)
        if res['statusCode'] == 100:
            self.lastUpdateTime = None
        return res

    def dict(self):
        return {
            'url': self.url,
            'createTime': self.createTime,
            'lastUpdateTime': self.lastUpdateTime,
            'deviceList': self.deviceList,
            'enable': self.enable
        }

    def __str__(self):
        class_name = type(self).__name__
        return f'<<{class_name}: {self.url}>>'

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_json(cls, client, webhook_json):
        return cls(client, url=webhook_json)

    @classmethod
    def from_webhook_list(cls, client, webhook_list):
        return [SwitchBotWebhook.from_json(client, w) for w in webhook_list]

    @classmethod
    def create(cls, client, url):
        path = 'webhook/setupWebhook'
        data = dict(action='setupWebhook', url=url, deviceList='ALL')
        client.post_json(path, data)
        return cls(client, url=url)
