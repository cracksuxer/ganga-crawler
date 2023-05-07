from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from random import randint
import json
import time
import requests

URL = 'https://www.milanuncios.com/anuncios-en-tenerife'

with open('SCRAPEOPS_API_KEY.json') as f:
    data = json.load(f)
    SCRAPEOPS_API_KEY = data['SCRAPEOPS_API_KEY']

def get_headers_list():
    response = requests.get(
        f'http://headers.scrapeops.io/v1/browser-headers?api_key={SCRAPEOPS_API_KEY}'
    )
    json_response = response.json()
    return json_response.get('result', [])

def get_random_header(header_list):
    random_index = randint(0, len(header_list) - 1)
    return header_list[random_index]

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

driver.get(URL) # type: ignore
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ma-ContentListing-advertising-native')))

scroll_pause_time = 0.1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    if (screen_height) * i > scroll_height:
        break

with open('milanuncios.html', 'wb') as f:
    f.write(driver.page_source.encode('utf8'))