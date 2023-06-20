from flask import Flask, request, jsonify, Response
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from random import choice
import re
from time import sleep 
from random_user_agent.user_agent import UserAgent
import requests

user_agent_rotator = UserAgent()

proxies = [
    'http://CrCWgH3r:bb3KGpCE@91.230.38.109:64220',
    'http://CrCWgH3r:bb3KGpCE@45.85.66.206:50933',
    'http://CrCWgH3r:bb3KGpCE@194.55.105.13:47634',
    'http://CrCWgH3r:bb3KGpCE@45.140.64.241:46385',
    'http://CrCWgH3r:bb3KGpCE@45.154.160.110:61956',
    'http://CrCWgH3r:bb3KGpCE@45.154.163.79:49156',
    'http://CrCWgH3r:bb3KGpCE@91.236.121.164:47682',
    'http://CrCWgH3r:bb3KGpCE@45.152.117.122:63971',
    'http://CrCWgH3r:bb3KGpCE@77.83.80.63:53622',
    'http://CrCWgH3r:bb3KGpCE@194.156.93.162:63025',
    'http://CrCWgH3r:bb3KGpCE@45.10.108.222:47210',
    'http://CrCWgH3r:bb3KGpCE@45.142.254.151:59861',
    'http://CrCWgH3r:bb3KGpCE@45.144.37.181:49839',
    'http://CrCWgH3r:bb3KGpCE@212.193.164.24:46273',
    'http://CrCWgH3r:bb3KGpCE@195.209.145.2:57269',
    'http://CrCWgH3r:bb3KGpCE@195.208.21.18:50040',
    'http://CrCWgH3r:bb3KGpCE@212.193.171.171:47732',
    'http://CrCWgH3r:bb3KGpCE@212.193.168.135:50421',
    'http://CrCWgH3r:bb3KGpCE@195.209.188.116:46413',
    'http://CrCWgH3r:bb3KGpCE@195.209.135.55:53533',
    'http://CrCWgH3r:bb3KGpCE@195.208.84.102:46432',
    'http://CrCWgH3r:bb3KGpCE@212.193.167.162:51246',
    'http://CrCWgH3r:bb3KGpCE@212.193.102.119:52577',
    'http://CrCWgH3r:bb3KGpCE@212.193.162.212:48864',
    'http://CrCWgH3r:bb3KGpCE@212.192.228.195:62665',
    'http://CrCWgH3r:bb3KGpCE@212.192.192.235:51607',
    'http://CrCWgH3r:bb3KGpCE@212.192.168.210:45786',
    'http://CrCWgH3r:bb3KGpCE@195.208.56.149:59609',
    'http://CrCWgH3r:bb3KGpCE@195.208.110.210:64662',
    'http://CrCWgH3r:bb3KGpCE@195.208.117.194:53780',
    'http://CrCWgH3r:bb3KGpCE@195.208.20.87:50544',
    'http://CrCWgH3r:bb3KGpCE@195.19.219.150:49585',
    'http://CrCWgH3r:bb3KGpCE@212.192.58.76:49214',
    'http://CrCWgH3r:bb3KGpCE@212.192.59.89:61151',
    'http://CrCWgH3r:bb3KGpCE@212.193.186.222:46301',
    'http://CrCWgH3r:bb3KGpCE@212.193.187.144:47355',
    'http://CrCWgH3r:bb3KGpCE@212.193.188.155:62075',
    'http://CrCWgH3r:bb3KGpCE@212.193.189.44:58696',
    'http://CrCWgH3r:bb3KGpCE@212.193.190.137:52004',
    'http://CrCWgH3r:bb3KGpCE@212.193.191.199:56319',
    'http://CrCWgH3r:bb3KGpCE@212.193.185.134:45901',
    'http://CrCWgH3r:bb3KGpCE@193.232.89.127:55065',
    'http://CrCWgH3r:bb3KGpCE@194.190.211.31:59906',
    'http://CrCWgH3r:bb3KGpCE@5.8.51.45:62666',
    'http://CrCWgH3r:bb3KGpCE@31.184.243.108:51805',
    'http://CrCWgH3r:bb3KGpCE@109.196.165.103:46090',
    'http://CrCWgH3r:bb3KGpCE@109.94.211.191:50361',
    'http://CrCWgH3r:bb3KGpCE@194.32.239.170:59713',
    'http://CrCWgH3r:bb3KGpCE@194.32.238.125:52494',
]

app = Flask(__name__)
# proxy = choice(proxies)
proxy = 'http://CrCWgH3r:bb3KGpCE@45.140.64.241:46385'
options = Options()
userAgent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/112.0.0.0 Safari/537.36')
options.add_argument(f'user-agent={userAgent}')
options.add_argument('window-size=1200,800')
options.add_argument('--headless')
sw_options = {
    'proxy': {
        'http': proxy,
        'https': proxy
    }
}
driver = webdriver.Chrome(seleniumwire_options=sw_options, options=options)


@app.route('/e/test')
def test():
    driver.get('https://ipinfo.io')
    ip = '45.140.64.241'
    return {
        'title': driver.title,
        'ip': ip in driver.find_element(By.CSS_SELECTOR, 'html').get_attribute('outerHTML')
    }
    'http://CrCWgH3r:bb3KGpCE@45.140.64.241:46385'


@app.route('/e/basket/<articul>')
def get_basket(articul):
    # 148276125
    url = f'https://www.wildberries.ru/catalog/{articul}/detail.aspx'
    driver.get(url)
    img = driver.find_elements(By.CSS_SELECTOR, '.zoom-image-container img')
    while len(img) == 0:
        sleep(0.3)
        img = driver.find_elements(By.CSS_SELECTOR, '.zoom-image-container img')
        print(len(img))
    # if len(img):
    src = img[0].get_attribute('src')
    basket = int(re.search(r'basket-(\d+)', src).group(1))
    return {
        'basket': basket
    }
    # else:
    #     return {
    #        'basket': None
    #     }


https://basket-05.wb.ru/vol796/part79616/79616275/info/sellers.json
https://basket-10.wb.ru/vol1595/part159521/159521068/info/sellers.json

@app.route('/e/bf/<articul>')
def bf_basket(articul):
    baskets = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for basket in baskets:
        url = 'https://basket-' + basket + '.wb.ru/vol' + str(articul)[:-5] + '/part'
        url += str(articul)[:-3] + '/' + str(articul) + '/info/sellers.json'
        headers = {
            'User-Agent': user_agent_rotator.get_random_user_agent()
        }
        proxy = choice(proxies)
        response = requests.get(url, headers=headers, proxies={
            'http': proxy,
            'https': proxy,
        })
        if response.status_code == 200:
            break
    return {
        'basket': int(basket)
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
