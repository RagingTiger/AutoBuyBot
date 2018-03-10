import requests
import re
import json
from bs4 import BeautifulSoup as bs
from getconf import * 
def getIds():
    global product_id
    global size_id
    for script in scripts:
        if 'spConfig =' in script.getText():
            regex = re.compile(r'var spConfig = new Product.Config\((.*?)\);')
            match = regex.search(script.getText())
            spConfig = json.loads(match.groups()[0])
            for key in spConfig['attributes']: # Should only call once
                for product in spConfig['attributes'][key]['options']:
                    if product['label_uk'] == uk_size:
                        size_id = product['id']
                        product_id = spConfig['attributes'][key]['id']

def checkout():
    print ('placeholder')
    

uk_size = '8.5'
early_link = 'https://www.overkillshop.com/en/nike-roshe-tiempo-vi-qs-853535-001.html'
session = requests.session()
response = session.get(early_link)
soup = bs(response.text, 'html.parser')
form = soup.find('form', {'id' : 'product_addtocart_form'})
scripts = soup.findAll('script')
product_id = ''
size_id = ''
getIds()

payload = {
    'product' : form.find('input', {'name' : 'product'})['value'],
    'related_product' : form.find('input', {'name' : 'related_product'})['value'],
    'super_attribute[' + product_id + ']' : size_id,
    'qty' : '1',
    'gpc_add' : '1'
}

response = session.post(form['action'], data=payload)
regex = re.compile(r'\\"(\d+)' + re.escape(r'\":{\"code\":\"' + shipping_state_abbrv + r'\"'))
match = regex.search(response.text)
region_id = match.groups()[0]
response = session.get('https://www.overkillshop.com/en/checkout/onepage/')
soup = bs(response.text, 'html.parser')
form_key = soup.find('input', {'name' : 'form_key'})['value']

payload = {
    'method' : 'guest'
}

response = session.post('https://www.overkillshop.com/en/checkout/onepage/saveMethod/', data=payload)

payload = {
    'billing[address_id]' : '',
    'billing[firstname]' : first_name,
    'billing[lastname]' : last_name,
    'billing[company]' : '',
    'billing[street][]' : shipping_address_1 + ', ' + shipping_apt_suite,
    'billing[postcode]' : shipping_zip,
    'billing[region_id]' : region_id,
    'billing[region]' : '',
    'billing[city]' : shipping_city,
    'billing[country_id]' : 'US',
    'billing[email]' : email,
    'billing[telephone]' : phone_number,
    'billing[fax]' : phone_number,
    'billing[customer_password]' : '',
    'billing[confirm_password]' : '',
    'billing[save_in_address_book]' : '1',
    'billing[use_for_shipping]' : '1'
}

response = session.post('https://www.overkillshop.com/en/checkout/onepage/saveBilling/', data=payload)

payload = {
    'shipping_method' : 'owebiashipping1_international'
}

response = session.post('https://www.overkillshop.com/en/checkout/onepage/saveShippingMethod/', data=payload)


payload = {
    'payment[method]' : 'paypal_standard',
    'agreement[1]' : '1',
    'agreement[2]' : '1'
}

response = session.post('https://www.overkillshop.com/en/checkout/onepage/saveOrder/form_key/' + form_key + '/', data=payload)

response = session.get('https://www.overkillshop.com/en/paypal/standard/redirect/')

# Paypal checkout (should we standardize this?)
soup = bs(response.text, 'html.parser')
form = soup.find('form')
inputs = form.findAll('input')
payload = {}
for input_tag in inputs:
    if not 'Click here if you are not' in input_tag['value']:
        payload[input_tag['name']] = input_tag['value']

response = session.post('https://www.paypal.com/cgi-bin/webscr', data=payload)
print (response.text)
