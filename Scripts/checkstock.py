#!/usr/bin/env python3
# Basic stock checker by making manual searches for a product (NMD in this case)
# Need to update this to be more general

import requests
import re
import json
import time
from bs4 import BeautifulSoup as bs

query = "nmd"

def einhalb():
    print ('43einhalb...')
    response = session.get('http://www.43einhalb.com/en/search?searchstring=' + query)
    soup = bs(response.text, 'html.parser')
    productListing = soup.find('ul', {'class' : 'productListing'})
    items = productListing.findAll('li', {'class' : 'item'})
    for item in items:
        variantListing = item.find('ul', {'class' : 'availableVariants'})
        links = variantListing.findAll('li', {'title' : ''})
        for link in links:
            printToSheet(item.find('span', {'class' : 'productName'}).getText(), 'http://www.43einhalb.com' + link.find('a')['href'])
            
def overkill():
    print ('Overkill...')
    response = session.get('https://www.overkillshop.com/en/catalogsearch/result/?q=' + query)
    soup = bs(response.text, 'html.parser')
    productListing = soup.find('ul', {'class' : 'products-grid'})
    if not productListing is None:
        items = productListing.findAll('li', {'class' : 'item'})
        for item in items:
            variantListing = item.find('ul', {'class' : 'text-left'})
            if not variantListing is None:
                links = variantListing.findAll('a', {'label_show' : ''})
                for link in links:
                    if 'disabled' not in link.attrs['class']:
                        printToSheet(item.find('a', {'class' : 'product-name'})['title'], link['href'])

def sns():
    print ('Sneakersnstuff...')
    response = session.get('http://www.jdsports.co.uk/search/' + query + '/')
    soup = bs(response.text, 'html.parser')
    items = soup.findAll('li', {'class' : 'product'})
    for item in items:
        desc = item.find('p')
        if desc.getText() != 'Sold out':
            printToSheet(item.find('a', {'class' : 'plink name'}), 'http://www.sneakersnstuff.com' + item.find('a')['href'])

def oneblockdown():
    print ('One Block Down...')
    response = session.get('http://www.oneblockdown.it/en/search/' + query)
    soup = bs(response.text, 'html.parser')
    scripts = soup.findAll('script')
    for script in scripts:
        if 'preloadedItems' in script.getText():                
            regex = re.compile('var preloadedItems = (.*?);')
            preloadedItems = regex.search(script.getText())
            items = json.loads(preloadedItems.groups()[0])
            for item in items:
                if item['stock'] != []:
                    link = 'http://www.oneblockdown.it/en/footwear-lifestyle/' + item['stock'][0]['itemId']
                    printToSheet(item['alias'], link)

def offspring():
    print ('Offspring...')
    response = session.get('http://www.offspring.co.uk/view/search?search=' + query)
    soup = bs(response.text, 'html.parser')
    items = soup.findAll('div', {'class' : 'productList_item'})
    for item in items:
        productCode = item.find('div', {'class' : 'containerTitle productList_quickbuy'})
        payload = {
            'productCode' : productCode['data-productcode'],
            'og' : 'false'
        }
        response = session.post('http://www.offspring.co.uk/view/basket/viewSizes', data=payload)
        responseJson = json.loads(response.text)
        if responseJson['variantOptions']['hasStock']:
            printToSheet(responseJson['shortDescription'] + ' ' + responseJson['shoeColour']['name'], 'http://www.offspring.co.uk' + item.find('a')['href'])              

def titolo():
    print ('Titolo...')
    response = session.get('https://en.titoloshop.com/catalogsearch/result/?q=' + query)
    soup = bs(response.text, 'html.parser')
    items = soup.findAll('li', {'class' : 'item'})
    for item in items:
        if item.find('p') is None or 'out-of-stock' not in item.find('p').attrs['class']:
            printToSheet(item.find('span', {'class' : 'name'}).getText(), item.find('a')['href'])

def solebox():
    print ('Solebox...')
    response = session.get('https://www.solebox.com/catalogsearch/result/?q=' + query)
    soup = bs(response.text, 'html.parser')
    items = soup.findAll('li', {'class' : 'product-grid-item'})
    for item in items:
        if query in item.find('h2').getText() and item.find('div', {'class' : 'value'}) is None:
            printToSheet(item.find('a')['title'], item.find('a')['href'])

def endclothing():
    print ('end Clothing...')
    response = session.get('http://www.endclothing.com/gb/catalogsearch/result/?q=' + query)
    soup = bs(response.text, 'html.parser')
    print (soup)
    items = soup.findAll('div', {'class' : 'thumbnail item'})
    print(items)
    for item in items:
        response = session.get(item['href'])
        soup = bs(response.text, 'html.parser')
        holder = soup.find('div', {'class' : 'add-to-holder'})
        print(holder)
        if holder is None:
            description = soup.find('div', {'class' : 'product-shop product-description'})
            printToSheet(description.find('h1').getText() + ' ' + description.find('h3').getText(), item['href'])

def jdsports():
    print ('JDSports...')
    response = session.get('http://www.jdsports.co.uk/search/' + query + '/')
    soup = bs(response.text, 'html.parser')
    items = soup.findAll('li', {'class' : 'listItem'})
    for item in items:
        link = 'http://www.jdsports.co.uk' + item.find('a')['href']
        response = session.get(link + 'quickview')
        soup = bs(response.text, 'html.parser')
        availability = soup.find('link', {'itemprop' : 'availability'})
        if availability is not None and availability['href'] == 'http://schema.org/InStock':
            regex = re.compile('\/product\/(.*?)\/')
            match = regex.search(link).groups()[0].replace('-',' ').title()
            printToSheet(match, link)

def zolando():
    print ('Zolando...')
    response = session.get('https://www.zalando.co.uk/catalog/?q=' + query + '&qf=1')
    soup = bs(response.text, 'html.parser')
    items = soup.findAll('li', {'class' : 'catalogArticlesList_item'})
    for item in items:
        if item['data-s'] != '':
            printToSheet(item.find('div', {'class' : 'catalogArticlesList_articleName'}).getText().replace(' - Trainers -', ''), 'https://www.zalando.co.uk' + item.find('a')['href'])

def bluetomato():
    print ('Blue Tomato...')
    response = session.get('https://www.blue-tomato.com/en-GB/page/adidas-originals-' + query + '/')
    soup = bs(response.text, 'html.parser')
    items = soup.findAll('li', {'class' : 'productcell'})
    for item in items:
        link = 'https://www.blue-tomato.com' + item['data-href']
        response = session.get(link)
        soup = bs(response.text, 'html.parser')
        availability = soup.find('li', {'class' : 'active'})
        if availability is not None:
            printToSheet(item.find('p').getText().title(), link)

def caliroots():
    print ('Caliroots...')
    response = session.get('https://caliroots.com/search/searchbytext?key=' + query)
    soup = bs(response.text, 'html.parser')
    items = soup.findAll('li', {'class' : 'product'})
    for item in items:
        availability = soup.find('div', {'class' : 'sold-out'})
        if availability is None:
            printToSheet(item.find('p', {'class' : 'name'}).getText(), 'https://caliroots.com' + item.find('a')['href'])

def eastbay():
    print ('Eastbay...')
    response = session.get('http://www.eastbay.com/Shoes/_-_/N-ne/keyword-' + query + '?cm_REF=Shoes&Nr=AND%28P_RecordType%3AProduct%29')
    soup = bs(response.text, 'html.parser')
    items = soup.findAll('li')
    for item in items:
        if item.has_attr('data-sku'):
            response = session.get('http://www.eastbay.com/search/json.cfm?Rpp=1&Ntt=' + item['data-sku'])
            loadedJSON = json.loads(response.text)['RECORDS']
            if len(loadedJSON) > 0 and loadedJSON[0]['PROPERTIES']['P_IsSaleable'] == 'Y':
                printToSheet(item.find('span', {'class' : 'product_title'}).getText() + ' ' + str(loadedJSON[0]['DIMENSIONS']['Color']).replace('[','').replace(']','').replace("'",'').replace(', ','/'), item.find('a')['href'])

def nakedcph():
    print ('Naked CPH...')
    response = session.get('http://www.nakedcph.com/catalog?search=' + query)
    soup = bs(response.text, 'html.parser')
    items_list = soup.find('ul', {'class' : 'list-commodity list-commodity-grid'})
    items = items_list.findAll('li')
    for item in items:
        response = session.get(item.find('a')['href'])
        soup = bs(response.text, 'html.parser')
        availability = soup.find('div', {'id' : 'commodity-show-outofstock'})
        if availability is None:
            printToSheet(item.find('span', {'class' : 'list-commodity-title'}).getText(), item.find('a')['href'])

def snipes():
    print ('Snipes...')
    response = session.get('https://www.snipes.com/search.html?q=' + query + '&submit=Finden')
    soup = bs(response.text, 'html.parser')
    items = soup.findAll('dl', {'class' : 'm_product_thumb'})
    for item in items:
        pattern = re.compile('(.*?);jsessionid')
        match = pattern.search(item.findAll('a')[1]['href'])
        if match is None:
            pattern = re.compile('(.*?)\?r')
            match = pattern.search(item.findAll('a')[1]['href'])
        printToSheet(''.join(item.findAll('a')[1].getText().split()), 'https://www.snipes.com' + match.groups()[0])

def asphaltgold():
    print ('Asphalt Gold...')
    response = session.get('https://asphaltgold.de/de/catalogsearch/result/?q=' + query)
    soup = bs(response.text, 'html.parser')
    items = soup.findAll('section', {'class' : 'item'})
    for item in items:
        response = session.get(item.findAll('a')[1]['href'])
        soup = bs(response.text, 'html.parser')
        availability = soup.find('button', {'class' : 'btn-cart'})
        countdown = soup.find('div', {'id' : 'productrelease_countdown'})
        if not countdown is None or not availability is None or not 'Derzeit nicht' in availability.getText():
            printToSheet(item.findAll('a')[1].getText(), item.find('a')['href'])

def baskets():
    print ('Baskets...')
    response = session.get('http://www.baskets-store.com/catalogsearch/result/?q=' + query)
    soup = bs(response.text, 'html.parser')
    items = soup.findAll('div', {'class' : 'item'})
    for item in items:
        options = soup.find('ul', {'class' : 'option'})
        availability = soup.findAll('li', {'class' : 'option'})
        is_avail = False
        for option in availability:
            if not 'disabled' in option.attrs['class']:
                is_avail = True
                
        if is_avail == True:
            printToSheet(item.find('a')['title'], item.find('a')['href'])

def bertola():
    print ('Bertola...')
    response = session.get('http://www.bertolashop.com/storeonline/gb/ricerca?controller=search&orderby=position&orderway=desc&search_query=' + query + '&submit_search=')
    soup = bs(response.text, 'html.parser')
    items = soup.findAll('li', {'class' : 'ajax_block_product'})
    for item in items:
        availability = item.find('span', {'class' : 'available-dif'})
        if 'Product available' in availability.getText():
            printToSheet(item.find('a')['title'], item.find('a')['href'])

def asos():
    print ('ASOS...')
    response = session.get('http://www.asos.com/search/' + query + '?q=' + query)
    soup = bs(response.text, 'html.parser')
    item = soup.find('a', {'class' : 'add-to-bag'})
    if not item is None:
        printToSheet(soup.find('title').getText(), soup.find('link', {'rel' : 'alternate'})['href'])


def printToSheet(title, link):
    print (link)

session = requests.session()

sites = [asos, bertola, baskets, asphaltgold, einhalb, overkill, sns,
         oneblockdown, offspring, titolo, solebox, jdsports, zolando,
         bluetomato, caliroots, eastbay, snipes]
while True:
    for x in range(0, len(sites)):
        try:
            sites[x]()
        except Exception:
            print ('ERROR')
            pass

    print ('')
    time.sleep(60)
