import requests
import json
import boto3
from pandas.io.json import json_normalize

class DFConverter:

    #Converts the input JSON to a DataFrame
    def convertToDF(self,dfJSON):
        return(json_normalize(dfJSON))

    #Converts the input DataFrame to JSON
    def convertToJSON(self, df):
        resultJSON = df.to_json(orient='records')
        return(resultJSON)

def get_s3_file(key, secret, filename):
    BUCKET = 'connect-b41e18daa2fc'
    FILE = filename
    client = boto3.resource('s3', aws_access_key_id=key, aws_secret_access_key=secret)
    obj = client.Object(BUCKET, FILE)
    r = obj.get()['Body'].read()
    return json.loads(r)

def get_aws_token():
    with open('C:\\AWS\\AWS.json', 'r') as json_file:
        d1 = json_file.read()
    d = json.loads(d1)
    return d

def pricing(cost, level, deviation=False, margin=False):
    markup = [[0.350, 0.400, 0.450, 0.500],
              [0.300, 0.350, 0.400, 0.450],
              [0.250, 0.300, 0.350, 0.400],
              [0.200, 0.275, 0.325, 0.375],
              [0.180, 0.225, 0.275, 0.325],
              [0.150, 0.200, 0.250, 0.300]]

    if deviation:
        dev = 0.05
    else:
        dev = 0

    if cost <= 2.5:
        tier = 0
    elif cost <= 7:
        tier = 1
    elif cost <= 15:
        tier = 2
    elif cost <= 50:
        tier = 3
    elif cost <= 150:
        tier = 4
    else:
        tier = 5

    if margin:
        p = markup[tier][level] + dev
        result = str(int(p*100)) + '%'
    else:
        p = cost / (1 - (markup[tier][level] + dev))
        result = round(p,2)

    return result

class BooksZohoApi:
    def __init__(self,token):
        """ This is a test"""
        self.endpoint = 'https://books.zoho.com/api/v3/'
        self.authtoken = '?organization_id=683229417'
        self.headers = {"Authorization": token,
           "Content-Type": "application/json;charset=UTF-8",}
    def transfer_order(self, json_file, autogen=True):
        self.module = 'transferorders'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data, 'ignore_auto_number_generation': autogen}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def list_contacts(self):
        self.module = 'contacts'
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def get_contact(self, contact_id):
        """Get contact information.

        Contact_id must be passed"""
        self.module = 'contacts/' + contact_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def update_item(self, item_id, json_file):
        self.module = 'items/' + item_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data}
        self.request = requests.put(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def update_bill(self, bill_id, json_file):
        self.module = 'bills/' + bill_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data}
        self.request = requests.put(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def get_item(self, item_id):
        self.module = 'items/' + item_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def item_inactive(self, item_id):
        self.module = 'items/' + item_id + '/inactive'
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.post(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def delete_items(self, item_id):
        self.module = 'items/' + item_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.delete(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def create_items(self, json_data):
        self.module = 'items/'
        self.payload = self.endpoint +self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def create_bill(self, json_data):
        self.module = 'bills/'
        self.payload = self.endpoint +self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.put(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def retrieve_porder(self, order_id):
        self.module = 'purchaseorders/' + str(order_id)
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def create_purchase_receive(self, purchase_id, json_data):
        self.module = 'purchasereceives/'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data, 'purchaseorder_id': purchase_id, 'ignore_auto_number_generation': 'true'}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def create_bills_receive(self, bill_id, purchase_id, json_data):
        self.module = 'purchasereceives/'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data, 'bill_id': bill_id, 'purchaseorder_id': purchase_id, 'ignore_auto_number_generation': 'true'}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def retrieve_bills(self, bills_id):
        self.module = 'bills/' + bills_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def retrieve_order(self, order_id):
        self.module = 'salesorders/' + order_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def update_order(self, order_id, json_data):
        self.module = 'salesorders/' + order_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.put(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def delete_sorder(self, order_id):
        self.module = 'salesorders/' + order_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.delete(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def delete_porder(self, order_id):
        self.module = 'purchaseorders/' + order_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.delete(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def delete_invoice(self, invoice_id):
        self.module = 'invoices/' + invoice_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.delete(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def delete_shipment(self, shipment_id):
        self.module = 'shipmentorders/' + shipment_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.delete(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def delete_package(self, package_id):
        self.module = 'packages/' + package_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.delete(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def delete_payments(self, customerpayments_id):
        self.module = 'customerpayments/' + customerpayments_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.delete(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def delete_estimates(self, estimates_id):
        self.module = 'estimates/' + estimates_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.delete(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def list_sorders(self, page):
        self.module = 'salesorders'
        self.payload = self.endpoint + self.module + self.authtoken
        self.params = {'page': page}
        self.request = requests.get(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def list_porders(self, page):
        self.module = 'purchaseorders'
        self.payload = self.endpoint + self.module + self.authtoken
        self.params = {'page': page}
        self.request = requests.get(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def void_order(self, order_id):
        self.module = 'salesorders/' + order_id + '/status/void'
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.post(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def create_shipment(self, package_id, so_id, json_data ):
        #self.module = 'shipmentorders?salesorder_id=' + str(so_id) + '&package_ids=' + str(package_id) + '&'
        self.module = 'shipmentorders'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data, 'ignore_auto_number_generation': True, 'salesorder_id': so_id, 'package_ids': [package_id]}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def create_order(self, json_file, autogen=True):
        self.module = 'salesorders'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data, 'ignore_auto_number_generation': autogen}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def create_contact_address(self, contact_id, json_data):
        self.module = 'contacts/' + contact_id + '/address'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def update_contact_address(self, contact_id, address_id, json_data):
        self.module = 'contacts/' + contact_id + '/address/' + address_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.put(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def get_contact_address(self, contact_id):
        self.module = 'contacts/' + contact_id + '/address'
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def get_package(self, package_id):
        self.module = 'packages/' + package_idsssssssss
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def update_package(self, package_id, json_data):
        self.module = 'packages/' + package_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data}
        self.request = requests.put(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def list_packages(self, page):
        self.module = 'packages'
        self.payload = self.endpoint + self.module + self.authtoken
        self.params = {'page': page}
        self.request = requests.get(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def get_customerpayments(self):
        self.module = 'customerpayments/' + customerpayments_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.post(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def get_shipment(self, shipment_id):
        self.module = 'shipmentorders/' + shipment_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.post(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def delivered(self, shipment_id):
        self.module = 'shipmentorders/' + shipment_id + '/status/delivered'
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.post(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def update_vendorpayment(self, payment_id, json_data):
        self.module = 'vendorpayments/' + payment_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.put(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def create_invoice(self, json_file):
        self.module = 'invoices'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def create_cxpayment(self, json_file):
        self.module = 'customerpayments'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def create_package(self, order_id, json_data):
        self.module = 'packages'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data, 'salesorder_id': order_id}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def delivered(self, shipment_id):
        self.module = 'shipmentorders/' + shipment_id + '/status/delivered'
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.post(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def create_shipment(self, package_id, so_id, json_data, autogen=False):
        #self.module = 'shipmentorders?salesorder_id=' + str(so_id) + '&package_ids=' + str(package_id) + '&'
        self.module = 'shipmentorders'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data, 'ignore_auto_number_generation': autogen, 'salesorder_id': so_id, 'package_ids': [package_id]}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r

class InventoryZohoApi:
    def __init__(self,token):
        self.endpoint = 'https://inventory.zoho.com/api/v1/'
        self.authtoken = '?authtoken=' + token + '&organization_id=683229417'
        self.authtoken2 = 'authtoken=' + token + '&organization_id=683229417'
        self.headers = {"Authorization": token,
           "Content-Type": "application/json;charset=UTF-8",}
    def list_contacts(self):
        self.module = 'contacts'
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def list_pricebooks(self):
        self.module = 'pricebooks'
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def get_pricebooks(self, pricebook_id):
        self.module = 'pricebooks/' + pricebook_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def update_pricebooks(self, pricebook_id, json_data):
        self.module = 'pricebooks/' + pricebook_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.put(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def get_contact(self, contact_id):
        """Get contact information.

        Contact_id must be passed"""
        self.module = 'contacts/' + contact_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def update_item(self, item_id, json_file):
        self.module = 'items/' + item_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data}
        self.request = requests.put(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def get_item(self, item_id):
        self.module = 'items/' + item_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def item_inactive(self, item_id):
        self.module = 'items/' + item_id + '/inactive'
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.post(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def delete_items(self, item_id):
        self.module = 'items/' + item_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.delete(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def create_items(self, json_data):
        self.module = 'items/'
        self.payload = self.endpoint +self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def create_bill(self, json_data):
        self.module = 'bills'
        self.payload = self.endpoint +self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def retrieve_bills(self, bills_id):
        self.module = 'bills/' + bills_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def retrieve_sorder(self, order_id):
        self.module = 'salesorders/' + order_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def retrieve_porder(self, order_id):
        self.module = 'purchaseorders/' + order_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def update_order(self, order_id, json_data):
        self.module = 'salesorders/' + order_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.put(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def delete_sorder(self, order_id):
        self.module = 'salesorders/' + order_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.delete(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def delete_porder(self, order_id):
        self.module = 'purchaseorders/' + order_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.delete(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def delete_invoice(self, invoice_id):
        self.module = 'invoices/' + invoice_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.delete(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def delete_shipment(self, shipment_id):
        self.module = 'shipmentorders/' + shipment_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.delete(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def delete_package(self, package_id):
        self.module = 'packages/' + package_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.delete(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def delete_payments(self, customerpayments_id):
        self.module = 'customerpayments/' + customerpayments_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.delete(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def list_sorders(self, page):
        self.module = 'salesorders'
        self.payload = self.endpoint + self.module + self.authtoken
        self.params = {'page': page}
        self.request = requests.get(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def list_porders(self, page):
        self.module = 'purchaseorders'
        self.payload = self.endpoint + self.module + self.authtoken
        self.params = {'page': page}
        self.request = requests.get(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def void_order(self, order_id):
        self.module = 'salesorders/' + order_id + '/status/void'
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.post(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def create_shipment(self, package_id, so_id, json_data, autogen=False):
        #self.module = 'shipmentorders?salesorder_id=' + str(so_id) + '&package_ids=' + str(package_id) + '&'
        self.module = 'shipmentorders'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data, 'ignore_auto_number_generation': autogen, 'salesorder_id': so_id, 'package_ids': [package_id]}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def create_order(self, json_file, autogen=True):
        self.module = 'salesorders'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data, 'ignore_auto_number_generation': autogen}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def create_contact_address(self, contact_id, json_data):
        self.module = 'contacts/' + contact_id + '/address'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def update_contact_address(self, contact_id, address_id, json_data):
        self.module = 'contacts/' + contact_id + '/address/' + address_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.put(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def get_contact_address(self, contact_id):
        self.module = 'contacts/' + contact_id + '/address'
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def get_package(self, package_id):
        self.module = 'packages/' + package_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def update_package(self, package_id, json_data):
        self.module = 'packages/' + package_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data}
        self.request = requests.put(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def list_packages(self, page):
        self.module = 'packages'
        self.payload = self.endpoint + self.module + self.authtoken
        self.params = {'page': page}
        self.request = requests.get(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def get_customerpayments(self, customerpayments_id):
        self.module = 'customerpayments/' + customerpayments_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def get_shipment(self, shipment_id):
        self.module = 'shipmentorders/' + shipment_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.post(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def deliver_shipment(self, shipment_id):
        self.module = 'shipmentorders/' + shipment_id + '/status/delivered'
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.post(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def create_invoice(self, json_file):
        self.module = 'invoices'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def create_inventory_adjustment(self, json_file):
        self.module = 'inventoryadjustments'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def delivered(self, shipment_id):
        self.module = 'shipmentorders/' + shipment_id + '/status/delivered'
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.post(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def create_cxpayment(self, json_file):
        self.module = 'customerpayments'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def get_invoices(self, invoice_id):
        self.module = 'invoices/' + invoice_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def update_vendorpayment(self, payment_id, json_data):
        self.module = 'vendorpayments/' + payment_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.put(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def update_bill(self, bill_id, json_file):
        self.module = 'bills/' + bill_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data}
        self.request = requests.put(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def create_package(self, order_id, json_data):
        self.module = 'packages'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data, 'salesorder_id': order_id}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def item_adjustment(self,json_file):
        self.module = 'inventoryadjustments'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def transfer_order(self, json_file, autogen=True):
        self.module = 'transferorders'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_file)
        self.params = {'JSONString': self.data, 'ignore_auto_number_generation': autogen}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def get_transferorder(self, transferorders_id):
        self.module = 'transferorders/'
        self.payload = self.endpoint + self.module + str(transferorders_id) + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.requests.text)
        return self.r

class bcispapi:
    def __init__(self):
        self.endpoint = 'https://api.bigcommerce.com/stores/e163lt99/v2/'
        self.endpoint1 = 'https://api.bigcommerce.com/stores/e163lt99/v3/'
        self.headers = {'accept': "application/json",
        'content-type': "application/json",
        'x-auth-token': "cqmn8oiw446hjiqkyp7gmlg6aolooa4",
        'x-auth-client': "646cipi08q4y96gegsja9n4f7wwwkts",}
        self.headers1 = {'accept': "application/json",
        'content-type': "application/json",
        'x-auth-token': "i9iraumus6c3zpa8a3pqz9le1fgv245",
        'x-auth-client': "foiciztdz4mptpgy83rj08brrphomb2",}

    def get_orders_mid_id(self,last_isp):
        self.module = 'orders'
        self.payload = self.endpoint + self.module
        self.params = {'min_id':int(last_isp)}
        self.request = requests.get(url=self.payload, headers=self.headers1, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def get_order(self,order_id):
        self.module = 'orders/' +str(order_id)
        self.payload = self.endpoint + self.module
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def get_order_product(self,order_id):
        self.module = 'orders/' +str(order_id) + '/products'
        self.payload = self.endpoint + self.module
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def get_order_coupons(self,order_id):
        self.module = 'orders/' + order_id + '/coupons'
        self.payload = self.endpoint + self.module
        self.request = requests.get(url=self.payload, headers=self.headers)
        return self.request
    def url_cupon(self,url):
        self.module = url
        self.request = requests.get(url=self.module, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def shipments(self,order_id):
        self.module = 'orders/' +str(order_id) + '/shipments'
        self.payload = self.endpoint + self.module
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def Updates_product(self,product_id ,json_data):
        self.module = 'catalog/products/'+str(product_id)
        self.payload = self.endpoint1 +self.module
        self.data = json_data
        self.request = requests.put(url=self.payload, headers=self.headers1, data=self.data)
        self.r = json.loads(self.request.text)
        return self.r
    def get_product(self,product_id):
        self.module = 'catalog/products/' + product_id
        self.payload = self.endpoint1 + self.module
        self.request = requests.get(url=self.payload, headers=self.headers1)
        self.r = json.loads(self.request.text)
        return self.r
    def get_productALL(self):
        self.module = 'catalog/products/'
        self.payload = self.endpoint1 + self.module
        self.request = requests.get(url=self.payload, headers=self.headers1)
        self.r = json.loads(self.request.text)
        return self.r
    def get_product_bulk_pricing(self,product_id):
        self.module = 'catalog/products/' + str(product_id)+ '/bulk-pricing-rules'
        self.payload = self.endpoint1 + self.module
        self.request = requests.get(url=self.payload, headers=self.headers1)
        self.r = json.loads(self.request.text)
        return self.r
    def Updates__bulk_pricing(self,product_id ,bulk_pricing_rule_id,json_data):
        self.module = 'catalog/products/'+str(product_id)+'/bulk-pricing-rules/'+str(bulk_pricing_rule_id)
        self.payload = self.endpoint1 +self.module
        self.data = json_data
        self.request = requests.put(url=self.payload, headers=self.headers1, data=self.data)
        self.r = json.loads(self.request.text)
        return self.r
    def get_product_variant(self,product_id,option_id):
        self.module = 'catalog/products/' + str(product_id)+ '/options/' + str(option_id)
        self.payload = self.endpoint1 + self.module
        self.request = requests.get(url=self.payload, headers=self.headers1)
        self.r = json.loads(self.request.text)
        return self.r
