import requests
import json
import boto3

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
        'x-auth-client':"foiciztdz4mptpgy83rj08brrphomb2",}

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

    def get_all_category(self,page):
        self.module = 'catalog/categories'
        self.payload = self.endpoint1 + self.module 
        self.params = {'page': int(page), 'limit' : 200}
        self.request = requests.get(url=self.payload, headers=self.headers1, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def get_order_product(self,order_id):
        self.module = 'orders/' +str(order_id) + '/products'
        self.payload = self.endpoint + self.module 
        self.request = requests.get(url=self.payload, headers=self.headers)
        self.r = json.loads(self.request.text)
        return self.r
    def get_order_coupons(self,order_id):
        self.module = 'orders/' + str(order_id) + '/coupons'
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
    def shipmentsadreess(self,order_id):
        self.module = 'orders/' +str(order_id) + '/shippingaddresses'
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
    def update_status(self,product_id,json_data):
        self.module = 'orders/' + str(product_id)
        self.payload = self.endpoint + self.module 
        self.data = json_data
        self.request = requests.put(url=self.payload, headers=self.headers1,data=self.data)
        self.r = json.loads(self.request.text)
        return self.r
    def get_option_sets(self):
        self.module = 'option_sets'
        self.payload = self.endpoint + self.module 
        self.request = requests.get(url=self.payload, headers=self.headers1)
        self.r = json.loads(self.request.text)
        return self.r 
    def get_List_Product_Options(self,product_id) :
        self.module = 'products/' + str(product_id) + '/options'
        self.payload = self.endpoint + self.module 
        self.request = requests.get(url=self.payload, headers=self.headers1)
        self.r = json.loads(self.request.text)
        return self.r
    def get_variants(self,product_id) :
        self.module = 'catalog/products/' + str(product_id) + '/variants'
        self.payload = self.endpoint1 + self.module 
        self.request = requests.get(url=self.payload, headers=self.headers1)
        self.r = json.loads(self.request.text)
        return self.r 
    def update_Option_Set(self,Set_id,json_data):
        self.module = 'option_sets/' + str(Set_id)
        self.payload = self.endpoint + self.module 
        self.data = json_data
        self.request = requests.put(url=self.payload, headers=self.headers1,data=self.data)
        self.r = json.loads(self.request.text)
        return self.r
    def Updates_Option_Set(self,product_id ,json_data):
        self.module = 'products/'+str(product_id)
        self.payload = self.endpoint +self.module 
        self.data = json_data
        self.request = requests.put(url=self.payload, headers=self.headers1, data=self.data)
        self.r = json.loads(self.request.text)
        return self.r
    def get_products_option_set_id(self,option_set_id,page):
        self.module = '/catalog/products' 
        self.payload = self.endpoint + self.module 
        self.params = {'option_set_id':int(option_set_id), 'page': int(page)}
        self.request = requests.get(url=self.payload, headers=self.headers1, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r
    def get_an_Option_Set(self,Option_Set_id):
        self.module = 'option_sets/' + str(Option_Set_id)
        self.payload = self.endpoint + self.module 
        self.request = requests.get(url=self.payload, headers=self.headers1)
        self.r = json.loads(self.request.text)
        return self.r 
        
    def get_item_list(self,page):
        self.module = 'catalog/products'
        self.payload = self.endpoint1 + self.module 
        self.params = {'page': int(page),'limit' : 200}
        self.request = requests.get(url=self.payload, headers=self.headers1 ,params=self.params)
        self.r = json.loads(self.request.text)
        return self.r 

    def get_customers(self,page):
        self.module = 'customers'
        self.payload = self.endpoint + self.module
        self.params = {'page': int(page), 'limit' : 200}
        self.request = requests.get(url=self.payload, headers=self.headers1 ,params=self.params)
        self.r = json.loads(self.request.text)
        return self.r 

    def get_customer_id(self,customer_id):
        self.module = 'customers/' + str(customer_id)
        self.payload = self.endpoint + self.module
        self.request = requests.get(url=self.payload, headers=self.headers1)
        self.r = json.loads(self.request.text)
        return self.r 
    def get_brands(self,page):
        self.module = 'catalog/brands'
        self.payload = self.endpoint1 + self.module
        self.params = {'page': int(page)}
        self.request = requests.get(url=self.payload, headers=self.headers1 , params=self.params)
        self.r = json.loads(self.request.text)
        return self.r 

    def get_shipping_addresses(self,order_id):
        self.module = 'orders/' + str(order_id) + '/shipping_addresses'
        self.payload = self.endpoint + self.module
        self.request = requests.get(url=self.payload, headers=self.headers1)
        self.r = json.loads(self.request.text)
        return self.r 

    def serch_orders(self,modulo,last_isp1):
        k = 50
        isp_orders = []
        while k == 50:
            r = modulo.get_orders_mid_id(int(last_isp1))
            k = len(r)
            isp_orders.extend(r)
            k = len(r)
            if len(r) == 50:
                last_isp1 = r[49]['id']
            last_isp = isp_orders[-1]['id']
        return last_isp, isp_orders  

    def get_customer_list(self,page):
        self.module = 'customers/addresses'
        self.payload = self.endpoint1 + self.modules
        self.params = {'page': int(page),'limit' : 200}
        self.request = requests.get(url=self.payload, headers=self.headers1,params=self.params)
        self.r = json.loads(self.request.text)
        return self.r

    def get_orders_status(self,page,status_id=None,max_date_created=None,min_date_created=None):
        self.module = 'orders' 
        self.payload = self.endpoint + self.module 
        self.params = {'status_id':status_id, 'page': int(page), 'max_date_created' : max_date_created,'min_date_created' : min_date_created ,'limit' : 200}
        self.request = requests.get(url=self.payload, headers=self.headers1, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r

    def get_customer_email(self,email):
        self.module = 'customers' 
        self.payload = self.endpoint + self.module 
        self.params = {'email':email,}
        self.request = requests.get(url=self.payload, headers=self.headers1, params=self.params)
        self.r = json.loads(self.request.text)
        return self.r

    def update_product(self,product_id,json_data):
        self.module = 'catalog/products/' + str(product_id)
        self.payload = self.endpoint1 + self.module 
        self.data = json_data
        self.request = requests.put(url=self.payload, headers=self.headers1,data=self.data)
        self.r = json.loads(self.request.text)
        return self.r

    def get_product_metafields(self,product_id):
        self.module = 'catalog/products/' + str(product_id) + '/metafields'
        self.payload = self.endpoint1 + self.module
        self.request = requests.get(url=self.payload, headers=self.headers1)
        self.r = json.loads(self.request.text)
        return self.r 

    def update_product_metafields(self,product_id,metafield_id,json_data):
        self.module = 'catalog/products/' + str(product_id)+'/metafields/' + str(metafield_id)
        self.payload = self.endpoint1 + self.module 
        self.data = json_data
        self.request = requests.put(url=self.payload, headers=self.headers1,data=self.data)
        self.r = json.loads(self.request.text)
        return self.r

    def update_product_variants(self,product_id,variant_id,json_data):
        self.module = 'catalog/products/' + str(product_id)+'/variants/' + str(variant_id)
        self.payload = self.endpoint1 + self.module 
        self.data = json_data
        self.request = requests.put(url=self.payload, headers=self.headers1,data=self.data)
        self.r = json.loads(self.request.text)
        return self.r

    def get_payments_order_id(self,order_id):
        self.module = 'payments/methods/'
        self.payload = self.endpoint1 + self.module
        self.params = {'order_id':order_id,}
        self.request = requests.get(url=self.payload, headers=self.headers1,params=self.params)
        self.r = json.loads(self.request.text)
        return self.r 

    def get_transactions_order_id(self,order_id):
        self.module = 'orders/' + str(order_id) + '/transactions'
        self.payload = self.endpoint1 + self.module
        self.request = requests.get(url=self.payload, headers=self.headers1)
        self.r = json.loads(self.request.text)
        return self.r

    def created_product(self,json_data,include_fields):
        self.module = 'catalog/products?include_fields=' + str(include_fields)
        self.payload = self.endpoint1 + self.module 
        self.data = json_data
        self.request = requests.post(url=self.payload, headers=self.headers1,data=self.data)
        self.r = json.loads(self.request.text)
        return self.r


    def created_cart(self,json_data):
        self.module = 'carts'
        self.payload = self.endpoint1 + self.module 
        self.data = json_data
        self.request = requests.post(url=self.payload, headers=self.headers1,data=self.data)
        self.r = json.loads(self.request.text)
        return self.r

    def get_cartId(self,cartId):
        self.module = 'carts/' +str(cartId)
        self.payload = self.endpoint1 + self.module
        self.request = requests.get(url=self.payload, headers=self.headers1,)
        self.r = json.loads(self.request.text)
        return self.r

    def get_cartId_url(self,cartId):
        self.module = 'carts/'+str(cartId)+'/redirect_urls'
        self.payload = self.endpoint1 + self.module 
        self.request = requests.post(url=self.payload, headers=self.headers1)
        self.r = json.loads(self.request.text)
        return self.r
        

class bcisp:  
    def __init__(self):
            self.endpoint = 'https://api.bigcommerce.com/stores/e163lt99'
            self.headers = {'accept': "application/json",
            'content-type': "application/json",
            'x-auth-token': "i9iraumus6c3zpa8a3pqz9le1fgv245",
            'x-auth-client':"foiciztdz4mptpgy83rj08brrphomb2",} 

    def _standard_call(self, module, call_type, cpl,data=None, date_filter=None, **kwargs):
        self.module = module
        if date_filter == None:
            self.payload = self.endpoint + str(cpl) + self.module
        else:
            self.payload = self.endpoint + str(cpl) + self.module + '?' + date_filter
        additional_args = locals()['kwargs']

        if len(additional_args) == 0:
            self.params = None
            self.data = data
        else:
            self.data = data
            self.params = {}
            
            keys = []
            extra_param = {}
            for i in kwargs:
                keys.append(i)
                extra_param = {i: additional_args[i]}
                self.params.update(extra_param)
        if call_type == 'GET':
            self.request = requests.get(url=self.payload, headers=self.headers, params=self.params,data=self.data).text
        elif call_type == 'POST':
            self.request = requests.post(url=self.payload, headers=self.headers, params=self.params,data=self.data).text
        elif call_type == 'PUT':
            self.request = requests.put(url=self.payload, headers=self.headers, params=self.params,data=self.data).text
        elif call_type == 'DELETE':
            self.request = requests.delete(url=self.payload, headers=self.headers, params=self.params,data=self.data).text
        self.r = json.loads(self.request)
        return self.r

    def list_orders(self,**kwargs):
        return self._standard_call('orders','GET','/v2/',**kwargs)
    def list_products(self,**kwargs):
        return self._standard_call('catalog/products','GET','/v3/',**kwargs)
        
    def get_orders_refunds(self,order_id):
        return self._standard_call('orders/{}/payment_actions/refunds'.format(order_id),'GET','/v3/')
    def get_orders_transactionss(self,order_id):
        return self._standard_call('orders/{}/transactions'.format(order_id),'GET','/v3/')
    def get_orders_products(self,order_id):
        return self._standard_call('orders/{}/products'.format(order_id),'GET','/v2/')

    def update_variants(self,product_id,variant_id,data,**kwargs):
        return self._standard_call('catalog/products/'+str(product_id)+'/variants/'+str(variant_id),'PUT','/v3/',data,**kwargs)
    def update_product(self,product_id,data):
        return self._standard_call('catalog/products/'+str(product_id),'PUT','/v3/',data)
    def update_custom_fieldst(self,product_id,custom_field_id,data):
        return self._standard_call('catalog/products/{}/custom-fields/{}'.format(product_id,custom_field_id),'PUT','/v3/',data)
  
