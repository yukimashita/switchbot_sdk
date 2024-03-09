from switchbot import SwitchBotClient

import credentials


def main():
    client = SwitchBotClient(credentials.API_TOKEN, credentials.API_SECRET)
    scenes = client.scenes()
    for s in scenes:
        if s.sceneName == '留守':
            s.execute()


if __name__ == '__main__':
    main()
