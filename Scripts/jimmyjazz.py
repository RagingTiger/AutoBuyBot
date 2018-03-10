#!/usr/bin/env python3
import requests
import timeit
from bs4 import BeautifulSoup as bs
import time
from getconf import *

# User input
use_early_link = True
early_link = ''
use_keyword = False
shoe_size = ''


# Functions
def add_to_cart(early_link, shoe_size):
	print('Adding to Cart')
	response = session.get(early_link, headers=headers)
	soup = bs(response.text, 'html.parser')

	available_sizes = []
	size_ids = []
	size_box = soup.find_all('a', {'class': 'box'})

	for a in size_box:
		for sizes in a.stripped_strings:
			available_sizes.append(sizes)
	for ids in size_box:
		size_ids.append(ids['id'][-8:])

	if shoe_size in available_sizes:
		pos = available_sizes.index(shoe_size)
		id = size_ids[pos]
		response = session.get('http://www.jimmyjazz.com/cart-request/cart/add/' + id + '/1', headers=headers)
		time.sleep(.5)
		return 1
	else:
		return 0


def checkout():
	print('Checking Out')
	response = session.get('http://www.jimmyjazz.com/cart', headers=headers)

	response = session.get('https://www.jimmyjazz.com/cart/checkout', headers=headers)
	soup = bs(response.text, 'html.parser')
	form_id = soup.find('input', {'name': 'form_build_id'})['id']

	payload = {
		'billing_address1': billing_address_1,
		'billing_address2': billing_address_2,
		'billing_city': billing_city,
		'billing_country': billing_country,
		'billing_email': email,
		'billing_email_confirm': email,
		'billing_first_name': first_name,
		'billing_last_name': last_name,
		'billing_phone': phone_number,
		'billing_state': billing_state_abbrv,
		'billing_zip': billing_zip,
		'cc_cvv': card_cvv,
		'cc_exp_month': card_exp_month,
		'cc_exp_year': card_exp_year,
		'cc_number': card_number,
		'cc_type': card_type,
		'email_opt_in': '1',
		'form_build_id': form_id,
		'form_id': 'cart_checkout_form',
		'gc_num': '',
		'shipping_address1': shipping_address_1,
		'shipping_address2': shipping_address_2,
		'shipping_city': shipping_city,
		'shipping_first_name': first_name,
		'shipping_last_name': last_name,
		'shipping_method': '0',
		'shipping_state': shipping_state,
		'shipping_zip': shipping_zip
	}

	response = session.post('https://www.jimmyjazz.com/cart/checkout', data=payload, headers=headers)

	response = session.get('https://www.jimmyjazz.com/cart/confirm')
	soup = bs(response.text, 'html.parser')
	form_id = soup.find('input', {'name': 'form_build_id'})['id']

	payload = {
		'form_build_id': form_id,
		'form_id': 'cart_confirm_form'
	}
	response = session.post('https://www.jimmyjazz.com/cart/confirm', data=payload, headers=headers)
	try:
		soup = bs(response.text, 'html.parser')
		error = soup.find('div', {'class': 'messages error'}).text
		print(error)
	except:
		print('Checkout was successful!')


# Main
start = timeit.default_timer()
session = requests.Session()
headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

if use_early_link:
	if add_to_cart(early_link, shoe_size):
		checkout()
	else:
		print('Size ' + shoe_size + ' not available')

stop = timeit.default_timer()
print(stop - start)
