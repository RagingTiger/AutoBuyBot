#!/usr/bin/env python3
import requests
import re
import timeit
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup as bs
from getconf import *

#User input
size = 'Medium'
use_early_link = True
early_link = 'http://shop-usa.palaceskateboards.com/products/reversible-thinsulate-green-gables-puritan-grey'
use_keyword = False
#TODO: Make the logic for keyword checkout

#Functions
def checkout():
    response = session.get('http://shop-usa.palaceskateboards.com/cart')
    soup = bs(response.text, 'html.parser')

    form = soup.find('form', {'action' : '/cart'})
    
    payload = {
       form.find('input', {'name' : re.compile('(?<=updates\[)(.*)(?=])')})['name'] : form.find('input', {'name' : re.compile('(?<=updates\[)(.*)(?=])')})['value'],
       'checkout' : 'Checkout',
       'note' : form.find('input', {'name' : 'note'})['value']
    }
    
    response = session.post('http://shop-usa.palaceskateboards.com/cart', data=payload)
    soup = bs(response.text, 'html.parser')

    form = soup.find('form', {'action' : re.compile('(?<=shop-usa.palaceskateboards.com)(.*)(?=/checkouts/)')})
    checkout_url = form['action'] # For later
    
    payload = {
        'utf8' : '✓',
        '_method' : 'patch',
        'authenticity_token' : form.find('input', {'name' : 'authenticity_token'})['value'],
        'previous_step' : 'contact_information',
        'step' : 'shipping_method',
        'checkout[email]' : email,
        'checkout[shipping_address][first_name]' : first_name,
        'checkout[shipping_address][last_name]' : last_name,
        'checkout[shipping_address][address1]' : shipping_address_1,
        'checkout[shipping_address][address2]' : shipping_apt_suite,
        'checkout[shipping_address][city]' : shipping_city,
        'checkout[shipping_address][country]' : 'United States',
        'checkout[shipping_address][province]' : '',
        'checkout[shipping_address][province]' : '',
        'checkout[shipping_address][province]' : shipping_state,
        'checkout[shipping_address][zip]' : shipping_zip,
        'checkout[shipping_address][phone]' :  phone_number,
        'remember_me' : 'false',
        'button' : '',
        'checkout[client_details][browser_width]' : '123',
        'checkout[client_details][browser_height]' : '456',
        'checkout[client_details][javascript_enabled]' : '1'
    }

    response = session.post(form['action'], data=payload)
    soup = bs(response.text, 'html.parser')
    
    form = soup.find('form', {'action' : re.compile('(?<=shop-usa.palaceskateboards.com)(.*)(?=/checkouts/)')})

    payload = {
        'utf8' : '✓',
        '_method' : 'patch',
        'authenticity_token' : form.find('input', {'name' : 'authenticity_token'})['value'],
        'previous_step' : 'shipping_method',
        'step' : 'payment_method',
        'checkout[shipping_rate][id]' : form.find('input', {'name' : 'checkout[shipping_rate][id]'})['value'],
        'button' : '',
        'checkout[client_details][browser_width]' : '123',
        'checkout[client_details][browser_height]' : '456',
        'checkout[client_details][javascript_enabled]' : '1'
    }

    response = session.post(form['action'], data=payload)
    soup = bs(response.text, 'html.parser')
    
    form = soup.find('form', {'data-payment-form' : re.compile('(?<=shop-usa.palaceskateboards.com)(.*)(?=/checkouts/)')})

    payload = {
        'utf8' : '✓',
        'authenticity_token' : form.find('input', {'name' : 'authenticity_token'})['value'],
        'previous_step' : 'payment_method',
        'step' : '',
        's' : '',
        'c' : form.find('input', {'name' : 'c'})['value'],
        'd' : form.find('input', {'name' : 'd'})['value'],
        'checkout[payment_gateway]' : form.find('input', {'name' : 'checkout[payment_gateway]'})['value'],
        'checkout[credit_card][number]' : card_number,
        'checkout[credit_card][name]' : first_name + ' ' + last_name,
        'checkout[credit_card][month]' : card_exp_month.strip('0'),
        'checkout[credit_card][year]' : card_exp_year,
        'expiry' : card_exp_month + ' / ' + card_exp_year[-2:],
        'checkout[credit_card][verification_value]' : card_cvv,
        'checkout[different_billing_address]' : 'false',
        'complete' : '1',
        'checkout[client_details][browser_width]' : '123',
        'checkout[client_details][browser_height]' : '456',
        'checkout[client_details][javascript_enabled]' : '1'
    }

    response = session.post(form['action'], data=payload)

    response = session.get(checkout_url)
    soup = bs(response.text, 'html.parser')
    print (soup) # So I think this works... I would need to check if it actually checks out the next time I want to buy palace...
    
#Main
start = timeit.default_timer()

session = requests.session()

if use_early_link:
    response = session.get(early_link)
    soup = bs(response.text, 'html.parser')
    
    size_codes = soup.find_all('option')
    size_code = ''
    for code in size_codes:
        if code.getText() == size:
            size_code = code['value']
            continue
        
    payload = {
        'id' : size_code,
        'button' : 'Add to Cart'
    }

    response = session.post('http://shop-usa.palaceskateboards.com/cart/add', data=payload)
    
    checkout()

stop = timeit.default_timer()
print(stop - start) # Get the runtime
