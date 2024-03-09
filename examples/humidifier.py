import time

from switchbot import SwitchBotClient, SwitchBotHumidifier

import credentials


def main():
    client = SwitchBotClient(credentials.API_TOKEN, credentials.API_SECRET)
    devices = client.devices(SwitchBotHumidifier)
    for d in devices:
        status = d.status()

        if status['power'] == 'on':
            d.off()
        else:
            d.on()

        time.sleep(20)

        if status['power'] == 'on':
            d.on()
        else:
            d.off()


if __name__ == '__main__':
    main()
