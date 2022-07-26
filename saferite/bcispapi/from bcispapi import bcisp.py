from bcispapi import bcisp
from bcispapi import bcispapi
from zohoapi import zohoapi_new
import pymongo
import json
from bcispapi import bc
import pandas as pd
import gspread as gs
import gspread_dataframe as gd
from oauth2client.service_account import ServiceAccountCredentials
import time

store = 'ISP'
bc1 = bc.bcispapi()
isp = bc.bcapi(store)
aws = zohoapi_new.get_aws_token()
zoho_token = zohoapi_new.get_s3_file(aws['AWS_KEY'],aws['SECRET_KEY'], 'zoho_token.json')
zh = zohoapi_new.InventoryZohoApi(zoho_token['INV_KEY'])

HOST = '3.210.205.130'
PORT = 27017
USER = 'jesfel'
PASS = 'FelipeSuperSecretPassword*987'
cstr = 'mongodb://{}:{}@{}:{}/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false'.format(USER, PASS, HOST, PORT)
conn = pymongo.MongoClient(cstr)
db = conn['ISP']
orders = db['Orders']
last_order = db['last_order']
items_bc = db['items_bc']
customer = db['Customers']
dbzh = conn['Zoho_Mirror']
so = dbzh['SO']

gskey = 'D:\\PY\\SL.json'
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(gskey,scope)
gc = gs.authorize(credentials)
gsheet = 'https://docs.google.com/spreadsheets/d/1O4vDV1ImWirImGPKq_Y4cOdiJORdjXImtqzup7sRVBI/edit#gid=0'
sh = gc.open_by_url(gsheet)

def fix_guest_customers(email):
    cx_info = isp.get_customer_by_email(email)
    if cx_info != '':
        return cx_info[0]['id']
    return 0

def search_inf(i,data):
    item_id = 0
    qt = 0
    pt = 0
    if i in data.values():
        consecutivo = i[2:3]
        inicial = str(data.items()).find(i)
        numero = str(data.items())[inicial-6:inicial-4]
        item_id = data['value_'+str(numero)]

        inicial = str(data.items()).find('qt'+str(consecutivo))
        numero = str(data.items())[inicial-6:inicial-4]
        qt = data['value_'+str(numero)]

        inicial = str(data.items()).find('pt'+str(consecutivo))
        numero = str(data.items())[inicial-6:inicial-4]
        pt = data['value_'+str(numero)]
    return item_id,qt,pt

def covert_dicctionary(lists):
    final = {}
    count = 10
    for dics in lists:
        count += 1
        for key in dics.keys():
            final.setdefault(key.lower()+'_'+str(count),dics[key])
    return final

def update_customer_zoho(order):
    if float(order['total_tax']) == 0.0:
        tax = ''
        taxable = False
        authority = 'OUT OF STATE'
        exemption = 'FL State'
    else:
        taxable = True
        exemption = ''
        authority = ''
        tax_exemption_id = 1729377000002313511
        tax = 1729377000027355808

    cx_data = {
    'is_taxable': taxable,
    'tax_exemption_code': exemption,
    'tax_authority_name':  authority,
    'tax_id': tax,}

    zh.update_contact(order['Zoho Customer ID'][0], cx_data)

def dfadjustment(so_items,order,adjustment ):
    total_price = 0
    for total in so_items:
        price = total['rate'] * total['quantity']
        total_price = total_price + price
    if float(order['subtotal_ex_tax']) < total_price:
        if total['tax_id'] == '':
            adjustment = total_price - float(order['subtotal_ex_tax'])
            adjustment_description = 'Rounding'
            return  adjustment, adjustment_description
        else:
            adjustment = adjustment + float(total_price) - float(order['subtotal_ex_tax'])
            adjustment_description = 'Tax Adjustment'
            return adjustment, adjustment_description

def order_product_coupons(orders_bc):
    inf_order = []
    for order in orders_bc:
        order['items'] = bc1.get_order_product(order['id'])
        if order['customer_id'] == 0:
            order['customer_id'] = fix_guest_customers(order['billing_address']['email'])
        order['Zoho Customer ID'] = [id['Zoho Customer ID'] for id in customer.find({"ISP Customer ID":order['customer_id']})]
        inf_order.append(order)
        promo = bc1.get_order_coupons(order['id'])
        if promo.status_code == 200:
            inf_disc = json.loads(promo.text)
            order['discount'] = inf_disc
            inf_disc = json.loads(promo.text)
        else:
            order['discount'] = []
        result = orders.update_one({"id": order['id']},{"$set": order}, upsert=True).raw_result
    return inf_order

def date_format(date):
        da = pd.to_datetime(date)
        da = da.strftime('%Y-%m-%d')
        return da


sheet1 = sh.worksheet('orders')
vorder = gd.get_as_dataframe(sheet1)
sheet2 = sh.worksheet('items')
vitmes = gd.get_as_dataframe(sheet2)
sheet3 = sh.worksheet('listas')

order_ok = gd.get_as_dataframe(sheet3)
last_isp = [order for order in last_order.find()][0]['last_isp']
orders_bc = bc1.serch_orders(bc1,last_isp)
inf_order = order_product_coupons(orders_bc[1])


if store == 'SS':
    template_id = '1729377000028731199'
    template = 'SS'
else:
    template_id = '1729377000028731259'
    template = 'ISP'
create_orders_ok = []
not_create_orders = []

for order in inf_order:
    if order['status'] != 'Incomplete' or order['status'] != 'Cancelled':
        if order['Zoho Customer ID'] != []:
            update_customer_zoho(order)
            so_items = []
            not_items  = []
            if float(order['total_tax']) == 0.0:
                tax = ''
                adjustment = ''
                adjustment_description = ''
            else:
                tax = 1729377000027355808
                adjustment = float(order['base_shipping_cost'])*0.07
                adjustment_description = 'Tax Adjustment'
            for item in order['items']:
                item_mg = [id for id in items_bc.find({'$and':[{'id':item['product_id']},{'variants.id':item['variant_id']}]})]
                if item_mg != []:
                    if len(item_mg[0]['variants']) > 1:
                        for i in item_mg[0]['variants']:
                            if i['id'] == item['variant_id'] and i['sku'] == str(item['sku']):
                                if i['bin_picking_number'] != '':
                                    bpn = i['bin_picking_number'].replace("'", '"')
                                    bpn = json.loads(bpn)
                                    if len(bpn) > 1:
                                        for k in bpn:
                                            if len(item['product_options'])>1:
                                                qt = int(item['quantity'] / len(item['product_options']))*int(k['qt'])
                                            else:
                                                qt = item['quantity']*int(k['qt'])
                                            so_line = {
                                            'item_id': int(k['id']),
                                            'rate': (float(item['base_price'])*float(k['pt']))/qt,
                                            'quantity': qt,
                                            'tax_id': tax,}
                                            so_items.append(so_line)
                                    else:
                                        so_line = {
                                        'item_id': int(bpn[0]['id']),
                                        'rate': (float(item['base_price']))/int(bpn[0]['qt']),
                                        'quantity': item['quantity']*int(bpn[0]['qt']),
                                        'tax_id': tax,}
                                        so_items.append(so_line)
                                else:
                                    r = {
                                    'id_order':order['id'],
                                    'product_id':item['product_id'],
                                    'sku':item['sku'],
                                    'message':'Not information Mongo DB'
                                    }
                                    not_items.append(r)
                    else:
                        custom_fields = item_mg[0]['custom_fields']
                        validation = 0
                        for fields in custom_fields:
                            if fields['name'] == 'id':
                                item_id = fields['value']
                                validation = validation + 1
                            if fields['name'] == 'qt':
                                validation = validation + 1
                                qt = fields['value']
                            if validation == 2:
                                so_line = {
                                'item_id': int(item_id),
                                'rate': float(item['base_price'])/int(qt),
                                'quantity': item['quantity']*int(qt),
                                'tax_id': tax,}
                                so_items.append(so_line)
                                validation = 0
                            if  fields['name'] == 'id0':
                                var = ['id0','id1','id2','id3','id4','id5','id6','id7','id8','id9']
                                data  = covert_dicctionary(custom_fields)
                                for i in var:
                                    item_id,qt,pt = search_inf(i,data)
                                    if item_id != 0:
                                        so_line = {
                                        'item_id': int(item_id),
                                        'rate': (float(item['base_price'])*float(pt))/int(qt),
                                        'quantity': item['quantity']*int(qt),
                                        'tax_id': tax,}
                                        so_items.append(so_line)
                else:
                    r = {
                    'id_order':order['id'],
                    'product_id':item['product_id'],
                    'sku':item['sku'],
                    'message':'Not information Mongo DB'
                    }
                    not_items.append(r)
    #         if len(so_data['line_items']) >
            total_price = 0
            for total in so_items:
                price = total['rate'] * total['quantity']
                total_price = total_price + price

            if order['discount'] != []:
                so_line = {
                'item_id': int(1729377000276122023),
                'rate': -float(order['discount'][0]['discount']),
                'quantity': 1,
                'tax_id': '',}
                so_items.append(so_line)
            if not_items != []:
                df_not_items = pd.json_normalize(not_items)
                data1 = vitmes.append(df_not_items)
                gd.set_with_dataframe(sheet2,data1,resize=True)

            so_data = {
                'template_id': template_id,
                'customer_id': int(order['Zoho Customer ID'][0]),
                'salesorder_number':store + str(-order['id']),
                'date': date_format(order['date_created']),
                'line_items': so_items,
                'shipping_charge': float(order['base_shipping_cost']),
                'custom_fields': [{'customfield_id': 1729377000039969865, 'value': 'Internet'},
                {'customfield_id': 1729377000040961274, 'value': template}],
                "adjustment" : adjustment,
                "adjustment_description" : adjustment_description,}
            if len(order['items']) <= len(so_data['line_items']):
                if float(order['subtotal_ex_tax']) != total_price:
                    if so_data['adjustment'] == '':
                        adjustment = float(order['subtotal_ex_tax']) - float(total_price)
                        adjustment_description = 'Rounding'
                    else:
                        adjustment = adjustment + (float(order['subtotal_ex_tax']) - float(total_price))
                        adjustment_description = 'Tax Adjustment'

                create_order = zh.create_order(so_data)
                if create_order['message'] == 'Sales Order has been created.':
                    so.insert_one(create_order)
                    create_order_ok = {
                    'id_order':order['id'],
                    'product_id':item['product_id'],
                    'sku':item['sku'],
                    'Message':create_order['message']
                    }
                    create_orders_ok.append(create_order_ok)
                else:
                    not_create_order = {
                    'id_order':order['id'],
                    'product_id':item['product_id'],
                    'sku':item['sku'],
                    'Message':create_order['message']
                    }
                    not_create_orders.append(not_create_order)
            else:
                not_create_order = {
                'id_order':order['id'],
                'product_id':order['product_id'],
                'sku':order['sku'],
                'Message':'Check the items, they do not match'
                }
                not_create_orders.append(not_create_order)
        else:
            not_create_order = {
                'id_order':order['id'],
                'product_id':'',
                'sku':'',
                'Message':'Customer not created'}
            not_create_orders.append(not_create_order)
    else:

        not_create_order = {
                'id_order':order['id'],
                'product_id':'',
                'sku':'',
                'Message':'order status' + order['status']}
        not_create_orders.append(not_create_order)

df_create_order_ok = pd.json_normalize(create_orders_ok)
data3 = order_ok.append(df_create_order_ok)
gd.set_with_dataframe(sheet3,data3,resize=True)

df_not_create_order = pd.json_normalize(not_create_orders)
data2 = vorder.append(df_not_create_order)
gd.set_with_dataframe(sheet1,data2,resize=True)

last_order.update_one({"last_isp": last_isp},{"$set":{'last_isp': orders_bc[0]}})
