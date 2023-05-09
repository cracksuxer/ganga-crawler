from typing import List, Union
from xmlrpc.client import Boolean
from bs4 import BeautifulSoup, NavigableString, Tag
from rich.traceback import install
from rich.console import Console
from box import Box
import re
from Add import Add

console = Console()
install(show_locals=True, theme='monokai', word_wrap=True)

def check_good_tag(tag: Union[Tag, None, NavigableString]) -> Boolean:
    return tag is not None and isinstance(tag, Tag)

def scrap_add(article: Tag) -> Union[Add, None]:
    photo_container = Box({
        'img_title': '',
        'link': ''
    })

    details = Box({
        'add_title': '',
        'title_link': 'https://www.milanuncios.com',
        'prices': Box({}),
        'location': False,
        'description': '',
        'label': Box({})
    })

    ma_AdCardV2_photoContainer = article.find('div', {'class': 'ma-AdCardV2-photoContainer'})
    if check_good_tag(ma_AdCardV2_photoContainer):
        try:
            img_title = ma_AdCardV2_photoContainer.img['title'] # type: ignore
            img_link = ma_AdCardV2_photoContainer.img['src'] # type: ignore
            photo_container.img_title = img_title
            photo_container.link = img_link
        except TypeError:
            console.log('TypeError: ma_AdCardV2_photoContainer.img is None')
    else:
        console.log('ma_AdCardV2_photoContainer is None or not Tag')

    ma_AdCardV2_detail = article.find('div', class_='ma-AdCardV2-detail')
    if check_good_tag(ma_AdCardV2_detail):
        extract_details(ma_AdCardV2_detail, details)
    console.log(f'Added: {details.add_title}')

    return Add(
        details.add_title, # type: ignore
        photo_container.link, # type: ignore
        details.title_link, # type: ignore
        photo_container.img_title, # type: ignore
        details.prices, # type: ignore
        details.location,
        details.description,
        details.label # type: ignore
    )

def extract_details(ma_AdCardV2_detail, details):
    ma_AdCardV2_detail_a = ma_AdCardV2_detail.find('a', class_='ma-AdCardListingV2-TitleLink') # type: ignore
    if check_good_tag(ma_AdCardV2_detail_a):
        details.title_link += ma_AdCardV2_detail_a.get('href') # type: ignore
        details.add_title = ma_AdCardV2_detail_a.get('title') # type: ignore
    else:
        console.log('ma_AdCardV2_detail_a is None or not Tag')

    ma_AdMultiplePrice = ma_AdCardV2_detail.find('div', class_='ma-AdMultiplePrice') # type: ignore
    if check_good_tag(ma_AdMultiplePrice):
        prices_list = []
        for p in ma_AdMultiplePrice: # type: ignore
            label_group = []
            for span in p: # type: ignore
                price_label = re.sub(r'\s+', ' ', span.text.strip()) # type: ignore
                label_group.append(price_label)
            prices_list.append(label_group)
        details.prices = prices_list # type: ignore
    else:
        console.log('ma_AdMultiplePrice is None or not Tag')

    ma_AdLocation_text = ma_AdCardV2_detail.find('span', class_='ma-AdLocation-text') # type: ignore
    if check_good_tag(ma_AdLocation_text):
        details.location = ma_AdLocation_text.get_text() # type: ignore
    else:
        console.log('ma_AdLocation_text is None or not Tag')

    ma_AdCardV2_description = ma_AdCardV2_detail.find('p', class_='ma-AdCardV2-description') # type: ignore
    if check_good_tag(ma_AdCardV2_description):
        details.description = ma_AdCardV2_description.get_text() # type: ignore
    else:
        console.log('ma_AdCardV2_description is None or not Tag')

    ma_AdTag_label = ma_AdCardV2_detail.find('ul', class_='ma-AdTagList') # type: ignore
    if check_good_tag(ma_AdTag_label):
        label_list = []
        for span in ma_AdTag_label: # type: ignore
            label = re.sub(r'\s+', ' ', span.text.strip()) # type: ignore
            label_list.append(label)
        details.label = label_list
    else:
        console.log('ma_AdTag_label is None or not Tag')
    
    
html_docs = [
    'milanuncios.html',
    'milanuncios5.html',
    'milanuncios6.html',
    'milanuncios8.html',
    'milanuncios9.html',
]

add_list: List[Add] = []
for html_doc in html_docs:    
    html_doc = open(html_doc, 'r', encoding='utf8').read()
    soup = BeautifulSoup(html_doc, 'html.parser')
        
    for article in soup.find_all('article'):
        if article is None:
            continue
        add: Union[Add, None] = scrap_add(article)
        if add is not None:
            add_list.append(add)
            
for add in add_list:
    console.print(f'{add.title} - {add.prices} - {add.location} - {add.img_link}')

# for article in soup.find_all('article'):
#     aux = article.find('div', {'class': 'ma-AdCardV2-photoContainer'})
#     if article.get_text() == '' or aux is None:
#         continue
#     console.print(aux.prettify())
#     console.print('-------------------')

# add_count: int = 0
# for add in soup.find_all('article'):
#     if add.get_text() == '':
#         continue
#     console.print(add.prettify())
#     console.print(add.get_text())
#     console.print('-------------------')
#     add_count += 1
    
# console.print(f'Add Count: {add_count}')

# Label: Destacado, Nuevo, etc
# img alt: Main image + title
# href title: ma-AdCardListingV2-TitleLink
# desc: div class='ma-AdCardV2-row
# 