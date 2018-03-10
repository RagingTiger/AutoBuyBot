#!/usr/bin/env python3
import requests
import re
import timeit
import json
from bs4 import BeautifulSoup as bs
from getconf import *

# User input
size = '6.5'
use_early_link = True
early_link = 'https://caliroots.com/adidas-originals-tubular-nova-primeknit-s74917/p/53784'

def checkout():  # USA checkout
    # TODO: Get rid of this by making a list of state codes
    response = session.get('https://caliroots.com/express/checkout/49')
    soup = bs(response.text, 'html.parser')
    scripts = soup.findAll('script')
    for script in scripts:
        if 'window.meta    = ' in script.getText():
            regex = re.compile('window\.meta    = ((.|\n)*?);')
            match = regex.search(script.getText())
            meta = json.loads(match.groups()[0])
            print (soup)

            print (meta)
            payload = {
                'ctx.COUNTRY' : 'GB',
                'meta' : {
                    'token' : meta.token,
                    'calc' : meta.calc,
                    'csci' : meta.csci,
                    'locale' : meta.locality,
                    'state' : 'ui_checkout_login',
                    'app_name' : 'hermesnodeweb'
                }
            }
            response = session.get('https://www.paypal.com/webapps/hermes/api/pxp/xo_aries_hermes_guest_throttle', data=payload)
            print (response.text)
# Main
start = timeit.default_timer()

session = requests.session()

if use_early_link:
    response = session.get(early_link)
    soup = bs(response.text, 'html.parser')

    options = soup.find_all('option')
    regexp = re.compile(size.replace('.', ','))
    product_id = ''

    for option in options:
        if regexp.search(option.getText()) is not None:
            product_id = option['value']
            continue

    payload = {
        'id' : product_id,
        'partial' : 'ajax-cart'
    }

    response = session.post('https://caliroots.com/cart/add', data=payload)
    soup = bs(response.text, 'html.parser')
    checkout()

stop = timeit.default_timer()
print (stop - start)
