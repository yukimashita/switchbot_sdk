import json

from switchbot import SwitchBotClient

import credentials


def main():
    client = SwitchBotClient(credentials.API_TOKEN, credentials.API_SECRET)
    devices = client.devices()
    for d in devices:
        status = d.status()
        print(f'{d.deviceName}:')
        print(json.dumps(status, indent=2))


if __name__ == '__main__':
    main()
