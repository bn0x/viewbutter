import requests
import threading
import json
import sys
import random
from time import sleep

class main:
    def __init__(self):
        self.session = requests.session()
        self.viewers = 800
        self.proxies = open("C:\GAY", 'r').readlines()
        self.username = "misscammie"
        self.headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)'}
        for i in range(self.viewers):
            if i <= self.viewers:
                gayShit = random.choice(self.proxies).strip()
                proxy = {'http': gayShit, 'https': gayShit}
                print(proxy)
                threading.Thread(target=self.view, args=[proxy]).start()
                sys.stdout.write('\rViewers Started: %d'%i)
            else:
                break

    def view(self, proxy):
        mySession = requests.session()
        while True:
            try:
                m3u8Url = self.go(mySession, proxy)
                for i in range(10):
                    mySession.get(
                                     m3u8Url,
                                     verify=False,
                                     headers=self.headers,
                                     proxies=proxy
                                 )
                sleep(3)
                continue
            except:
                sleep(3)
                continue


    def go(self, session, proxy):
        accessTokenRequest = session.get("http://api.twitch.tv/api/channels/%s/access_token"%self.username,
                                                    headers=self.headers,
                                                    params={'as3': 't'},
                                                    proxies=proxy,
                                                    verify=False)
        json = accessTokenRequest.json()
        m3u8Request = session.get("http://usher.twitch.tv/select/%s.json?nauth=%s" % (self.username, str(json['token'])),
                                            params={'private_code': '', 'allow_source': 'true', 'type': 'any', 'p': '1000000', 'nauthsig': json['sig']},
                                            headers=self.headers,
                                            proxies=proxy,
                                            verify=False)
        m3u8Url = m3u8Request.text.split()[-1]
        return m3u8Url

if __name__ == "__main__":
    main()