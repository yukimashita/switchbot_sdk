import time

from switchbot import SwitchBotClient, SwitchBotCeilingLightPro

import credentials


def main():
    client = SwitchBotClient(credentials.API_TOKEN, credentials.API_SECRET)
    devices = client.devices(SwitchBotCeilingLightPro)
    for d in devices:
        status = d.status()

        print(f'{d.deviceName}: 10% 2700K')
        d.on()
        d.brightness(10)
        d.colorTemperature(2700)
        time.sleep(20)

        print(f'{d.deviceName}: 100% 6500K')
        d.brightness(100)
        d.colorTemperature(6500)
        time.sleep(20)

        # restore to state
        s = f'{d.deviceName}: ' \
            f'{status["brightness"]}% ' \
            f'{status["colorTemperature"]}K'
        print(s)
        if status['power'] == 'on':
            d.on()
        else:
            d.off()
        d.brightness(status['brightness'])
        d.colorTemperature(status['colorTemperature'])


if __name__ == '__main__':
    main()
