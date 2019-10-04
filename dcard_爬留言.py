import time

topic_url = "https://www.dcard.tw/f/joke/p/232224230"
count = 0  #+1
argu = "&limit=1"
url = topic_url + "/comments?after=" + str(count) + argu

# cookie = dict(__cfduid= "")


import requests
from bs4 import BeautifulSoup
UserAgent = "Chrome/77.0.3865.90"
headers = {'User-Agent': UserAgent}
response = requests.session()
source = response.get(url, headers=headers).text
# source = response.get(url, headers=headers, cookies=cookie).text

print(source[:8000])


while(1):
    try:
        if "id" in source:
            print("第" + str(count+1) + "樓有回應")
            filename = str(count+1) + ".txt"
            with open(filename, "w",encoding="utf-8") as text_file:
                print(source, file=text_file)

            count = count + 1
            url = web + str(count) + argu
            source = response.get(url, headers=headers, cookies=cookie).text
            time.sleep(1)
        else:
            time.sleep(2)
            #print(".", end='')
            source = response.get(url, headers=headers, cookies=cookie).text
    except Exception as e:
        #print(e)
        time.sleep(1)
