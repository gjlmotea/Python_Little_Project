searchKeyword = "福利"
##如搜尋結果有多個頁面，一個頁面一個執行緒
#Keyword:YUZUKI、小丁Cosplay、福利
web = "https://asiansister.com/"
searchPage_url = "https://asiansister.com/tag.php?tag=" + searchKeyword
UserAgent = "Chrome/77.0.3865.90"




def get_and_save_all_Hpicture(url):
    import requests
    from bs4 import BeautifulSoup
    headers = {'User-Agent': UserAgent}
    response = requests.session()
    searchPage_source = response.get(url, headers=headers).text
        

    searchPage_DOM = BeautifulSoup(searchPage_source, 'html.parser')
    searchPage_itemBox_Tags = searchPage_DOM.select(".itemBox")


    import os
    import urllib.request
    opener = urllib.request.build_opener()
    opener.addheaders = [(UserAgent, 'Chrome/77.0.3865.90')]

    for itemBox_Tag in searchPage_itemBox_Tags:
        viewPage_uri = itemBox_Tag.a.get("href")
        viewPage_url = web + viewPage_uri
        print("正在進入..." + viewPage_url)
        
        viewPage_source = response.get(viewPage_url, headers=headers).text
        viewPage_DOM = BeautifulSoup(viewPage_source, 'html.parser')

        image_Tags = viewPage_DOM.find_all("img", class_ = "lazyload showMiniImage")
        
        for image_Tag in image_Tags:
            image_uri_path = image_Tag.get("dataurl")[5:]
            image_uri = image_uri_path.split('/')[-1]
            image_url = web + image_uri_path
            
            if "_t.jpg" in image_url:       ## VIP picture
                image_url = image_url[:-6] + image_url[-4:]
            print(image_uri)

            dir_path = './' + searchKeyword + '/' + viewPage_uri[5:] 
            savepath = './' + searchKeyword + '/' + viewPage_uri[5:] + '/' + image_uri
                
            urllib.request.install_opener(opener)
            try:
                urllib.request.urlretrieve(image_url, savepath)
            except FileNotFoundError:
                os.makedirs(dir_path)
                urllib.request.urlretrieve(image_url, savepath)
            except urllib.error.HTTPError:
                #找不到該原始圖片，抓取縮圖
                print("404 Error... Can't find this picture origin size.")
                urllib.request.urlretrieve(image_url[:-4] + '_t' + image_url[-4:], savepath)





import requests
from bs4 import BeautifulSoup
headers = {'User-Agent': UserAgent}
response = requests.session()
searchPage_source = response.get(searchPage_url, headers=headers).text

searchPage_DOM = BeautifulSoup(searchPage_source, 'html.parser')
searchPage_itemBox_Tags = searchPage_DOM.select(".itemBox")


if "btn page" in searchPage_source:
    page_btns = searchPage_DOM.find_all("a", class_ = "btn page")
    page_total = len(page_btns) + 1

    import threading
    threads = []
    for i in range(page_total):
        searchArgument = "&page=" + str(i+1)
        searchPage_url = "https://asiansister.com/tag.php?tag=" + searchKeyword + searchArgument
        print("===== 第 " + str(i+1) + " 頁: " + searchPage_url)
        threads.append(threading.Thread(target = get_and_save_all_Hpicture, args = (searchPage_url,)))
    for i in range(page_total):
        threads[i].start()
    for i in range(page_total):
        threads[i].join()
        
    
else:
    import os
    import urllib.request
    opener = urllib.request.build_opener()
    opener.addheaders = [(UserAgent, 'Chrome/77.0.3865.90')]

    for itemBox_Tag in searchPage_itemBox_Tags:
        viewPage_uri = itemBox_Tag.a.get("href")
        viewPage_url = web + viewPage_uri
        print("正在進入..." + viewPage_url)
        
        viewPage_source = response.get(viewPage_url, headers=headers).text
        viewPage_DOM = BeautifulSoup(viewPage_source, 'html.parser')

        image_Tags = viewPage_DOM.find_all("img", class_ = "lazyload showMiniImage")
        
        for image_Tag in image_Tags:
            image_uri_path = image_Tag.get("dataurl")[5:]
            image_uri = image_uri_path.split('/')[-1]
            image_url = web + image_uri_path
            
            if "_t.jpg" in image_url:       ## VIP picture
                image_url = image_url[:-6] + image_url[-4:]
            print(image_uri)

            dir_path = './' + searchKeyword + '/' + viewPage_uri[5:] 
            savepath = './' + searchKeyword + '/' + viewPage_uri[5:] + '/' + image_uri
                
            urllib.request.install_opener(opener)
            try:
                urllib.request.urlretrieve(image_url, savepath)
            except FileNotFoundError:
                os.makedirs(dir_path)
                urllib.request.urlretrieve(image_url, savepath)



