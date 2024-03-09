class SwitchBotRemote:
    black_id_list = [
        '02-202012121137-44787258',
        '02-202012121140-59655760'
    ]

    def __init__(self,
                 client,
                 deviceId=None,
                 deviceName=None,
                 remoteType=None,
                 hubDeviceId=None):
        self.client = client
        self.deviceId = deviceId
        self.deviceName = deviceName
        self.remoteType = remoteType
        self.hubDeviceId = hubDeviceId
        self._state = None

    def _path(self, path=None):
        if path is None:
            return f'devices/{self.deviceId}'
        if path.startswith('/'):
            path = path[1:]
        return f'devices/{self.deviceId}/{path}'

    def _get_status(self, keys):
        path = self._path('status')
        res = self.client.get_json(path)
        status = res['body']
        if keys is None:
            return status
        return {k: status[k] for k in keys}

    def status(self, force_reload=False):
        if force_reload or self._state is None:
            self._status = self._get_status(None)
        return self._status

    def delete(self):
        path = self._path()
        return self.client.delete(path)

    def commands(self, command, parameter='default', commandType='command'):
        path = self._path('commands')
        data = {
            'command': command,
            'parameter': parameter,
            'commandType': commandType
        }
        return self.client.post_json(path, data)

    def __str__(self):
        class_name = type(self).__name__
        return f'<<{class_name}: {self.deviceName}>>'

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_json(cls, client, device_json):
        factories = {
            'Air Conditioner': SwitchBotRemoteAirConditioner,
            'Light': SwitchBotRemoteLight
        }
        cls = factories.get(device_json['remoteType'], cls)
        return cls(client, **device_json)

    @classmethod
    def from_device_list(cls, client, remote_list):
        return [SwitchBotRemote.from_json(client, r)
                for r in remote_list if r['deviceId'] not in SwitchBotRemote.black_id_list]


class SwitchBotRemoteAirConditioner(SwitchBotRemote):
    MODE_AUTO = 1
    MODE_COOL = 2
    MODE_DRY = 3
    MODE_FAN = 4
    MODE_HEAT = 5

    FAN_AUTO = 1
    FAN_LOW = 2
    FAN_MEDIUM = 3
    FAN_HIGH = 4

    def on(self, temperature=25, mode=MODE_AUTO, fanSpeed=FAN_AUTO):
        parameter = f'{temperature},{mode},{fanSpeed},on'
        return self.commands('setAll', parameter)

    def off(self):
        parameter = '25,1,1,off'
        return self.commands('setAll', parameter)


class SwitchBotRemoteLight(SwitchBotRemote):
    def on(self):
        return self.commands('turnOn')

    def off(self):
        return self.commands('turnOff')

    def brightnessUp(self):
        return self.commands('brightnessUp')

    def brightnessDown(self):
        return self.commands('brightnessDown')
