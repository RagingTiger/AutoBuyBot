import requests
import urllib
import json
from bs4 import BeautifulSoup as bs

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
pid = "B27136"
url = "http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct?layer=Add%20To%20Bag%20overlay&pid=" + pid + "_650&Quantity=1&masterPid=" + pid + "aq2659add-to-cart-button="
session = requests.session()
response = session.get(url, headers=headers)
soup = bs(response.text, "html.parser")
print(json.loads(urllib.parse.unquote(soup.find("div", {"class":"hidden"}).getText())))