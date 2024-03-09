class SwitchBotDevice:
    def __init__(self, client,
                 deviceId=None,
                 deviceName=None,
                 deviceType=None,
                 enableCloudService=None,
                 hubDeviceId=None):
        self.client = client
        self.deviceId = deviceId
        self.deviceName = deviceName
        self.deviceType = deviceType
        self.enableCloudService = enableCloudService
        self.hubDeviceId = hubDeviceId
        self._status = None

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
        if force_reload or self._status is None:
            self._status = self._get_status(None)
        return self._status

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
            'Ceiling Light Pro': SwitchBotCeilingLightPro,
            'Humidifier': SwitchBotHumidifier,
            'Plug Mini (US)': SwitchBotPlugMini,
            'Plug Mini (JP)': SwitchBotPlugMini,
            'WoIOSensor': SwitchBotOutdoorMeter,
            'Bot': SwitchBotBot,
            'Smart Fan': SwitchBotCirculator
        }
        cls = factories.get(device_json['deviceType'], cls)
        return cls(client, **device_json)

    @classmethod
    def from_device_list(cls, client, device_list):
        return [SwitchBotDevice.from_json(client, d) for d in device_list]


class SwitchBotCeilingLightPro(SwitchBotDevice):
    def status(self, force_reload=False):
        if force_reload or self._status is None:
            keys = ('power', 'brightness', 'colorTemperature')
            self._status = self._get_status(keys)
        return self._status

    def on(self):
        return self.commands('turnOn')

    def off(self):
        return self.commands('turnOff')

    def toggle(self):
        return self.commands('toggle')

    def brightness(self, brightness):
        return self.commands('setBrightness', str(brightness))

    def colorTemperature(self, colorTemperature):
        return self.commands('setColorTemperature', str(colorTemperature))


class SwitchBotHumidifier(SwitchBotDevice):
    def status(self, force_reload=False):
        if force_reload or self._status is None:
            keys = ('power', 'humidity', 'temperature',
                    'nebulizationEfficiency', 'auto',
                    'childLock', 'sound', 'lackWater')
            self._status = self._get_status(keys)
        return self._status

    def on(self):
        return self.commands('turnOn')

    def off(self):
        return self.commands('turnOff')

    def mode(self, mode):
        return self.commands('setMode', parameter=mode)


class SwitchBotPlugMini(SwitchBotDevice):
    def status(self, force_reload=False):
        if force_reload or self._status is None:
            keys = ('power', 'voltage', 'weight',
                    'electricityOfDay', 'electricCurrent', 'version')
            self._status = self._get_status(keys)
        return self._status

    def on(self):
        return self.commands('turnOn')

    def off(self):
        return self.commands('turnOff')

    def toggle(self):
        return self.commands('toggle')


class SwitchBotOutdoorMeter(SwitchBotDevice):
    def status(self, force_reload=False):
        if force_reload or self._status is None:
            keys = ('temperature', 'humidity')
            self._status = self._get_status(keys)
        return self._status


class SwitchBotBot(SwitchBotDevice):
    def status(self, force_reload=False):
        if force_reload or self._status is None:
            keys = ('version', 'power', 'battery', 'deviceMode')
            self._status = self._get_status(keys)
        return self._status

    def on(self):
        return self.commands('turnOn')

    def off(self):
        return self.commands('turnOff')

    def press(self):
        return self.commands('press')


class SwitchBotCirculator(SwitchBotDevice):
    def status(self, force_reload=False):
        if force_reload or self._status is None:
            keys = ('mode', 'version',
                    'battery', 'power', 'nightStatus',
                    'oscillation', 'verticalOscillation',
                    'chargingStatus', 'fanSpeed')
            self._status = self._get_status(keys)
        return self._status

    def on(self):
        return self.commands('turnOn')

    def off(self):
        return self.commands('turnOff')

    def nightLightMode(self, mode):
        # mode:
        #   'off': turn off nightlight
        #       1: bright
        #       2: dim
        assert mode in ('off', 1, 2, 'bright', 'dim')
        mode = dict(bright=1, dim=2).get(mode, mode)
        return self.commands('setNightLightMode', mode)

    def windMode(self, mode):
        # mode: 'direct', 'natural', 'sleep', 'baby'
        assert mode in ('direct', 'natural', 'sleep', 'baby')
        return self.commands('setWindMode', mode)

    def windSpeed(self, speed):
        assert 0 < speed <= 100
        return self.commands('setWindSpeedMode', speed)

    def fanSpeed(self, speed):
        """
        statusはfanSpeedだけどコマンドはsetWindSpeedModeなんだよなぁ
        上のwindMode, nightLightModeもそうだけど、statusとcommandは統一して欲しいな
        """
        return self.windSpeed(speed)

    #
    # ここから先リファレンスに書いてないので想像で書いてる
    #

    # 縦横の首振りはリモコンとアプリ両方でできるので
    # 何かしらの手段はあるはず
    def oscillation(self, mode):
        # statusCode=160が返ってきたコマンド一覧
        # - setOscillation
        # - setOscillationMode
        # - setOsc
        # - setOscMode
        # - oscillation
        # - oscillationMode
        return self.commands('oscillationMode', mode)
