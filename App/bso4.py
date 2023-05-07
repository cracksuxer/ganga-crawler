from calendar import c
from http import cookies
from bs4 import BeautifulSoup
from rich.traceback import install
from rich.console import Console
console = Console()
install(show_locals=True, theme="monokai", word_wrap=True)

html_doc = open('milanuncios.html', 'r', encoding='utf8').read()

soup = BeautifulSoup(html_doc, 'html.parser')


count: int = 0
for add in soup.find_all('article'):
    if add.get_text() == '':
        continue
    console.print(add.get_text())
    console.print('-------------------')
    count += 1
    
console.print(f'Count: {count}')