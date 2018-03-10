#!/usr/bin/env python3
import sys
import json

"""An interactive script for generating userinfo.json"""
if sys.version_info[0] == 2:
	input = raw_input

configuration = {}

print("You may simply press <enter> without inputting anything to any of")
print("these questions, but this may produce strange errors.")

configuration["first_name"] = input("Please enter your first name: ")
configuration["last_name"] = input("Please enter your last name: ")
configuration["phone_number"] = input("Please enter your phone number: ")
configuration["email"] = input("Please enter your email address: ")
configuration["shipping_address_1"] = input("Please enter the first line of your shipping address: ")
configuration["shipping_address_2"] = input(
	"Please enter the second line of your shipping address (hit <enter> if the second line is an apartment/suite number): ")
configuration["shipping_apt_suite"] = input("Please enter your apartment/suite number, if applicable: ")
configuration["shipping_city"] = input("Please enter your shipping city: ")
configuration["shipping_state"] = input("Please enter your shipping state (not abbreviated): ")
configuration["shipping_state_abbrv"] = input("Please enter your shipping state (abbreviated): ")
configuration["shipping_country"] = input("Please enter your shipping country (not abbreviated): ")
configuration["shipping_country_abbrv"] = input("Please enter your shipping country (abbreviated): ")
configuration["shipping_zip"] = input("Please enter your shipping zip/post code: ")

billing = input("Is your billing address different than the shipping address? [Y/N]: ").title()
if billing in ["Y", "Yes"]:
	configuration["billing_address_1"] = input("Please enter the first line of your billing address: ")
	configuration["billing_address_2"] = input(
		"Please enter the second line of your billing address (hit <enter> if the second line is an apartment/suite number): ")
	configuration["billing_apt_suite"] = input("Please enter your apartment/suite number, if applicable: ")
	configuration["billing_city"] = input("Please enter your billing city: ")
	configuration["billing_state"] = input("Please enter your billing state (not abbreviated): ")
	configuration["billing_state_abbrv"] = input("Please enter your billing state (abbreviated): ")
	configuration["billing_country"] = input("Please enter your billing country: ")
	configuration["billing_zip"] = input("Please enter your billing zip/post code: ")
else:
	configuration["billing_address_1"] = configuration["shipping_address_1"]
	configuration["billing_address_2"] = configuration["shipping_address_2"]
	configuration["billing_apt_suite"] = configuration["shipping_apt_suite"]
	configuration["billing_city"] = configuration["shipping_city"]
	configuration["billing_state"] = configuration["shipping_state"]
	configuration["billing_state_abbrv"] = configuration["shipping_state_abbrv"]
	configuration["billing_country"] = configuration["shipping_country"]
	configuration["billing_country_abbrv"] = configuration["shipping_country_abbrv"]
	configuration["billing_zip"] = configuration["shipping_zip"]

configuration["card_type"] = input("Please enter your credit card type (Visa, MasterCard, Amex...)? ")
print("")
print(
	"It is recommended that, if you are testing, you input a real card number but a fake CVV.  This way, checkout will proceed as normal so you can see what will occur, but nothing will be charged to your account.")
print("")
configuration["card_number"] = input("Please enter your credit card number: ")
configuration["card_cvv"] = input("Please enter the CVV for that credit card: ")
configuration["card_exp_year"] = input("Please enter your card expiration year: ")
configuration["card_exp_month"] = input("Please enter your card expiration month: ")
configuration["name_on_card"] = input("Please enter your name as it appears on this card: ")
print("Thank you! All done.")

with open("userinfo.json", "w") as conffile:
	json.dump(configuration, conffile, sort_keys=True, indent=4)
