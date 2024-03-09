from switchbot import SwitchBotClient, SwitchBotCirculator

import credentials


def main():
    client = SwitchBotClient(credentials.API_TOKEN, credentials.API_SECRET)
    devices = client.devices(SwitchBotCirculator)
    for d in devices:
        print('--')
        print(d)
        print(d.status())
#        print(d.on())
#        print(d.nightLightMode('off'))
        print(d.oscillation('off'))


if __name__ == '__main__':
    main()
