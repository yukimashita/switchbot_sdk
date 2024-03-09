from switchbot import SwitchBotClient, SwitchBotWebhook

import credentials


def main():
    client = SwitchBotClient(credentials.API_TOKEN, credentials.API_SECRET)
    webhooks = client.webhooks()
    if len(webhooks) == 0:
        print('nothing')
    else:
        for w in webhooks:
            print(w.delete())
    url = 'https://your.endpoint/here'
    w = SwitchBotWebhook.create(client, url)
    print(w)


if __name__ == '__main__':
    main()
