# -*- coding: utf-8 -*-

import os
import shutil
import unicodedata
import webbrowser
import re

import requests
from wox import Wox,WoxAPI
from bs4 import BeautifulSoup

URL = 'http://dig.chouti.com/all/hot/recent/1'

def full2half(uc):
    """Convert full-width characters to half-width characters.
    """
    return unicodedata.normalize('NFKC', uc)


class Main(Wox):

    def request(self,url):
    #如果用户配置了代理，那么可以在这里设置。这里的self.proxy来自Wox封装好的对象
		if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
			proxies = {
				"http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
				"https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))
			}
			return requests.get(url,proxies = proxies)
		else:
			return requests.get(url)

    def query(self, param):
		r = self.request(URL);
		bs = BeautifulSoup(r.text, 'html.parser')
		posts = bs.findAll('div', {'class': 'item'});
		result = []
		for p in posts:
                    target = p.find('a', {'class': 'show-content'})
                    title = re.sub('\s+', ' ', target.text)

                    subTitle = "chouti origin"
                    if p.find('span', {'class': 'content-source'}):
                        subTitle = p.find('span', {'class': 'content-source'}).text

                    item = {
                        'Title': title,
                        'SubTitle': subTitle,
                        'IcoPath': os.path.join('img', 'chouti.png'),
                        'JsonRPCAction': {
                            'method': 'open_url',
                            'parameters': [target['href']]
                        }
                    }

                    result.append(item)

		return result
	
    def openUrl(self, url):  
		webbrowser.open(url)

if __name__ == '__main__':
	Main()
