import sys
import re
import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import unicodecsv

current=time.strftime("%Y-%m-%d-%H%M",time.localtime()) #年月日時分
print("Current Time:",current)
filename = ['LOL_銅牌','LOL_銀牌','LOL_黃金','LOL_白金','LOL_鑽石','LOL_全部']#產生6個CSV檔 檔名

try:
    rec_time=str(input('是否依現在時間點來做CSV檔命名(以免覆蓋之前的時間點)? (y/N)'))
except:
    print("發生錯誤")
    raise
else:
    if(rec_time=='y' or rec_time== 'Y'):
        print("(依照時間點進行檔案命名)")
        filename = ['LOL_銅牌'+current,'LOL_銀牌'+current,'LOL_黃金'+current,'LOL_白金'+current,'LOL_鑽石'+current,'LOL_全部'+current]
    else:
        print("(不依時間點進行檔案命名)")
        
#網站的homepage(index page)排位為黃金
ranking = ['bronze','silver','','platinum','diamond','all']     #不同的排位，url的一部份
#           銅牌      銀牌  黃金    白金      鑽石      全部


rs = requests.session()

for r in range(len(ranking)):   #r 0~5
    url = 'https://www.leagueofgraphs.com/zh/champions/stats/'+ranking[r]
    res = rs.get(url, verify=True)
    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.select(".medium-24 tr")
    hl = soup.select(".medium-24 tr td a")
    hl_pat = re.compile(r'/zh/champions/stats/\w+') ##英雄之相對url，還沒對應到當前ranking(hurl)

    with open(filename[r]+'.csv', 'wb') as csvfile:
        writer = unicodecsv.writer(csvfile,encoding='utf-8-sig')
        writer.writerow(["編號","名字","選用率","勝率","禁用率","擊殺","死亡","助攻","場均五連殺","定位","定位","定位","勝率/遊戲時間","勝率/所有遊戲","勝率/(擊殺-死亡)@10分鐘","勝率/(擊殺-死亡)@20分鐘","url"])


        i=0
        h=0
        print("編號\t名字\t\t選用率\t勝率\t禁用率\t擊殺\t死亡\t助攻\t場均五連殺\t定位\t\t定位\t\t定位")


        try:
            for ele in table:       #table中每位英雄的tr      141次
                    
                    i=i+1
                    if(i==16 or i==17 or i==33 or i==49 or i==65 or i==81 or i==97 or i==113 or i==129 or i==145):  #網頁排版斷行
                        continue;
                    
                    tr_soup = BeautifulSoup(table[i].text, 'html.parser')
                    #print(tr_soup)
                    mytext=re.sub(" {1,}", " ", tr_soup.text)    #把多個空白縮減為一個空白
                    mytext=mytext.replace("\n","")
                    mytext=mytext.replace("\r","")

                    sp_pat = re.compile(r' ')      #空白符號作為斷格
                    result = re.split(sp_pat,mytext)
                    #print(result)
                    
                    pct_pat = re.compile(r'%')     #百分比符號作為斷格
                    hero = result[4]
                    pick = re.split(pct_pat,result[-10])
                    win = re.split(pct_pat,result[-9])
                    ban = re.split(pct_pat,result[-8])
                    kill = result[-7]
                    death = result[-5]
                    assist = result[-3]
                    ave5k = result[-2]
                    myspace='\t\t'     #排版用
                    if(len(hero)>=4):
                       myspace='\t'
                    else:
                       myspace='\t\t'
                    role=['','','']
                    if(result[-11]!=''):
                        role[0]=result[-11];
                        role[0]=role[0].replace(",","")
                        if(result[-12]!=''):
                            role[1]=result[-12];
                            role[1]=role[1].replace(",","")     #去除逗號
                            if(result[-13]!=''):
                                role[2]=result[-13];
                                role[2]=role[2].replace(",","")

                    myspace2='\t\t'     #排版用
                    if(len(role[0])>=4):
                       myspace2='\t'
                    else:
                       myspace2='\t\t'
                    
                    hlfind = hl_pat.findall(str(hl[h]))     #所有匹配hl_pat的相對url 在當前ranking中
                    hurl = 'https://www.leagueofgraphs.com'+str(hlfind[0])+'/'+str(ranking[r]) #獲得在當下ranking中此英雄的絕對url
                    print(hurl)
                    hlres = rs.get(hurl, verify=True)
                    hlsoup = BeautifulSoup(hlres.text, 'html.parser')
                    data_target = hlsoup.select(".medium-12 .box-padding-10 script")
                    #data_target[3]   #勝率/遊戲時間                   9個時間點
                    #data_target[4]   #勝率/所有遊戲                   9個時間點
                    #data_target[5]   #胜率/ (杀敌 - 死亡) @10分钟      11個點
                    #data_target[6]   #胜率/ (杀敌 - 死亡) @20分钟      21個點
                    data_pat = re.compile(r'-*\d+,\d+.\d+')
                    data1 = data_pat.findall(str(data_target[3]))   #勝率/遊戲時間 
                    data2 = data_pat.findall(str(data_target[4]))   #勝率/所有遊戲   
                    data3 = data_pat.findall(str(data_target[5]))   #胜率/ (杀敌 - 死亡) @10分钟
                    data4 = data_pat.findall(str(data_target[6]))   #胜率/ (杀敌 - 死亡) @20分钟
                    
                    role0 = role[0].encode("utf-8").decode("cp950", "ignore") # for print 簡字編碼問題 'cp950' codec can't encode character '\u8fdc'(远)
                    role1 = role[1].encode("utf-8").decode("cp950", "ignore")
                    role2 = role[2].encode("utf-8").decode("cp950", "ignore")                    
                    print(result[1],"\t",hero,myspace,pick[0]+"%\t",win[0]+"%\t",ban[0]+"%\t",kill[0]+"\t",death[0]+"\t",assist[0]+"\t",ave5k,"\t"+role[0]+myspace2+role[1]+"\t"+role[2]+"\t")
                    writer.writerow([result[1],hero,pick[0],win[0],ban[0],kill[0],death[0],assist[0],ave5k,role[0],role[1],role[2],data1,data2,data3,data4,hurl])
                    
                    h=h+1

        except  IndexError as e:    #超過141個英雄範圍之index
            print("---Ranking: ",ranking[r],"End ---")
            time.sleep(0.5)         #for requests.exceptions.ConnectionError
        except Exception as e:
            raise e
        
#總共846(不同網址) => 141英雄 * 6種排位        
    
rs.close()
print("====== END ======")
