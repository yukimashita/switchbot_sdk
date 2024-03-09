from switchbot import SwitchBotClient, SwitchBotOutdoorMeter

import credentials


def main():
    client = SwitchBotClient(credentials.API_TOKEN, credentials.API_SECRET)
    devices = client.devices(SwitchBotOutdoorMeter)
    for d in devices:
        status = d.status()
        s = f'{d.deviceName}: {status["temperature"]}℃ {status["humidity"]}%'
        print(s)


if __name__ == '__main__':
    main()
