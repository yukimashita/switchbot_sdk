from switchbot import SwitchBotClient, SwitchBotCeilingLightPro

import credentials


def main():
    client = SwitchBotClient(credentials.API_TOKEN, credentials.API_SECRET)
    devices = client.devices(SwitchBotCeilingLightPro)
    for d in devices:
        status = d.status()
        if status['power'] == 'on':
            continue
        d.brightness(10)
        d.colorTemperature(2700)
        d.on()


if __name__ == '__main__':
    main()
