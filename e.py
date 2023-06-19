from flask import Flask, request, jsonify, Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from .proxies import proxies
from random import choice
import re


app = Flask(__name__)
options = Options()
userAgent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/112.0.0.0 Safari/537.36')
options.add_argument(f'user-agent={userAgent}')
options.add_argument('window-size=1200,800')
options.add_argument('--headless')
proxy = choice(proxies)
options.proxy = {
    'http': proxy,
    'https': proxy,
}
driver = webdriver.Chrome(options=options)


@app.route('/e/basket/<articul>')
def get_basket(articul):
    url = f'https://www.wildberries.ru/catalog/{articul}/detail.aspx'
    driver.get(url)
    img = driver.find_elements(By.CSS_SELECTOR, '.zoom-image-container img')
    if len(img):
        src = img[0].get_attribute('src')
        basket = int(re.search(r'basket-(\d+)', src).group(1))
        return {
           'basket': basket
        }
    else:
        return {
           'basket': None
        }
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
