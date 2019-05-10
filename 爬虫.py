from openpyxl import Workbook
from lxml import etree
import requests
import random
import time
import os

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
} #模拟浏览器
proxies = {"https": "xxxxxxxxxxxx", "http": "http://xxxxxxxxx"}  #设置代理池


wb = Workbook()
ws = wb.active
for i in range(70):
    url = 'https://xxxxxxx/ershoufang/pn%s/'%(str(i+1))  #目标地址
    response = requests.get(url=url,headers=headers,proxies=proxies) #获取页面的数据对象
    response.encoding = 'utf-8' #将页面的数据转成utf8
    page_text = response.text  #取出页面数据
    tree = etree.HTML(page_text) 
    url_list = tree.xpath('/html/body/div[5]/div[5]/div[1]/ul/li/div[2]/h2/a/@href') #取出关键数据
    phone_list=[]
    for url in url_list:
        print(url)
        try:
            detail_page_text = requests.get(url=url,headers=headers,proxies=proxies).text
        except:
            continue
        tree = etree.HTML(detail_page_text)
        try:
            phone = tree.xpath('//*[@id="houseChatEntry"]/div/p[3]/text()')[0]
        except:
            continue
        phone_list.append(str(phone))    
    ws.append(phone_list)
wb.save('phones.xlsx')