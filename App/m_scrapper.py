from this import d
from mdurl import URL
from seleniumwire import webdriver
from random import randint
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
import json
import time
import requests

from typing import Any, List

URLS = [ 
    # 'https://www.milanuncios.com/anuncios-en-tenerife/?pagina=10',
    # 'https://www.milanuncios.com/anuncios-en-tenerife/?pagina=11',
    # 'https://www.milanuncios.com/anuncios-en-tenerife/?pagina=12',
    # 'https://www.milanuncios.com/anuncios-en-tenerife/?pagina=13',
    # 'https://www.milanuncios.com/anuncios-en-tenerife/?pagina=14',
    'https://www.milanuncios.com/anuncios-en-tenerife/?pagina=15',
    'https://www.milanuncios.com/anuncios-en-tenerife/?pagina=16',
    'https://www.milanuncios.com/anuncios-en-tenerife/?pagina=17',
    'https://www.milanuncios.com/anuncios-en-tenerife/?pagina=18',
    'https://www.milanuncios.com/anuncios-en-tenerife/?pagina=19'
]

with open('../SCRAPEOPS_API_KEY.json') as f:
    data = json.load(f)
    SCRAPEOPS_API_KEY = data['API_KEY']

def get_headers_list():
    response = requests.get(
        f'http://headers.scrapeops.io/v1/browser-headers?api_key={SCRAPEOPS_API_KEY}'
    )
    json_response = response.json()
    return json_response.get('result', [])

def get_random_header(header_list: List[Any]):
    random_index = randint(0, len(header_list) - 1)
    return header_list[random_index]

proxy_options = {
    'proxy': {
        'http': f'http://scrapeops.headless_browser_mode=true.country=es:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'https': f'http://scrapeops.headless_browser_mode=true.country=es:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'no_proxy': 'localhost:127.0.0.1'
    }
}

options = webdriver.ChromeOptions()
# option.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-sh-usage')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--blink-settings=imagesEnabled=false')

driver = webdriver.Chrome(ChromeDriverManager().install(), 
                            options=options, 
                            seleniumwire_options=proxy_options)



# driver.get(URL) # type: ignore
# WebDriverWait(driver, 2)

# with open('milanuncios_unloaded.html', 'wb') as f:
#     f.write(driver.page_source.encode('utf8'))

for url in URLS:
    driver.get(url)
    WebDriverWait(driver, 2)
    with open(f'milanuncios_unloaded{url[-1]}.html', 'wb') as f:
        f.write(driver.page_source.encode('utf8'))