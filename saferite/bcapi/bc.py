import requests
import json
import boto3

class bcapi:  
    def __init__(self,cod_store):
        if cod_store.upper()=='ISP':
            self.endpoint = 'https://api.bigcommerce.com/stores/e163lt99'
            self.headers = {'accept': "application/json",
            'content-type': "application/json",
            'x-auth-token': "i9iraumus6c3zpa8a3pqz9le1fgv245",
            'x-auth-client':"foiciztdz4mptpgy83rj08brrphomb2",}
        elif cod_store.upper()=='SS':
            self.endpoint = 'https://api.bigcommerce.com/stores/4yhayto7'
            self.headers = {'accept': "application/json",
            'content-type': "application/json",
            'x-auth-token': "9tmmhy9nw1rl20ljv6kv2jtzfbbyhuq",
            'x-auth-client': "m3u7la2n6igltyoydefn4z67phv87zj",}  
        elif cod_store.upper()=='FL':
            self.endpoint = 'https://api.bigcommerce.com/stores/rgulxx84tf'
            self.headers = {'accept': "application/json",
            'content-type': "application/json",
            'x-auth-token': "93kbq8p4s5djcdxtlkccexk3xzjah68"
            } 
        elif cod_store.upper()=='N95':
            self.endpoint = 'https://api.bigcommerce.com/stores/b7e0lck4gj'
            self.headers = {'accept': "application/json",
            'content-type': "application/json",
            'x-auth-token': "6ftx690qpv5j3tgyuzrx5shpo8qke7a"
            }
        elif cod_store.upper()=='TEST':
            self.endpoint = 'https://api.bigcommerce.com/stores/zqimewefx0'
            self.headers = {'Accept': "application/json",
            'Content-Type': "application/json",
            'X-Auth-Token': "qkybqhtavtqh2z0jj4qh86ezqiqq77b"
            }          


    def _standard_call(self, module, call_type, cpl,data=None,json_data=None, date_filter = None, **kwargs):
        self.module = module
        self.json_data = json_data
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
            self.request = requests.post(url=self.payload, headers=self.headers, params=self.params,data=self.data,json=self.json_data).text
        elif call_type == 'PUT':
            self.request = requests.put(url=self.payload, headers=self.headers, params=self.params,data=self.data,json=self.json_data).text
        elif call_type == 'DELETE':
            self.request = requests.delete(url=self.payload, headers=self.headers, params=self.params,data=self.data).text
        try:    
                self.r = json.loads(self.request)
        except:
                self.r = self.request      
        return self.r

    def create_customers(self,json_data):
        return self._standard_call('customers','POST','/v3/',json_data) 

    def create_customers_addresses(self,json_data):
        return self._standard_call('customers/addresses','POST','/v3/',json_data)  

    def create_custom_fields(self,product_id,json_data) :
        return self._standard_call('catalog/products/{}/custom-fields'.format(product_id),'POST','/v3/',json_data) 

    def create_order(self, data):
        return  self._standard_call('orders','POST','/v2/', data)

    def create_shipment(self,order_id,data):
        return self._standard_call(f'orders/{order_id}/shipments','POST','/v2/',json_data=data)

        
    def delete_custom_fields(self,product_id,custom_field_id):
        return self._standard_call('catalog/products/{}/custom-fields/{}'.format(product_id,custom_field_id),'DELETE','/v3/') 


    def get_customer(self,customer_id): #bulk-pricing-rules
        return self._standard_call('customers/{}'.format(customer_id),'GET','/v2/')  
    def get_customers(self,**kwar): #bulk-pricing-rules
        return self._standard_call('customers','GET','/v2/',**kwar)      
    def get_categories(self,category_id,**kwar): #bulk-pricing-rules
        return self._standard_call('catalog/categories/{}'.format(category_id),'GET','/v3/',**kwar)     
    def get_bpr(self,product_id): #bulk-pricing-rules
        return self._standard_call('catalog/products/{}/bulk-pricing-rules'.format(product_id),'GET','/v3/')
    def get_metafields(self,category_id): #bulk-pricing-rules
        return self._standard_call('catalog/categories/{}/metafields'.format(category_id),'GET','/v3/') 
    def get_modifiers_products(self,product_id):
        return self._standard_call('catalog/products/{}/modifiers'.format(product_id),'GET','/v3/')  
    def get_options_products(self,product_id):
        return self._standard_call('catalog/products/{}/options'.format(product_id),'GET','/v3/')
    def get_order(self,order_id):
         return self._standard_call('orders/{}'.format(order_id),'GET','/v2/')
    def get_order_coupons(self,order_id):
         return self._standard_call('orders/{}/coupons'.format(order_id),'GET','/v2/')
    def get_orders_products(self,order_id):
        return self._standard_call('orders/{}/products'.format(order_id),'GET','/v2/')
    def get_orders_refunds(self,order_id):
        return self._standard_call('orders/{}/payment_actions/refunds'.format(order_id),'GET','/v3/')
    def get_orders_transactionss(self,order_id):
        return self._standard_call('orders/{}/transactions'.format(order_id),'GET','/v3/')
    def get_orders_taxes(self,order_id):
        return self._standard_call('orders/{}/taxes'.format(order_id),'GET','/v2/')
    def get_product(self,product_id,**kwargs):
         return self._standard_call('catalog/products/{}'.format(product_id),'GET','/v3/',**kwargs) 
    def get_product_custom_fields(self,product_id):
         return self._standard_call('catalog/products/{}/custom-fields'.format(product_id),'GET','/v3/')      
    def get_product_variant(self,product_id,variant_id):
         return self._standard_call('catalog/products/{}/variants/{}'.format(product_id,variant_id),'GET','/v3/')       
    def get_shipmentsadreess(self,order_id):
          return self._standard_call('orders/{}/shippingaddresses'.format(order_id),'GET','/v2/',)
    def get_a_shipmentsadreess(self,order_id,shipping_address_id):
          return self._standard_call('orders/{}/shippingaddresses/{}'.format(order_id,shipping_address_id),'GET','/v2/',)
    def get_shipmentsadreessCustomers(self,customer_id):
          return self._standard_call('customers/{}/addresses'.format(customer_id),'GET','/v2/')          
    def get_shipments(self,order_id):
        return self._standard_call('orders/{}/shipments'.format(order_id),'GET','/v2/')
    def list_customers(self,**kwargs):
        return self._standard_call('customers','GET','/v3/',**kwargs)    

    def list_categories(self,**kwargs):
        return self._standard_call('catalog/categories','GET','/v3/',**kwargs)
    def list_customers(self,**kwargs):
      return self._standard_call('customers','GET','/v3/',**kwargs)    
    def list_orders(self,**kwargs):####
        return self._standard_call('orders','GET','/v2/',**kwargs)
    def list_products(self,**kwargs):
        return self._standard_call('catalog/products','GET','/v3/',**kwargs)
    def list_refunds(self,**kwargs):
        return self._standard_call('orders/payment_actions/refunds','GET','/v3/',**kwargs)
    def list_brands(self,**kwargs):
        return self._standard_call('catalog/brands','GET','/v3/',**kwargs)

    def update_custom_fields(self,product_id,custom_field_id,data):
        return self._standard_call('catalog/products/{}/custom-fields/{}'.format(product_id,custom_field_id),'PUT','/v3/',data)
    def update_orders(self,order_id,json_data):
        return self._standard_call('orders/{}'.format(order_id),'PUT','/v2/',json_data=json_data)
    def update_product(self,product_id,data):
        return self._standard_call('catalog/products/'+str(product_id),'PUT','/v3/',data)
    def update_status(self,order_id,json_data):
          return self._standard_call('orders/{}'.format(order_id),'PUT','/v2/',json_data)
    def update_variants(self,product_id,variant_id,data,**kwargs):
        return self._standard_call('catalog/products/'+str(product_id)+'/variants/'+str(variant_id),'PUT','/v3/',data,**kwargs)
    def update_customers(self,customer_id,json_data):
        return self._standard_call('customers/{}'.format(customer_id),'PUT','/v2/',json_data) 


    def delete_order_shipments(self,order_id):
        return self._standard_call(f'orders/{order_id}/shipments','DELETE','/v2/')

    def delete_order_shipment(self,order_id,shipment_id):
        return self._standard_call(f'orders/{order_id}/shipments/{shipment_id}','DELETE','/v2/')     

    def delete_customers(self,**kwargs):
        return self._standard_call('customers','DELETE','/v3/',**kwargs) 

    def while_for_len(self,fuction,debug = False,**kwargs):
        """
        Siempre debe llevar el campo limit en 250
        """
        k = 250
        page = 1
        data_full = []
        while  k == 250:
            data = fuction(page=page, **kwargs)
            k = len(data)
            #print(k)
            page += 1
            data_full+=data
        if debug:    
            data_full = pd.json_normalize(data_full)    
        return data_full  




    def while_for_pages(self,fuction,**kwargs):
        page = 1
        pages = 1
        data_full = []
        while page <= pages:
            data = fuction(page=page,**kwargs)
            #print(page)
            page += 1
            pages = int(data['meta']['pagination']['total_pages'])
            data_full += data['data']
        #data_full = pd.json_normalize(data_full)    
        return data_full 
            
      
    