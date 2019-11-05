'''
free proxy website:
https://free-proxy-list.net/
'''

import time
import requests
from bs4 import BeautifulSoup

UserAgent = "Chrome/77.0.3865.90"
headers = {'User-Agent': UserAgent}
response = requests.session()

url = "https://free-proxy-list.net/"

url_source = response.get(url, headers=headers).text
url_DOM = BeautifulSoup(url_source, 'html.parser')
#print(url_source)

proxy_txt = ''

for i in url_DOM.find('tbody').find_all('tr'):
    proxyInfo = i.find_all('td')
    proxy_ip = proxyInfo[0].getText()
    proxy_port = proxyInfo[1].getText()
    proxy_supportHttps = proxyInfo[6].getText()
    proxy_data = proxy_ip + ":" + proxy_port
    #print(proxy_data)
    
    proxy_txt = proxy_txt + proxy_data + "\n" 
    
print(proxy_txt)

with open ("./freeProxy.txt","w+") as f:
    f.write(proxy_txt)
