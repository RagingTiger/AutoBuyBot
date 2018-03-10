#!/usr/bin/env python3
# This is the checkout process on NakedCPH for an HSBC card with Verified by Visa
# Unfortunately, this is will likely need to be done on a case by case basis for
# different cart types.

import requests
import re
import time
import timeit
from bs4 import BeautifulSoup as bs
from getconf import *

def checkout(first, last):
    i = first
    while first <= last:
        print ('Trying: ' + str(first))
        password = '' # Your Verified by Visa password
        soup = None
        while soup is None:
            try:
                print ('Adding to cart')
                payload = {
                    'action' : 'add',
                    'item_pid' : first,
                    'ajax' : '1'
                }
                response = session.post('http://www.nakedcph.com/cart', data=payload)
                soup = bs(response.text, 'html.parser')
            except Exception:
                pass
        print (soup)
        if soup.find('a').getText() != 'Cart (0)':
            none = None
            while none is None:
                try:
                    payload = {
                        'formid' : 'details.anonymous',
                        'email' : email,
                        'email_repeat' : email,
                        'first_name' : first_name,
                        'surname' : last_name,
                        'address' : shipping_address_1,
                        'address2' : shipping_apt_suite,
                        'zip' : shipping_zip,
                        'city' : shipping_city,
                        'state' : shipping_state,
                        'country' : shipping_country,
                        'phone' : phone_number
                    }
                    response = session.post('http://www.nakedcph.com/checkout/details', data=payload)
                    none = 1
                except Exception:
                    pass
                
            none = None
            while none is None:
                try:
                    payoad = {
                        'mode' : 'user',
                        'shipping' : '6', # Need to figure out which countries these correspond to
                        'payment' : 'quickpay10secure'
                    }
                    response = session.post('http://www.nakedcph.com/checkout/handling', data=payload)
                    none = 1
                except Exception:
                    pass

            none = None
            while none is None:
                try:
                    payload = {
                        'confirmed' : 'on'
                    }
                    response = session.post('http://www.nakedcph.com/checkout/confirm', data=payload)
                    soup = bs(response.text, 'html.parser')
                    none = 1
                except Exception:
                    pass

            payload = {
                'agreement_id' : soup.find('input', {'name' : 'agreement_id'})['value'],
                'amount' : soup.find('input', {'name' : 'amount'})['value'],
                'autocapture' : soup.find('input', {'name' : 'autocapture'})['value'],
                'callbackurl' : soup.find('input', {'name' : 'callbackurl'})['value'],
                'cancelurl' : soup.find('input', {'name' : 'cancelurl'})['value'],
                'continueurl' : soup.find('input', {'name' : 'continueurl'})['value'],
                'currency' : soup.find('input', {'name' : 'currency'})['value'],
                'language' : soup.find('input', {'name' : 'language'})['value'],
                'merchant_id' : soup.find('input', {'name' : 'merchant_id'})['value'],
                'order_id' : soup.find('input', {'name' : 'order_id'})['value'],
                'payment_methods' : soup.find('input', {'name' : 'payment_methods'})['value'],
                'version' : soup.find('input', {'name' : 'version'})['value'],
                'checksum' : soup.find('input', {'name' : 'checksum'})['value']
            }
            response = session.post('https://payment.quickpay.net/', data=payload)
            soup = bs(response.text, 'html.parser')

            payload = {
                'card_number' : card_number,
                'month' : card_exp_month,
                'year' : card_exp_year,
                'cvd' : card_cvv,
                'session_id' : soup.find('input', {'name' : 'session_id'})['value']
            }

	    # The 3d secure process should always be relatively similar for every card
            response = session.post('https://payment.quickpay.net/prepare_3d_secure', data=payload)
            soup = bs(response.text, 'html.parser')

            MD = soup.find('input', {'name' : 'MD'})['value']
            PaReq = soup.find('input', {'name' : 'PaReq'})['value']
            TermUrl = soup.find('input', {'name' : 'TermUrl'})['value']

            payload = {
                'MD' : MD,
                'PaReq' : PaReq,
                'TermUrl' : TermUrl
            }
            secure5link = soup.find('form', {'id' : 'secure_3d_form'})['action']
            response = session.post(secure5link, data=payload)
            soup = bs(response.text, 'html.parser')

            payload = {
                'executionTime' : '0',
                'PaReq' : PaReq,
                'MD' : MD,
                'TermUrl' : TermUrl,
                'deviceSignature' : '',
                'DeviceID' : '',
                'CallerID' : '',
                'IpAddress' : '',
                'cancelHit' : '',
                'CookieType' : '2',
                'AcsCookie' : '!@#Dummy#@!',
                'dnaError' : '',
                'mesc' : '',
                'mescIterationCount' : '0',
                'desc' : '',
                'isDNADone' : 'false',
                'ABSlog' : 'DSP;FlashLoadTime:639;DEVICEID;'
            }
            response = session.post(secure5link, data=payload)
            soup = bs(response.text, 'html.parser')
            pattern = re.compile('getPartialSlotDefinition\("(.*?)","(.*?)","(.*?)"\)')
            matches = pattern.findall(response.text)
            slotData = []
            if len(matches) > 0:
                for match in matches:
                    if len(match) > 0:
                        slotData = match

            if not slotData == []:
                payload = {
                    'slotpin1' : password[int(slotData[0])-1],
                    'slotpin2' : password[int(slotData[1])-1],
                    'slotpin3' : password[int(slotData[2])-1],
                    'pin' : '0',
                    'submitted' : '1',
                    'authType' : 'Visa Password',
                    'cancelHit' : '0',
                    'forgotPassword' : '0',
                    'cardHolder' : name_on_card,
                    'authDefaultSelect' : 'Visa Password',
                    'AuthFallBack' : '',
                    'Phase' : 'passwd',
                    'pan' : 'XXXX XXXX XXXX ' + card_number[-4:],
                    'tryIndex' : '1',
                    'PaReq' : PaReq,
                    'TermUrl' : TermUrl,
                    'MD' : MD,
                    'PTerms' : '',
                    'PDescription' : '',
                    'PConditions' : '',
                    'ARCOTC' : '',
                    'ARCOTR' : '',
                    'Locale' : 'en_GB_hsbcvisadebit/',
                    'VSDCInput' : soup.find('input', {'name' : 'VSDCInput'})['value'],
                    'VSDCData' : '',
                    'ChipPluginName' : '',
                    'ChipPluginVersion' : '', # You need to check these values for your own card
                    'ChipPluginPresent' : 'TRUE', # Do you have a chip card?
                    'eAccessPresent' : 'FALSE', 
                    'eAccessRequired' : 'FALSE',
                    'ChipSecret' : '',
                    'AcsCookie' : soup.find('input', {'name' : 'AcsCookie'})['value'],
                    'AcsCondData' : '1301',
                    'ABSlog' : 'GPP;INIT',
                    'DeviceID' : soup.find('input', {'name' : 'DeviceID'})['value'],
                    'CookieType' : '2'
                }
                TermUrl = soup.find('input', {'name' : 'TermUrl'})['value']
                response = session.post('https://secure5.arcot.com/acspage/cap.cgi', data=payload)
                soup = bs(response.text, 'html.parser')

                payload = {
                    'PaRes' : soup.find('input', {'name' : 'PaRes'})['value'],
                    'MD' : MD,
                    'PaReq' : PaReq
                }
                response = session.post(TermUrl, data=payload)
                soup = bs(response.text, 'html.parser')

                response = session.get('https://payment.quickpay.net' + soup.find('a')['href'])
                soup = bs(response.text, 'html.parser')
                p = soup.find('p')
                while not p is None and p.getText() == 'Please wait while we process your payment...':
                    response = session.get('https://payment.quickpay.net' + soup.find('a')['href'])
                    soup = bs(response.text, 'html.parser')
                    return
                    
                print ('ORDER PLACED')
            else:
                print ('Verification was not needed')

        first = first + 1
        if first == last:
            first = i

session = requests.session()
first1 = 12345
last1 = 67890
checkout(first1, last1) # Only if you want a range of product IDS
