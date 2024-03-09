from switchbot import SwitchBotClient, SwitchBotBot

import credentials


def main():
    client = SwitchBotClient(credentials.API_TOKEN, credentials.API_SECRET)
    devices = client.devices(SwitchBotBot)
    for d in devices:
        d.on()


if __name__ == '__main__':
    main()
