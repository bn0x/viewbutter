from __future__ import print_function
import requests
import threading
import sys
import argparse
import random
from time import sleep

proxyCount = {}

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-u', '--username', help="username", default="chikari")
parser.add_argument('-p', '--proxies', help="proxies file", default="C:/proxies.txt")
parser.add_argument('-v', '--viewers', help="viewers count", default=150, type=int)
args = parser.parse_args()


class viewbot(object):
    def __init__(self, proxy, args=args, proxyCount=proxyCount, errors=0):
        self.username = args.username
        self.headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)'}
        self.proxy = {
            'http': 'http://%s'%proxy.strip(),
            'https': 'http://%s'%proxy.strip(),
        }
        self.session = requests.session()
        while True:
            try:
                if errors == 15:
                    return
                self.m3u8 = self.getM3U8Url()
                while True:
                    self.session.get(self.m3u8,
                                     headers=self.headers,
                                     proxies=self.proxy,
                                     verify=False)
                    errors -= 1
                    sleep(3)
            except:
                errors += 1
                continue

    def getM3U8Url(self):
        self.getAccessToken = self.session.get("http://api.twitch.tv/api/channels/%s/access_token"%self.username,
                                                headers=self.headers,
                                                params={'as3': 't'},
                                                proxies=self.proxy,
                                                verify=False,).json()

        self.getM3U8 = self.session.get("http://usher.twitch.tv/select/%s.json"%self.username,
                                        params={
                                            'nauth': self.getAccessToken['token'],
                                            'private_code': '',
                                            'allow_source': True,
                                            'type': 'any',
                                            'p': 1000000,
                                            'nauthsig': self.getAccessToken['sig'],
                                        },
                                        headers=self.headers,
                                        proxies=self.proxy,
                                        verify=False,)
        return self.getM3U8.content.split()[-1]

if __name__ == "__main__":
    proxies = open(args.proxies, 'r').readlines()
    if len(proxies) < args.viewers:
        sys.exit('You need more proxies bro.')
    for proxy in proxies:
        proxyCount[proxy.strip()] = 0
    for viewer in range(args.viewers):
        while True:
            proxies[viewer] = proxies[viewer].strip()
            if proxyCount[proxies[viewer].strip()] < 10:
                threading.Thread(target=viewbot, args=[proxies[viewer]]).start()
                proxyCount[proxies[viewer]] += 1
                break
            else:
                viewer = int(random.choice(range(len(proxies))))
                continue
        sys.stdout.write("\rViewers Started: %d"%viewer)
    print()
    while True:
        sys.stdout.write("\rViewers Currently Running: %d"%threading.activeCount())
        sleep(1)