import re
from bs4 import BeautifulSoup
import requests
# import sys
from multiprocessing import Pool, Lock, Value
mutex = Lock()
n_processed = Value('i', 0)
def get_info(id_):
#     sys.setrecursionlimit(1000000)
    info_ = dict()
    _html = requests.get('https://www.bookvoed.ru/book?id='+str(id_)).text
    soup = BeautifulSoup(_html, 'html.parser')
    name_ = soup.find('h1').contents[0]
    if(soup.find('div', class_='ov nM')):
        age_ = '0+'
    elif(soup.find('div', class_='qv nM')):
        age_ = '6+'
    elif(soup.find('div', class_='pv nM')):
        age_ = '12+'
    elif(soup.find('div', class_='rv nM')):
        age_ = '16+'
    elif(soup.find('div', class_='sv nM')):
        age_ = '18+'
    else:
        age_ = 'Nothing AGE Press F'
    if(soup.find('img', class_='tf')):
        image_ = soup.find('img', class_='tf').get('src')
    else:
        image_ = '-'
    if(soup.find('div', class_='lw')):
        descr_ = soup.find('div', class_='lw')
        descr_ = str(descr_).split('"lw">')[1]
        descr_ = str(descr_).split(' <div')[0]
        descr_ = re.sub('\s+', ' ', descr_[1:])
    else:
        descr_ = '-'
    if(soup.find('a', class_='Ke Le ')):
        rat_  = '-'
    elif(soup.find('a', class_='Ke Le ff')): #text.replace("\n", "0"))):
        rat_ = int(soup.find('a', class_='Ke Le ff').text.replace("\n", "0"))
    else:
        rat_  = '-'
    if(soup.find('a', class_='Ke Me ')):
        ratingP_ = int(soup.find('a', class_='Ke Me ').text.replace("\n", "0"))
    else:
        ratingP_ = 0
    if(soup.find('a', class_='Ke Oe ')):
        ratingN_ = int(soup.find('a', class_='Ke Oe ').text.replace("\n", "0"))
    else:
        ratingN_ = 0
    if(ratingP_ != 0 or ratingN_ != 0):
        rating_ = round(ratingP_/(ratingP_+ratingN_)*100, 1)
    else:
        rating_ = '-'
    if(soup.find('meta', itemprop='price')):
        price_ = soup.find('meta', itemprop='price').get('content')
    else:
        price_ = 'Отсутствует в продаже'
    ser_ = soup.findAll('tr', class_='uw')
    table = {}
    if(ser_):
        for i in ser_:
            ff = i.find(class_='vw').text
            rr = i.find(class_='ww').text
            table[ff] = rr
    info_ = {
        "ID": id_,
        "Название": str(name_),
        "Обложка": image_,
        "Возраст": age_,
        "Описание": descr_,
        "Рейтинг": rating_,
        "Понравилось": ratingP_,
        "В закладки": rat_,
        "Не понравилось": ratingN_,
        "Цена": price_
    }
    info_ = {**info_, **table}
    return info_

def func_wrapper(uid):
    res = get_info(uid)
    with mutex:
        global n_processed
        n_processed.value += 1
        if n_processed.value % 10 == 0:
            print(f"\r{n_processed.value} objects are processed...", end='', flush=True)
    return res
