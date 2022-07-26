import json
import requests
class MMM:
	def __init__(self, shop_key):
		self.endpoint = 'https://3m.mirakl.net/api/'
		self.head = {
			'Content-Type': 'application/json',
			'authorization': shop_key,
			'Accept': 'application/json'}
	def _standard_call(self, module, call_type, file = None,data = None, **kwargs):
		self.module = module
		self.payload = self.endpoint + self.module
		additional_args = locals()['kwargs']
		if len(additional_args) == 0:
			if data == None:
				self.params = None
			else:
				self.params = {'JSONString': data}
		else:
			if data == None:
				self.params = {}
			else:
				self.params = {'JSONString': data}
			keys = []
			extra_param = {}
		for i in kwargs:
			keys.append(i)
			extra_param = {i: additional_args[i]}
			self.params.update(extra_param)
		if call_type == 'GET':
						self.request = requests.get(url=self.payload, headers=self.head, json=file, params=self.params).text
		elif call_type == 'POST':
						self.request = requests.post(url=self.payload, headers=self.head,json=file, params=self.params).text
		elif call_type == 'PUT':
						self.request = requests.put(url=self.payload, headers=self.head, json=file, params=self.params).text
		elif call_type == 'DELETE':
						self.request = requests.delete(url=self.payload, headers=self.head, json=file, params=self.params).text
		try:
			self.r = json.loads(self.request)
			return self.r
		except:
			return self.request 
												
	def list_orders(self,**kwargs):
		return self._standard_call('orders','GET',**kwargs) 