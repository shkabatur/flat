import requests
import json
import re
from time import sleep
from functools import reduce
from pprint import pprint

#переводив текстовое число в формат необходимый для генерации запроса
def ord_digits(d):
    return reduce( lambda a,b: '.' +  str(ord(b)) + a, list(d)[::-1], '')

def parse_page(page):
    contacts = []
    
    NAME_POS = 6
    NUMBER_POS = 7
    REGISTERED_POS = 8
    LOCATION_POS = 9
    STEP = 5
    
    current = 0
    page = page.split('<td style="width:10%;min-width: 70px;">')
    for i in range(10):
        contact = {}
        try:
            contact["name"]         = page[NAME_POS + (i * STEP)].split("</td>")[0]
        except:
            break
        contact["number"]       = page[NUMBER_POS + (i * STEP)].split("</td>")[0]
        registered   = page[REGISTERED_POS + (i * STEP)].split("</td>")[0]
        contact["location"]     = page[LOCATION_POS + (i * STEP)].split("</td>")[0]
        if  registered == "Да":
            contacts.append(contact)
    return contacts
    

def login():
    auth_url = "https://172.16.4.208/auth"
    login_headers = {
        "Host": "172.16.4.208",
        "Connection": "keep-alive",
        "Content-Length": "113",
        "Cache-Control": "max-age=0",
        "Origin": "https://172.16.4.208",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; ONEPLUS A3010) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://172.16.4.208/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }
    login_payload = "login=21232f297a57a5a743894a0e4a801fc3&login0=&pass=202cb962ac59075b964b07152d234b70&pass0=&UserName=&UserDomain="

# логинимся
    login_request = requests.post(auth_url, data=login_payload, headers=login_headers, verify=False)
# получаем наш ssid
    refer = login_request.text.split()[9][1:-2]
    ssid = refer.split('=')[1]
    return ssid
    

def get_page(n,ssid, url):
    page_number = str(n-1)

    """
    GET /abn?sh=1&page=.114&pager=.49.55&f1=.49&f2=.49.50.51&search=&SSID=.48.49.50.54.5.56&oldsort=.123.79.76.68.83.79.82.84.125&oldsortobr=.123.79.76.68.83.79.82.84.79.66.82.125&selM=.123.83.69.76.77.125&pag=.49.54&zonaID=.49& HTTP/1.1
    Host: 172.16.4.208
    Connection: keep-alive
    Cache-Control: max-age=0
    If-Modified-Since: Sat, 1 Jan 2000 00:00:00 GMT
    User-Agent: Mozilla/5.0 (Linux; Android 7.1.1; ONEPLUS A3010) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36
    Accept: */*
    Referer: https://172.16.4.208/index?SSID=01264424762580834826266826374353882634243002347228
    Accept-Encoding: gzip, deflate, br
    Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7
    """

    get_url = url + "/abn?sh=1&page=.114&pager=" + ord_digits(page_number) + "&f1=.49&f2=.49.50.51" + "&search=&SSID=" + ord_digits(ssid) + "&pag=.52&zonaID=.49"

    get_headers = {
        "Host": "172.16.4.208",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "If-Modified-Since": "Sat, 1 Jan 2000 00:00:00 GMT",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; ONEPLUS A3010) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Accept": "*/*",
        "Referer": "https://172.16.4.208/index?SSID=" + ssid,
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    r = requests.get(get_url, headers=get_headers, verify=False)
    return r.text
    

#------------------------------------------------------------------------------    
url = "https://172.16.4.208"
ssid = login()

contacts = []

for i in range(1,91):
    page = get_page(i,ssid,url)

    contacts.extend(parse_page(page))
for c in contacts: print(c)

with open ('json.txt', 'w+', encoding="utf-8") as f:
    f.write(json.dumps(contacts))
    
