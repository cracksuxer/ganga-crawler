from seleniumwire import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager


INPUT = 'milanuncios_unloaded9.html'
OUTPUT = 'milanuncios9.html'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get(f'file:///C:/Users/Rules/Desktop/ganga-crawler/App/{INPUT}')

scroll_pause_time = 0.5
screen_height = driver.execute_script("return window.screen.height;")
i = 1

while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    if (screen_height) * i > scroll_height:
        break
    
with open(OUTPUT, 'wb') as f:
    f.write(driver.page_source.encode('utf8'))