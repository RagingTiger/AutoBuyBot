from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup as bs
import requests
import sys
import re
from getconf import *
from atclibs import *

# TO DO: scrape for early links

# Constants
base_url = 'http://www.supremenewyork.com'

# Inputs
keywords_category = ['accessories']  # Demo stuff, feel free to change
keywords_model = ['crew', 'socks']
keywords_style = ['white']

# if there is no size, such as for socks, the size is OS
size = 'OS'

use_early_link = False

early_link = ''


# early_link = 'http://www.supremenewyork.com/shop/jackets/nzpacvjtk' #sold out
# early_link = 'http://www.supremenewyork.com/shop/shirts/r1k32vjf4/sblz8csj2' # mult sizes
# early_link = 'http://www.supremenewyork.com/shop/accessories/kcgevis8r/xiot9byq4' #one size


# Functions
def product_page(url):
	print('Finding matching products...', end='')
	session = requests.Session()
	session.headers.update({
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
		              'Chrome/52.0.2743.116 Safari/537.36',
		'X-XHR-Referer': 'http://www.supremenewyork.com/shop/all',
		'Referer': 'http://www.supremenewyork.com/shop/all/bags',
		'Accept': 'text/html, application/xhtml+xml, application/xml',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
		'DNT': '1'
	})
	
	response = session.get(base_url + url)
	soup = bs(response.text, 'html.parser')
	
	h1 = soup.find('h1', {'itemprop': 'name'})
	
	p = soup.find('p', {'itemprop': 'model'})
	
	match = []
	
	if h1 is not None and p is not None:
		model = h1.string
		style = p.string
		
		for keyword in keywords_model:
			if keyword.title() in model:
				match.append(1)
			else:
				match.append(0)
		
		# add to cart
		if 0 not in match:
			match = []
			for keyword in keywords_style:
				if keyword.title() in style:
					match.append(1)
				else:
					match.append(0)
			if 0 not in match:
				print('FOUND: ' + model + ' at ' + base_url + url)
				add_to_cart(soup, base_url + url)
			else:
				print('Sorry, couldnt find {} in {}'.format(model, style))
		else:
			print('Sorry couldnt find what you are looking for')


def add_to_cart(soup, url):
	product_name = soup.find('h1', {'itemprop': 'name'}).string
	print('Adding {} to cart...'.format(product_name))
	session = requests.Session()
	session.headers.update({
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
		              'Chrome/52.0.2743.116 Safari/537.36',
		'X-XHR-Referer': 'http://www.supremenewyork.com/shop/all',
		'Referer': 'http://www.supremenewyork.com/shop/all/',
		'Accept': 'text/html, application/xhtml+xml, application/xml',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
		'DNT': '1'
	})
	form = soup.find('form', {'action': re.compile('(?<=/shop/)(.*)(?=/add)')})
	csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']
	
	# find size
	sold_out = soup.find('fieldset', {'id': 'add-remove-buttons'}).find('b')
	if sold_out is not None:
		sys.exit('Sorry, product is sold out!')
	else:
		if size.upper() == 'OS':
			size_value = form.find('input', {'name': 'size'})['value']
		else:
			try:
				size_value = soup.find('option', string=size.title())['value']
			except:
				sys.exit('Sorry, {} is sold out!'.format(size))
	
	if form is not None:
		payload = {
			'utf8': '✓',
			'authenticity_token': form.find('input', {'name': 'authenticity_token'})['value'],
			'size': size_value,
			'commit': 'add to cart'
		}
		headers = {
			'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
			'Origin': 'http://www.supremenewyork.com',
			'X-Requested-With': 'XMLHttpRequest',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Referer': url,
			'X-XHR-Referer': None,
			'X-CSRF-Token': csrf_token,
			'Accept-Encoding': 'gzip, deflate'
		}
		
		session.post(base_url + form['action'], data=payload, headers=headers)
		checkout(session)
	else:
		sys.exit('Sorry, product is sold out!')


def checkout(session):
	print('Filling out checkout info...')
	response = session.get('https://www.supremenewyork.com/checkout')
	soup = bs(response.text, 'html.parser')
	form = soup.find('form', {'action': '/checkout'})
	
	csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']
	headers = {
		'Accept': 'text/html, */*; q=0.01',
		'X-CSRF-Token': csrf_token,
		'X-Requested-With': 'XMLHttpRequest',
		'Referer': 'https://www.supremenewyork.com/checkout',
		'Accept-Encoding': 'gzip, deflate, sdch, br'
	}
	
	country_abbrv = shipping_country_abbrv
	if country_abbrv == 'US':
		country_abbrv = 'USA'
	
	if card_type.lower() in ['mastercard', 'master card', 'master']:
		card_ = 'master'
	elif card_type.lower() == 'visa':
		card_ = 'visa'
	elif card_type.lower() == 'american express':
		card_ = 'american_express'
	else:
		sys.exit('You must be using a master, visa, or american express card')
	
	payload = {
			'utf8': '✓',
			'authenticity_token': form.find('input', {'name': 'authenticity_token'})['value'],
			'order[billing_name]': first_name + ' ' + last_name,
			'order[email]': email,
			'order[tel]': format_phone(phone_number),
			'order[billing_address]': shipping_address_1,
			'order[billing_address_2]': shipping_apt_suite,
			'order[billing_zip]': shipping_zip,
			'order[billing_city]': shipping_city,
			'order[billing_state]': shipping_state,
			'order[billing_country]': country_abbrv,
			'same_as_billing_address': '1',
			# 'store_address': '0',
			'store_credit_id': '',
			'credit_card[type]': card_,
			'credit_card[cnb]': format_card(card_number),
			'credit_card[month]': card_exp_month,
			'credit_card[year]': card_exp_year,
			'credit_card[vval]': card_cvv,
			'order[terms]': '1',
			'hpcvv': '',
			'cnt': '2'
		}
	
	response = session.get('https://www.supremenewyork.com/checkout.js', data=payload, headers=headers)
	
	payload = {
			'utf8': '✓',
			'authenticity_token': form.find('input', {'name': 'authenticity_token'})['value'],
			'order[billing_name]': first_name + ' ' + last_name,
			'order[email]': email,
			'order[tel]': format_phone(phone_number),
			'order[billing_address]': shipping_address_1,
			'order[billing_address_2]': shipping_apt_suite,
			'order[billing_zip]': shipping_zip,
			'order[billing_city]': shipping_city,
			'order[billing_state]': shipping_state_abbrv,
			'order[billing_country]': country_abbrv,
			'same_as_billing_address': '1',
			'store_credit_id': '',
			'store_address': '1',
			'credit_card[type]': card_type,
			'credit_card[cnb]': format_card(card_number),
			'credit_card[month]': card_exp_month,
			'credit_card[year]': card_exp_year,
			'credit_card[vval]': card_cvv,
			'order[terms]': '1',
			'hpcvv': ''
		}
	
	headers = {
		'Origin': 'https://www.supremenewyork.com',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Referer': 'https://www.supremenewyork.com/checkout',
		'Accept-Encoding': 'gzip, deflate, br'
	}
	
	response = session.post('https://www.supremenewyork.com/checkout', data=payload, headers=headers)
	if 'Your order has been submitted' in response.text:
		print('Checkout was successful, check for a confirmation email!')
	else:
		try:
			soup = bs(response.text, 'html.parser')
			error_msg = soup.find('div', {'class': 'errors'})
			if error_msg is None:
				print(soup.find('p').text)
			else:
				print('\n' + 'ERROR: ' + error_msg)
		except:
			print('Checkout failed')

# Main
tick()

session1 = requests.Session()
session1.headers.update({
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
	              'Chrome/52.0.2743.116 Safari/537.36',
	'Upgrade-Insecure-Requests': '1',
	'DNT': '1',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate, sdch',
	'Accept-Language': 'en-US,en;q=0.8,da;q=0.6'
})

if use_early_link:
	try:
		response1 = session1.get(early_link)
		soup = bs(response1.text, 'html.parser')
	except:
		sys.exit('Unable to connect to site...')
	add_to_cart(soup, early_link)
else:
	try:
		url = base_url + '/shop/all/' + keywords_category[0] + '/'
		response1 = session1.get(url)
	except:
		sys.exit('Unable to connect to site...')
	soup1 = bs(response1.text, 'html.parser')
	links1 = soup1.find_all('a', href=True)
	links_by_keyword1 = []
	for link in links1:
		for keyword in keywords_category:
			product_link = link['href']
			if keyword in product_link and 'all' not in product_link:
				if product_link not in links_by_keyword1:
					links_by_keyword1.append(link['href'])
	pool1 = ThreadPool(len(links_by_keyword1))
	result1 = pool1.map(product_page, links_by_keyword1)

tock()  # runtime
