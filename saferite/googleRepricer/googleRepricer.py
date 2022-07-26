import numpy as np
from bs4 import BeautifulSoup
import json
import pandas as pd
import datetime as dt
import pymongo
from pprint import pprint
import pyautogui as ptg
import pyperclip
import mws
from pandas.io.json import json_normalize
import gspread_dataframe as gd
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import gspread as gs
from bcispapi import bcispapi
import time

bc = bcispapi()
db_client = pymongo.MongoClient('mongodb://jesfel:FelipeSuperSecretPassword*987@3.235.105.186:27017/')
google = db_client['Google_Analysis']['Repricer']
gskey = 'C:\\PY\\SL.json'
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(gskey, scope)
gsheet = 'https://docs.google.com/spreadsheets/d/17mq7VP_S6kLGDIUDB0sDplRBJdgb9p5-NPlzIYEONtQ/edit?usp=sharing'
gc = gs.authorize(credentials)
sh = gc.open_by_url(gsheet)
hoja =  sh.worksheet('Data')
data_after = gd.get_as_dataframe(hoja)
col2 = {'Sold by':["NO"], 'Details & special offers':["NO"], 'Item price':["NO"], 'Unnamed: 7':["NO"], 'Unnamed: 9':["NO"], 'Unnamed: 12':["NO"]}
col = ['Sold by', 'Details & special offers', 'Item price', 'Unnamed: 7', 'Unnamed: 9', 'Unnamed: 12']

def shopping_bot(shop_id):
	url = 'view-source:https://www.google.com/shopping/product/' + str(shop_id)

	ptg.hotkey("f6")
	time.sleep(0.1)
	ptg.typewrite(url, 0.010)
	ptg.hotkey("enter")

	time.sleep(2.5)
	ptg.hotkey("ctrlleft", "a")
	time.sleep(0.1)
	ptg.hotkey("ctrlleft", "c")
	time.sleep(0.15)
	ptg.hotkey("ctrlleft", "c")

	html = pyperclip.paste()
	soup = BeautifulSoup(html, 'lxml')
	page = soup.find("section",{"id":"online"})

	return page
def amazon_bot(ASIN):
	url = 'view-source:https://www.amazon.com/dp/' + str(ASIN)

	ptg.hotkey("f6")
	time.sleep(0.1)
	ptg.typewrite(url, 0.010)
	ptg.hotkey("enter")

	time.sleep(4.5)
	ptg.hotkey("ctrlleft", "a")
	time.sleep(0.1)
	ptg.hotkey("ctrlleft", "c")
	time.sleep(0.25)
	ptg.hotkey("ctrlleft", "c")
	time.sleep(0.25)
	ptg.hotkey("ctrlleft", "c")
	time.sleep(0.25)

	html2 = pyperclip.paste()
	soup2 = BeautifulSoup(html2, 'lxml')

	if soup2.find("div",{"id":"cerberus-data-metrics"}):
		page2 = soup2.find("div",{"id":"cerberus-data-metrics"})
		amazon_price = page2['data-asin-price']
	elif soup2.find("div",{"id":"soldByThirdParty"}):
		page2 = soup2.find("div",{"id":"soldByThirdParty"})
		amazon_price = page2.span.text.strip()
	elif soup2.find("div",{"id":"price"}):
		page2 = soup2.find("div",{"id":"price"})
		amazon_price = page2.span.text.strip()
	elif soup2.find("div",{"id":"olp-upd-new-freeshipping"}):
		page2 = soup2.find("div",{"id":"olp-upd-new-freeshipping"})
		amazon_price = page2.span.text.strip()
	else:
		pass

	if soup2.find("div",{"id":"merchant-info"}):
		page3 = soup2.find("div",{"id":"merchant-info"})
		amazon_vendor = page3.text.strip()
	else:
		amazon_vendor = "No info"

	return amazon_price,amazon_vendor
def find_arrival(string, keyword):
	x = string.find(keyword)
	if x >= 0:
		if keyword == 'Arrives':
			return string[x:x+25]
		if keyword == 'Show':
			return string[:x]
		else:
			return string[:x-2]
	else:
		if keyword == 'Arrives':
			return ""
		else:
			return string
def fix_data_repricer(page, shop_id, bc_id, amazon_price, amazon_vendor):
	table = page.find("table")
	final_table = pd.read_html(str(table))
	final_table = final_table[0]
	# final_table = final_table.rename(columns={'Unnamed: 7': 'Shipping cost', 'Unnamed: 9': 'Tax', 'Unnamed: 12': 'Total cost'})
	final_table = final_table.loc[(final_table['Sold by']!='Item price')]
	final_table = final_table.loc[(final_table['Sold by']!='Shipping')]
	final_table = final_table.loc[(final_table['Sold by']!='Tax')]
	final_table = final_table.loc[(final_table['Sold by']!='')]
	final_table = final_table.loc[(final_table['Sold by']!='Total price')]
	final_table['Item price'] = final_table['Item price'].str.replace('$','')
	final_table['Sold by'] = final_table['Sold by'].str.replace('Opens in a new window','')
	final_table = final_table[final_table['Sold by'].notna()]
	final_table.drop(['Details & special offers'],axis=1,inplace=True)
	final_table = final_table [['Sold by', 'Item price', 'Total price',]]
	final_table['Total price'] = final_table['Total price'].str.replace('Item price',' Item price ')
	final_table['Total price'] = final_table['Total price'].str.replace('Shipping',' Shipping ')
	final_table['Total price'] = final_table['Total price'].str.replace('Tax',' Tax ')
	final_table['Total price'] = final_table['Total price'].str.replace('Total price',' Total price ')
	final_table['Total price'] = final_table['Total price'].str.replace('$','')
	final_table['Total price'] = final_table['Total price'].str.replace(',','')
	final_table['Item price'] = final_table['Item price'].str.replace(',','')
	final_table.reset_index(inplace=True)
	final_table.drop(['index'],axis=1,inplace=True)

	for i in range(len(final_table['Total price'])):
	    x = final_table['Total price'][i].find('Shipping ')
	    final_table['Total price'][i] = final_table['Total price'][i][x:]

	final_table['Shipping'] = final_table['Total price']

	for i in range(len(final_table['Total price'])):
	    x = final_table['Total price'][i].find('Tax ')
	    final_table['Shipping'][i] = final_table['Shipping'][i][9:x]

	final_table['Tax'] = final_table['Total price']

	for i in range(len(final_table['Total price'])):
	    x = final_table['Total price'][i].find('Total ')
	    y = final_table['Total price'][i].find(' T')
	    final_table['Tax'][i] = final_table['Tax'][i][y+4:x]

	final_table = final_table.drop(['Total price'],axis=1)
	final_table['Item price'] = pd.to_numeric(final_table['Item price'])
	final_table['Shipping'] = pd.to_numeric(final_table['Shipping'])
	final_table['Tax'] = pd.to_numeric(final_table['Tax'])

	final_table['Final Price'] = final_table['Item price'] + final_table['Shipping'] + final_table['Tax']
	final_table = final_table [['Sold by', 'Item price', 'Shipping', 'Tax', 'Final Price']]
	final_table = final_table.sort_values(by=['Final Price'])
	final_table.reset_index(inplace=True, drop=True)
	sellers_data = json.loads(final_table.to_json(orient = "records"))
	data = {"BC ID": int(bc_id), "date": dt.datetime.today().strftime('%m-%d-%Y %H:%M'),"Shopping ID": str(shop_id),"Amazon vendor": amazon_vendor,"Amazon Price": amazon_price,"Google Shopping": sellers_data}
	return data
def json_to_mongo(json_data, mongo_obj):
    return ""
def fix_data_mongo(dataFrame):
	stores = []
	for x in google.find():
		stores.append(x)

	result = json_normalize(stores, 'Google Shopping', ['BC ID', 'Shopping ID', 'date', 'Amazon vendor', 'Amazon Price'])
	result['Shipping cost'] = result['Shipping cost'].str.replace('$','')
	result['Tax'] = result['Tax'].str.replace('$','')
	result['Total cost'] = result['Total cost'].str.replace('$','')
	result['Amazon Price'] = result['Amazon Price'].str.replace('$','')
	result['Item price'] = result['Item price'].str.replace('$','')
	result['Item price'] = result['Item price'].str.replace('NO','')
	result['Item price'] = result['Item price'].str.replace(' minimum order','')
	result['Item price'] = result['Item price'].str.replace(',','')
	result['Amazon Price'] = result['Amazon Price'].str.replace(',','')
	result['Amazon vendor'] = result['Amazon vendor'].str.replace('Ships from and sold by ','')
	result['Amazon vendor'] = result['Amazon vendor'].str.replace(' in easy-to-open packaging','')
	result['Amazon vendor'] = result['Amazon vendor'].str.replace('Sold by ','')
	result['Amazon vendor'] = result['Amazon vendor'].str.replace('and Fulfilled by Amazon ','')
	result['Amazon vendor'] = result['Amazon vendor'].str.replace('Contractor Source and Fulfilled by ','')
	# result['Amazon Price'] = result['Amazon Price'].apply(pd.to_numeric)
	result.drop(result.loc[result['Sold by']=='eBay'].index, inplace=True)
	result.drop(result.loc[result['Sold by']=='Industrial Safety Products'].index, inplace=True)
	result.drop(result.loc[result['Amazon vendor']=='E-Com Supply.'].index, inplace=True)
	result.drop(result.loc[result['Sold by']=='Walmart - Independence ...'].index, inplace=True)
	result.drop(result.loc[result['Sold by']=='Walmart'].index, inplace=True)
	result.drop(result.loc[result['Sold by']=='Walmart - Aymity Safety'].index, inplace=True)
	result.drop(result.loc[result['Sold by']=='Walmart - Top Dog Tool'].index, inplace=True)
	result.drop(result.loc[result['Sold by']=='Walmart - Saferite Solutions Inc'].index, inplace=True)
	result.drop(result.loc[result['Sold by']=='Walmart - SIM Supply Inc'].index, inplace=True)
	result.drop(result.loc[result['Sold by']=='Walmart - Texas America Safety ...'].index, inplace=True)
	result.drop(result.loc[result['Sold by']=='Walmart - CALIFORNIA TOOLS LLC'].index, inplace=True)
	result.drop(result.loc[result['Sold by']=='Walmart - Zoro'].index, inplace=True)
	result['Shopping ID'] = result['Shopping ID'].apply(pd.to_numeric)
	dataFrame['Shopping ID'] = dataFrame['Shopping ID'].apply(pd.to_numeric)
	result = result.drop_duplicates(['Shopping ID'])
	result = result.reset_index()
	result = result.merge(dataFrame, left_on='Shopping ID', right_on='Shopping ID')

	return result
def feed_repricer(result):
	pricer_data = []

	for i in range(len(result['Sold by'])):
		#item = bc.get_product(str(result['BC ID'][i]))

		print("Sku: " + str(result['SKU'][i]))
		print('we are currently at ' + str(result['Total Price'][i]))

		# Check who got the lowest price between amazon and google shooping
		if result['Total cost'][i] < result['Amazon Price'][i]:
			competitor_price = result['Total cost'][i]
			competitor_name = result['Sold by'][i]
		else:
			competitor_price = result['Amazon Price'][i]
			competitor_name = result['Amazon vendor'][i]

		# Checks if we are above the lowest competitor
		if competitor_price < result['Total Price'][i]:
			# Checks if the lowest competitor is above our lowest price
			if competitor_price > result['Min'][i]:
				print("Competitor Price: " + str(competitor_price))
				print("Competitor name: " + competitor_name)
				print("we can go down to " + str(competitor_price - 1))
				final_price = str(competitor_price - 1)
				message = "we can go down to " + str(competitor_price - 1)
			else:
				print("Competitor Price: " + str(competitor_price))
				print("Competitor name: " + competitor_name)
				print("we can't go down")
				message = "we can't go down"
				final_price = result['Min'][i]
		else:
			print("we could go up to " + "$" + str(round(competitor_price-0.5)))
			print("Competitor Price: " + str(competitor_price))
			print("Competitor name: " + competitor_name)
			final_price = round(competitor_price-0.5)
			message = "we could go up to " + "$" + str(round(competitor_price-0.5))

	#         items = "{\"id\":" + str(result['BC ID'][i]) + "," + "\"price\":" + str(round(x-0.5)) + "}"
	#         r = bc.Updates_product(result['BC ID'][i], str(items))

		if result['Total Price'][i] < result['Min'][i]:
			message = ("We are below MIN price we should go up to " + str(result['Min'][i]))

		print("-----------------------------------")

		col = {'Date': dt.datetime.today(),
		   'SKU': result['SKU'][i],
		   'Competitor name': competitor_name,
		   'Competitor price': competitor_price,
		   'Our price': result['Total Price'][i],
		   'Our price fixed': final_price,
			'Min price': result['Min'][i],
			'Message': message,
			'BC ID': result['BC ID_x'][i]
		  }
		pricer_data.append(col)

	data = pd.DataFrame(pricer_data, columns=['Date', 'SKU', 'BC ID', 'Competitor name', 'Competitor price',
											 'Our price', 'Min price', 'Our price fixed', 'Message'])

	hoja2 = sh.worksheet('Pricer')
	gd.set_with_dataframe(hoja2,data,resize=True)
def update_prices(dataFrame):
	dataFrame['BC ID'].astype(int)
	for i in range(len(dataFrame)):
		sleep(1)
		bc_info = bc.get_product(str(dataFrame['BC ID'][i]))
		hoja.update_acell('H' + str(i+2), bc_info['data']['price'])

# while True:
for i in range(1):#len(data_after['Shopping ID'])):
	try:
		page = shopping_bot(data_after['Shopping ID'][i])

		if data_after['asin'][i] == 0:
			amazon_price = 0
			amazon_vendor = 0
		else:
			amazon_price, amazon_vendor = amazon_bot(data_after['asin'][i])

		data = fix_data_repricer(page,data_after['Shopping ID'][i],data_after['BC ID'][i], amazon_price, amazon_vendor)
		google.insert_one(data)
	except:
		pass
#
# #action
# html = pyperclip.paste()
# soup = BeautifulSoup(html, 'lxml')
# # page = soup.find("section",{"id":"transactable"})
#
# # #normal table
# html = pyperclip.paste()
# soup = BeautifulSoup(html, 'lxml')
# page = soup.find("section",{"id":"online"})
#
# table = page.find("table")
# final_table = pd.read_html(str(table))
# final_table = final_table[0]
# # final_table = final_table.rename(columns={'Unnamed: 7': 'Shipping cost', 'Unnamed: 9': 'Tax', 'Unnamed: 12': 'Total cost'})
# final_table = final_table.loc[(final_table['Sold by']!='Item price')]
# final_table = final_table.loc[(final_table['Sold by']!='Shipping')]
# final_table = final_table.loc[(final_table['Sold by']!='Tax')]
# final_table = final_table.loc[(final_table['Sold by']!='')]
# final_table = final_table.loc[(final_table['Sold by']!='Total price')]
# final_table['Item price'] = final_table['Item price'].str.replace('$','')
# final_table['Sold by'] = final_table['Sold by'].str.replace('Opens in a new window','')
# final_table = final_table[final_table['Sold by'].notna()]
# final_table.drop(['Details & special offers'],axis=1,inplace=True)
# final_table = final_table [['Sold by', 'Item price', 'Total price',]]
# final_table['Total price'] = final_table['Total price'].str.replace('Item price',' Item price ')
# final_table['Total price'] = final_table['Total price'].str.replace('Shipping',' Shipping ')
# final_table['Total price'] = final_table['Total price'].str.replace('Tax',' Tax ')
# final_table['Total price'] = final_table['Total price'].str.replace('Total price',' Total price ')
# final_table['Total price'] = final_table['Total price'].str.replace('$','')
# final_table['Total price'] = final_table['Total price'].str.replace(',','')
# final_table['Item price'] = final_table['Item price'].str.replace(',','')
# final_table.reset_index(inplace=True)
# final_table.drop(['index'],axis=1,inplace=True)
#
# for i in range(len(final_table['Total price'])):
#     x = final_table['Total price'][i].find('Shipping ')
#     final_table['Total price'][i] = final_table['Total price'][i][x:]
#
# final_table['Shipping'] = final_table['Total price']
#
# for i in range(len(final_table['Total price'])):
#     x = final_table['Total price'][i].find('Tax ')
#     final_table['Shipping'][i] = final_table['Shipping'][i][9:x]
#
# final_table['Tax'] = final_table['Total price']
#
# for i in range(len(final_table['Total price'])):
#     x = final_table['Total price'][i].find('Total ')
#     y = final_table['Total price'][i].find(' T')
#     final_table['Tax'][i] = final_table['Tax'][i][y+4:x]
#
# final_table = final_table.drop(['Total price'],axis=1)
# final_table['Item price'] = pd.to_numeric(final_table['Item price'])
# final_table['Shipping'] = pd.to_numeric(final_table['Shipping'])
# final_table['Tax'] = pd.to_numeric(final_table['Tax'])
#
# final_table['Final Price'] = final_table['Item price'] + final_table['Shipping'] + final_table['Tax']
# final_table = final_table [['Sold by', 'Item price', 'Shipping', 'Tax', 'Final Price']]
# final_table = final_table.sort_values(by=['Final Price'])
# final_table.reset_index(inplace=True, drop=True)
# sellers_data = json.loads(final_table.to_json(orient = "records"))
