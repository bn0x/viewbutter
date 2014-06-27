import requests
import threading
import json
import sys
import random
from time import sleep

class main:
    def __init__(self):
        self.session = requests.session()
        self.proxysUsed = {}
        self.viewers = int(sys.argv[2])
        self.proxies = open(sys.argv[3], 'r').readlines()
        for proxy in self.proxies:
            self.proxysUsed[proxy.strip()] = 0
        print("[+] Proxies loaded in dict")
        self.username = sys.argv[1]
        self.headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)'}
        for i in range(self.viewers):
            if i <= self.viewers:
                while True:
                    gayShit = random.choice(self.proxies).strip()
                    if self.proxysUsed[gayShit] < 10:
                        break
                    else:
                        continue
                self.proxysUsed[gayShit] += 1
                proxy = {'http': gayShit, 'https': gayShit}
                threading.Thread(target=self.view, args=[proxy]).start()
                sys.stdout.write('\r[+] Viewers Started: %d'%i)
            else:
                break
        print("")
        while True:
            sys.stdout.write("\r[+] Viewers still running: %d"%threading.activeCount())
            sleep(0.5)

    def view(self, proxy):
        errors = 0
        mySession = requests.session()
        while True:
            if errors == 15:
                return
            try:
                m3u8Url = self.go(mySession, proxy)
                for i in range(10):
                    mySession.get(
                                     m3u8Url,
                                     verify=False,
                                     headers=self.headers,
                                     proxies=proxy
                                 )
                errors -= 1
                sleep(3)
                continue
            except:
                errors += 1
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