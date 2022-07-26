import requests
import json
import boto3

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

def get_s3_file(key, secret, filename):
    BUCKET = 'connect-b41e18daa2fc'
    client = boto3.resource('s3', aws_access_key_id=key, aws_secret_access_key=secret)
    r = client.Object(BUCKET, filename).get()['Body'].read()
    return json.loads(r)
def send_s3_file(key, secret, filename, file):
    BUCKET = 'connect-b41e18daa2fc'
    s3 = boto3.resource('s3', aws_access_key_id=key, aws_secret_access_key=secret)
    r = s3.Object(BUCKET, FILE).put(Body=file)
    return json.loads(r)
def get_aws_token():
    with open('C:\\AWS\\AWS.json', 'r') as json_data:
        d1 = json_data.read()
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
    def __init__(self,zoho_token):
        payload = 'https://accounts.zoho.com/oauth/v2/token?refresh_token='+zoho_token['refresh_token']+'&redirect_uri=https://deluge.zoho.com/delugeauth/callback'+'&client_id='+zoho_token['client_id']+'&client_secret='+zoho_token['client_secret']+'&grant_type=refresh_token'
        self.endpoint = 'https://books.zoho.com/api/v3/'
        self.authtoken = '?organization_id=683229417'
        self.headers = {"Authorization":'Zoho-oauthtoken '+json.loads(requests.post(url=payload).text)['access_token'],
           "Content-Type": "application/json;charset=UTF-8",}
    def _standard_call(self, module, call_type, data=None, **kwargs):
        self.module = module
        self.payload = self.endpoint + self.module + self.authtoken
        additional_args = locals()['kwargs']

        if len(additional_args) == 0:
            if data == None:
                self.params = None
            else:
                self.params = {'JSONString': str(data)}
        else:
            if data == None:
                self.params = {}
            else:
                self.params = {'JSONString': str(data)}
            keys = []
            extra_param = {}
            for i in kwargs:
                keys.append(i)
                extra_param = {i: additional_args[i]}
                self.params.update(extra_param)
        if call_type == 'GET':
            self.request = requests.get(url=self.payload, headers=self.headers, params=self.params).text
        elif call_type == 'POST':
            self.request = requests.post(url=self.payload, headers=self.headers, params=self.params).text
        elif call_type == 'PUT':
            self.request = requests.put(url=self.payload, headers=self.headers, params=self.params).text
        elif call_type == 'DELETE':
            self.request = requests.delete(url=self.payload, headers=self.headers, params=self.params).text
        self.r = json.loads(self.request)
        return self.r

    # Create#
    def create_contacts(self, json_data):
        return self._standard_call('contacts','POST',json_data)
    def create_contact_person(self, json_data):
        return self._standard_call('contacts/contactpersons','POST',json_data)####
    def create_contact_address(self, contact_id, json_data):
        return self._standard_call('contacts/{}'.format(contact_id),'POST')
    def create_estimate(self, json_data):
        return self._standard_call('estimates','POST',json_data)####
    def create_sorder(self, json_data, autogen=True):
        return self._standard_call('salesorders','POST',json_data,ignore_auto_number_generation=autogen)
    def create_invoice(self, json_data):
        return self._standard_call('invoices','POST',json_data)
    def create_credit_note(self, json_data):
        return self._standard_call('creditnotes','POST',json_data)
    def create_creditnote(self, json_data):
        return self._standard_call('creditnotes','POST',json_data)
    def create_refunds(self,creditnote_id,json_data):
        return self._standard_call('creditnotes/{}/refunds'.format(creditnote_id),'POST',json_data)
    def create_customerPayments(self, json_data):
        return self._standard_call('customerpayments','POST',json_data)
    def create_expenses(self, json_data):
        return self._standard_call('expenses','POST',json_data)
    def create_porder(self, json_data):
        return self._standard_call('purchaseorders','POST',json_data)
    def create_purchase_receive(self, purchase_id, json_data):
        return self._standard_call('purchasereceives/','POST',json_data,purchaseorder_id=purchase_id,ignore_auto_number_generation='true')
    def create_bill(self, json_data):
        return self._standard_call('bills/','PUT',json_data)
    def create_bills_receive(self, bill_id, purchase_id, json_data):
        return self._standard_call('purchasereceives/','POST',json_data,bill_id=bill_id,purchaseorder_id=purchase_id,ignore_auto_number_generation='true')
    def create_vendor_credits(self,json_data,autogen=True):#####
        return self._standard_call('vendorcredits', 'POST', json_data, ignore_auto_number_generation=autogen)
    def create_vendor_payments(self,json_data,autogen=True):#####
        return self._standard_call('vendorpayments', 'POST',  json_data, ignore_auto_number_generation=autogen)
    def create_items(self, json_data):
        return self._standard_call('items/','POST',json_data)
    def create_shipment(self, package_id, so_id, json_data, autogen=False):
        return self._standard_call('shipmentorders','POST',json_data,ignore_auto_number_generation=autogen,salesorder_id=so_id,package_ids=[package_id])
    def create_package(self, order_id, json_data):
        return self._standard_call('packages','POST',json_data,salesorder_id=order_id)
    def create_transfer_order(self, json_data, autogen=True):
        return self._standard_call('transferorders', 'POST', json_data, ignore_auto_number_generation=autogen)

    # Update#
    def update_contact(self, item_id, json_data):
        return self._standard_call('items/{}'.format(item_id),'PUT',json_data)
    def update_contact_address(self, contact_id, address_id, json_data):
        return self._standard_call('contacts/{}/address/{}'.format(contact_id,address_id),'PUT',json_data)
    def update_estimates(self, estimate_id, json_data):####
        return self._standard_call('estimates/{}'.format(estimate_id), 'PUT', json_data)
    def update_estimate_billing(self, estimate_id, json_data):####
        return self._standard_call('estimates/{}/address/billing'.format(estimate_id), 'PUT', json_data)
    def update_estimate_shipping(self, estimate_id, json_data):####
        return self._standard_call('estimates/{}/address/shipping'.format(estimate_id), 'PUT', json_data)
    def update_sorder(self, order_id, json_data):
        return self._standard_call('salesorders/{}'.format(order_id),'PUT',json_data)
    def update_sorder_billing(self, order_id, json_data):####
        return self._standard_call('salesorders/{}/address/billing'.format(order_id), 'PUT', json_data)
    def update_sorder_shipping(self, order_id, json_data):####
        return self._standard_call('salesorders/{}/address/shipping'.format(order_id), 'PUT', json_data)
    def update_invoice(self, invoice_id, json_data):
        return self._standard_call('invoices/:'.format(invoice_id),'PUT',json_data)
    def update_invoice_billing(self, invoice_id, json_data):####
        return self._standard_call('invoices/{:}/address/billing'.format(invoice_id),'PUT',json_data)
    def update_invoice_shipping(self, invoice_id, json_data):####
        return self._standard_call('invoices/{:}/address/shipping'.format(invoice_id),'PUT',json_data)
    def update_credit_note(self, creditnote_id, json_data):
        return self._standard_call('creditnotes/{:}'.format(creditnote_id),'PUT',json_data)
    def update_credit_note_invoice_billing(self, invoice_id, json_data):####
        return self._standard_call('creditnotes/{}/address/billing'.format(creditnote_id),'PUT',json_data)
    def update_credit_note_shipping(self, invoice_id, json_data):####
        return self._standard_call('creditnotes/{}/address/shipping'.format(creditnote_id),'PUT',json_data)
    def update_credit_note_refund(self, invoice_id, creditnote_refund_id, json_data):####
        return self._standard_call('creditnotes/:/refunds/:'.format(creditnote_id,creditnote_refund_id),'PUT',json_data)
    def update_customerPayments(self, payment_id, json_data):####
        return self._standard_call('customerpayments/{}'.format(payment_id),'PUT',json_data)
    def update_customerPayments_refund(self, payment_id, refund_id, json_data):####
        return self._standard_call('customerpayments/{}/refunds/:'.format(payment_id,refund_id),'PUT',json_data)
    def update_expenses(self, expense_id, json_data):####
        return self._standard_call('expenses/{}'.format(expense_id),'PUT',json_data)
    def update_porder(self, purchase_order_id, json_data):
        return self._standard_call('purchaseorders/{}'.format(purchase_order_id),'PUT',json_data)
    def update_porder_billing(self, order_id, json_data):####
        return self._standard_call('purchaseorders/{}/address/billing'.format(order_id), 'PUT', json_data)
    def update_porder_shipping(self, order_id, json_data):####
        return self._standard_call('purchaseorders/{}/address/shipping'.format(order_id), 'PUT', json_data)
    def update_bill(self, bill_id, json_data):
        return self._standard_call('bills/{}'.format(bill_id),'PUT',json_data)####
    def update_bill_billing(self, bill_id, json_data):
        return self._standard_call('bills/{}/address/billing'.format(bill_id),'PUT',json_data)####
    def update_vendor_credits(self, vendor_credit_id, json_data):
        return self._standard_call('vendorcredits/{}'.format(vendor_credit_id),'PUT',json_data)####
    def update_vendor_payment(self, payment_id, json_data):
        return self._standard_call('vendorpayments/{}'.format(payment_id),'PUT',json_data)
    def update_item(self, item_id, json_data):
        return self._standard_call('items/{}'.format(item_id),'PUT',json_data)
    def update_package(self, package_id, json_data):
        return self._standard_call('packages/{}'.format(package_id),'PUT',json_data)

    # Delete#
    def delete_contact(self, contact_person_id, address_id):
        return self._standard_call('contacts/{}'.format(contact_person_id),'DELETE')####
    def delete_contact_address(self, contact_person_id, address_id):
        return self._standard_call('contacts/{:}/address/{:}'.format(contact_person_id, address_id),'DELETE')####
    def delete_estimates(self, estimates_id):
        return self._standard_call('estimates/{}'.format(estimates_id),'DELETE')
    def delete_sorder(self, order_id):
        return self._standard_call('salesorders/{}'.format(order_id),'DELETE')
    def delete_invoice(self, invoice_id):
        return self._standard_call('invoices/{}'.format(invoice_id),'DELETE')
    def delete_invoicePayment(self, invoice_id, invoice_payment_id):
        return self._standard_call('invoices/{:}/payments/{:}'.format(invoice_id, invoice_payment_id),'DELETE')####
    def delete_applied_credit(self, invoice_id, creditnotes_invoice_id):
        return self._standard_call('invoices/{:}/creditsapplied/{:}'.format(invoice_id, creditnotes_invoice_id),'DELETE')####
    def delete_creditNote(self, creditnote_id):
        return self._standard_call('creditnotes/{}'.format(creditnote_id),'DELETE')####
    def delete_creditNote_refund(self, creditnote_id,creditnote_refund_id):
        return self._standard_call('creditnotes/{}/refunds/{}'.format(creditnote_id,creditnote_refund_id),'DELETE')#####
    def delete_customerPayments(self, customerpayments_id):
        return self._standard_call('customerpayments/{}'.format(customerpayments_id),'DELETE')
    def delete_expenses(self, expense_id):
        return self._standard_call('expenses/{}'.format(expense_id), 'DELETE')#####
    def delete_porder(self, order_id):
        return self._standard_call('purchaseorders/{}'.format(order_id),'DELETE')
    def delete_bill(self, bill_id):
        return self._standard_call('bills/{}'.format(bill_id),'DELETE')########
    def delete_bills_vendorCredits(self, vendor_credit_id,vendor_credit_bill_id):
        return self._standard_call('bills/{}'.format(vendor_credit_id,vendor_credit_bill_id),'DELETE')########
    def delete_bill_payments(self, bill_id,bill_payment_id):
        return self._standard_call('bills/{}/payments/{}'.format(bill_id,bill_payment_id),'DELETE')########
    def delete_vendorPayment(self, payment_id):
        return self._standard_call('vendorpayments/{}'.format(payment_id),'DELETE')########
    def delete_items(self, item_id):
        return self._standard_call('items/{}'.format(item_id),'DELETE')
    def delete_shipment(self, shipment_id):
        return self._standard_call('shipmentorders/{}'.format(shipment_id),'DELETE')
    def delete_package(self, package_id):
        return self._standard_call('packages/{}'.format(package_id),'DELETE')

    # List#
    def list_contacts(self, **kwargs):
        return self._standard_call('contacts', 'GET', **kwargs)
    def list_estimates(self, **kwargs):####
        return self._standard_call('estimates', 'GET', **kwargs)
    def list_credit_notes(self, **kwargs):####
        return self._standard_call('creditnotes', 'GET', **kwargs)
    def list_credit_note_refunds(self, **kwargs):####
        return self._standard_call('creditnotes/refunds', 'GET', **kwargs)
    def list_customer_payments(self, **kwargs):####
        return self._standard_call('customerpayments', 'GET', **kwargs)
    def list_expenses(self, **kwargs):####
        return self._standard_call('expenses', 'GET', **kwargs)
    def list_employees(self, **kwargs):####
        return self._standard_call('employees', 'GET', **kwargs)
    def list_bills(self, **kwargs):####
        return self._standard_call('bills', 'GET', **kwargs)
    def list_vendor_credits(self, **kwargs):####
        return self._standard_call('vendorcredits', 'GET', **kwargs)
    def list_vendor_payments(self, **kwargs):####
        return self._standard_call('vendorpayments', 'GET', **kwargs)
    def list_users(self, **kwargs):####
        return self._standard_call('users', 'GET', **kwargs)
    def list_items(self, **kwargs):####
        return self._standard_call('items', 'GET', **kwargs)
    def list_sorders(self,**kwargs):
        return self._standard_call('salesorders','GET', **kwargs)
    def list_porders(self, **kwargs):
        return self._standard_call('purchaseorders','GET', **kwargs)
    def list_packages(self, **kwargs):
        return self._standard_call('packages','GET', **kwargs)
    def list_all_pricebooks_id(self, **kwargs):
        return self._standard_call('pricebooks','GET', **kwargs)
    def list_invoices(self, **kwargs):
        return self._standard_call('invoices', 'GET', **kwargs)

    # Get#
    def get_contact(self, contact_id):
        return self._standard_call('contacts/{}'.format(contact_id),'GET')
    def get_estimate(self, estimate_id):
        return self._standard_call('estimates/{}'.format(estimate_id), 'GET')####
    def get_sorder(self, order_id):
        return self._standard_call('salesorders/{}'.format(order_id),'GET')
    def get_invoice(self, invoice_id):
        return self._standard_call('invoices/{}'.format(invoice_id),'GET')
    def get_credit_note(self, creditnote_id):
        return self._standard_call('creditnotes/{}'.format(creditnote_id),'GET')####
    def get_customer_payment(self, customerpayments_id):
        return self._standard_call('customerpayments/{}'.format(customerpayments_id),'GET')####
    def get_expense(self, expense_id):
        return self._standard_call('expenses/{}'.format(expense_id),'GET')####
    def get_employee(self, employees_id):
        return self._standard_call('employees/{}'.format(employees_id),'GET')####
    def get_porder(self, order_id):
        return self._standard_call('purchaseorders/{}'.format(order_id),'GET')
    def get_bill(self, bills_id):
        return self._standard_call('bills/{}'.format(bills_id),'GET')
    def get_bill_payments(self, bills_id):
        return self._standard_call('bills/{}/payments'.format(bills_id),'GET')
    def get_vendor_credit(self, vendor_credit_id):
        return self._standard_call('vendorcredits/{}'.format(vendor_credit_id),'GET')####
    def get_vendor_payment(self, payment_id):
        return self._standard_call('vendorpayments/{}'.format(payment_id),'GET')####
    def get_user(self, user_id):
        return self._standard_call('users/:'.format(user_id),'GET')####
    def get_item(self, item_id):
        return self._standard_call('items/{}'.format(item_id),'GET')
    def get_contact_address(self, contact_id):
        return self._standard_call('contacts/{}/address'.format(contact_id),'GET')####
    def get_package(self, package_id):
        return self._standard_call('packages/{}'.format(package_id),'GET')
    def get_shipment(self, shipment_id):
        return self._standard_call('shipmentorders/{}'.format(shipment_id),'POST')
    def get_pricebook(self,pricebook_id):
            return self._standard_call('pricebooks/{}'.format(pricebook_id),'GET')

        # Mark As#
    def mark_contact_as_active(self, contact_id):####
        return self._standard_call('contacts/{}/active'.format(contact_id),'POST')
    def mark_contact_as_inactive(self, contact_id):####
        return self._standard_call('contacts/{}/inactive'.format(contact_id),'POST')
    def mark_estimate_as_sent(self, estimate_id):####
        return self._standard_call('estimates/{:}/status/sent'.format(contact_id),'POST')
    def mark_estimate_as_accepted(self, estimate_id):####
        return self._standard_call('estimates/{:}/status/accepted'.format(contact_id),'POST')
    def mark_estimate_as_declined(self, estimate_id):####
        return self._standard_call('estimates/{:}/status/declined'.format(contact_id),'POST')
    def mark_sorder_as_open(self, salesorder_id):####
        return self._standard_call('salesorders/{:}/status/open'.format(salesorder_id),'POST')
    def mark_sorder_as_voided(self, order_id):####
        return self._standard_call('salesorders/{}/status/void'.format(order_id),'POST')
    def mark_invoice_as_sent(self, invoice_id):####
        return self._standard_call('invoices/:/status/sent'.format(order_id),'POST')
    def mark_invoice_as_void(self, invoice_id):####
        return self._standard_call('invoices/:/status/void'.format(order_id),'POST')
    def mark_invoice_as_draft(self, invoice_id):####
        return self._standard_call('invoices/:/status/draft'.format(order_id),'POST')
    def mark_credit_note_as_void(self, creditnote_id):####
        return self._standard_call('creditnotes/{}/status/void'.format(creditnote_id),'POST')
    def mark_credit_note_as_draft(self, creditnote_id):####
        return self._standard_call('creditnotes/{}/status/draft'.format(creditnote_id),'POST')
    def mark_credit_note_as_open(self, creditnote_id):####
        return self._standard_call('creditnotes/{}/status/open'.format(creditnote_id),'POST')
    def mark_porder_as_open(self, purchaseorder_id):####
        return self._standard_call('purchaseorders/{}/status/open'.format(purchaseorder_id),'POST')
    def mark_porder_as_billed(self, purchaseorder_id):####
        return self._standard_call('purchaseorders/{}/status/billed'.format(purchaseorder_id),'POST')
    def mark_porder_as_cancelled(self, purchaseorder_id):####
        return self._standard_call('purchaseorders/{}/status/cancelled'.format(purchaseorder_id),'POST')
    def mark_bill_as_void(self, purchaseorder_id):####
        return self._standard_call('bills/{}/status/void'.format(purchaseorder_id),'POST')
    def mark_bill_as_open(self, purchaseorder_id):####
        return self._standard_call('bills/{}/status/open'.format(purchaseorder_id),'POST')
    def mark_shipment_as_delivered(self, shipment_id):
        return self._standard_call('shipmentorders/{}/status/delivered'.format(shipment_id),'POST')
    def mark_item_as_inactive(self, item_id):
        return self._standard_call('items/{}/inactive'.format(item_id),'POST')
    def mark_item_as_active(self, item_id):####
        return self._standard_call('items/{}/active'.format(item_id),'POST')
    def sent_statements(self,contact_id,json_data):
        return self._standard_call('contacts/{}/statements/email'.format(contact_id),'POST',json_data)
    def sent_invoice(self,invoice_id,json_data):
        return self._standard_call('invoices/{}/email'.format(invoice_id),'POST',json_data)

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
        self.payload = self.endpoint + self.module
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def get_pricebooks(self, pricebook_id):
        self.module = 'pricebooks/' + pricebook_id
        self.payload = self.endpoint + self.module
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
    def update_item(self, item_id, json_data):
        self.module = 'items/' + item_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
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
    def get_sorder(self, order_id):
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
    def create_order(self, json_data, autogen=True):
        self.module = 'salesorders'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
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
        self.data = json.dumps(json_data)
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
    def create_invoice(self, json_data):
        self.module = 'invoices'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def create_inventory_adjustment(self, json_data):
        self.module = 'inventoryadjustments'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def mark_shipment_as_delivered(self, shipment_id):
        self.module = 'shipmentorders/' + shipment_id + '/status/delivered'
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.post(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def create_cxpayment(self, json_data):
        self.module = 'customerpayments'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
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
    def update_bill(self, bill_id, json_data):
        self.module = 'bills/' + bill_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
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
    def item_adjustment(self,json_data):
        self.module = 'inventoryadjustments'
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.post(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def update_contact(self, contact_id, json_data):
        self.module = 'contacts/' + str(contact_id)
        self.payload = self.endpoint + self.module + self.authtoken
        self.data = json.dumps(json_data)
        self.params = {'JSONString': self.data}
        self.request = requests.put(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def list_so(self, salesorder_number):
        self.module = 'salesorders'
        self.payload = self.endpoint + self.module + self.authtoken
        self.params = {'salesorder_number': salesorder_number}
        self.request = requests.get(url=self.payload, headers=self.headers, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def retrieve_order(self, order_id):
        self.module = 'salesorders/' + order_id
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def retrieve_packages(self, package_id):
        self.module = 'packages/' + str(package_id)
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def get_invoices_filtro(self, status):
        self.module = 'invoices?&filter_by_=' + str(package_id)
        self.payload = self.endpoint + self.module + self.authtoken
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
