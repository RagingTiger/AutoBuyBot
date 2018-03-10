#!/usr/bin/env python3
import requests
import timeit
from bs4 import BeautifulSoup as bs
from getconf import *

base_url = "http://www.sneakersnstuff.com/en/"

#User Vars
early_link = 'product/23807/new-balance-epic-tr-blueberry'
shoe_size = '8'

def checkout ():
    #TODO: SNS uses ayden for payment processing
    #Calls a URL that looks like so:
    '''
    https://live.adyen.com/hpp/pay.shtml?
    paymentAmount=1800
    &currencyCode=USD
    &skinCode=f4J2tsmj
    &merchantReference=3076306
    &shopperReference=2213612
    &shopperEmail=
    &merchantAccount=SneakersnstuffCOM
    &sessionValidity=2016-06-18T17%3a09%3a12Z
    &shipBeforeDate=2016-06-25T16%3a59%3a12Z
    &allowedMethods=card
    &resURL=http%3a%2f%2fwww.sneakersnstuff.com%2fadyen%2freturn
    &countryCode=US
    &merchantSig=Bk2R0n7GdFH9t911QknLhsO%2b53Y%3d
    &shopperLocale=en
    &orderData=H4sIAAAAAAAEAK2QsQrCMBCGd8F3CMFVtJtDzVAXF6c8wTUX9DBNzuQ69O1tpYJDHQS374f%2fjo%2b%2fFmiDVy5AKUedMvq8JfFd0Wa9UqqWNuHwwinkmSbG9xH64jKxUIranIF5UDa5e1FNc1KWwfk52w5C2F08Ut%2fVO8GlZ48eopAM2lTfKpzJeW02h4%2fCiPkHSysQETIqeyNmitc%2f6FT7JZ8R5gVHmqY2T53OD0dyAQAA
    &billingAddress.street= Line 1 and 2
    &billingAddress.city=
    &billingAddress.postalCode=
    &billingAddress.stateOrProvince=
    &billingAddress.country=US
    :return:
    '''
    return

def add_to_cart(url, size):
    size_code = ''
    session = requests.Session()
    response = session.get(base_url + url)

    soup = bs(response.text, 'html.parser')
    form = soup.find('form', { 'id': 'add-to-cart-form'})
    size_divs = form.find_all('div', { 'class':  'size-button property available'})
    print ('Sizes available: {}'.format(len(size_divs)))
    anti_token = form.find('input', {'name': '_AntiCsrfToken'})['value']

    for div in size_divs:
        #TODO: Perhaps there is a better way for size systems?
        if (div.text.strip().replace('US ', '') == size):
            print ('Found')
            size_code = div['data-productid']
            break
    if not size_code:
        print('Could not find size!')
        return

    payload = {
        '_AntiCsrfToken': anti_token,
        'partial': 'cart-summary',
        'id': size_code
    }

    response = session.post(base_url + "cart/add", data=payload)
    print (response)
#    checkout()


# Main
start = timeit.default_timer()
if early_link:
    add_to_cart(early_link, shoe_size)
# else
#TODO: keyword logic

stop = timeit.default_timer()
print ("Runtime: {}".format(stop - start))
