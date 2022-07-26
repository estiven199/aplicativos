import json
import numpy as np
import pandas as pd
from zohoapi import zohoapi
from Information import inf
from dateutil import parser
from pandas.io.json import json_normalize

class for_feed():
	aws = zohoapi.get_aws_token()
	zoho_token = zohoapi.get_s3_file(aws['AWS_KEY'],aws['SECRET_KEY'], 'zoho_token.json')
	z = zohoapi.BooksZohoApi(zoho_token['BOOKS_KEY']) 
	t = inf.information()
	def __init__(self):
		 pass
	def close_file(self,feed_url,new):
		with open(feed_url, 'w') as file:
			json.dump(new, file)
		file.close
	def search_orders_bcisp(self,feed_url,b,string,var=None,var1=None,noid=None,validate=False):
		isp_orders = []
		dfpromo = pd. DataFrame(columns=())
		d_f = pd.DataFrame(columns=())
		col = {}
		with open(feed_url) as file:
			file_isp = json.load(file)
		file.close
		last_isp1 = int(file_isp[string])+int(1)
		k = 50
		while k == 50:
			try:
			    r = b.get_orders_mid_id(int(last_isp1))
			    k = len(r)
			    isp_orders.extend(r)
			    if len(r) == 50:
			        last_isp1 = r[49]['id']
			    last_isp = isp_orders[-1]['id']
			except:
				break    
		isp_orders = json_normalize(isp_orders)
		isp_orders.drop_duplicates('id',keep = 'last', inplace = True)
		isp_orders = isp_orders.loc[~isp_orders['status_id'].isin([0])]
		isp_orders.reset_index   

		if validate == True:    
			for i in isp_orders['id']:
				r1 = b.get_order_product(i)
				r2 = b.get_order(i)
				inf_order = json_normalize(r2)
				r3 = b.get_order_coupons(i)
				if r3.status_code == 200: # se valioda si tiene cupones
			 		promo = json.loads(r3.text)
			 		data_promo = json_normalize(promo)
			 		dfpromo = dfpromo.append(data_promo)

				for k in var1:
					try:
						col[k] = inf_order[k][0]
					except:
						col[k] = 0


				for j in range(len(r1)):
					try:
						r1[j]['product_options'][0]['id']
						for t in range(len(r1[j]['product_options'])):
							del r1[j]['product_options'][t]['id']

						data = json_normalize(r1[j],'product_options',['order_id','product_id','base_total','sku','quantity','base_price','id'])
						for h in range(4):
							for k in var:
								try:
									col[k+str(h)] = data[k][h]
								except:
									col[k+str(h)] = 0
					except:
						data1 = json_normalize(r1[j])
						for h in range(4):
					 		for k in var:
					 			try:
					 				col[k+str(h)] = data1[k][h]
				 				except:
					 				col[k+str(h)] = 0

					df = pd.DataFrame([col])
					d_f = d_f.append(df)
				 
			d_f.columns = d_f.columns.str.replace('_x','')
			d_f.head() 
			d_f.reset_index(inplace = True)
			d_f = self.t.deleted_columns(d_f)
			d_f = d_f.rename(columns = {'product_id0' :'product_id','base_total0':'base_total','base_price0':'base_price','quantity0':'quantity'})#,'id0':'order_product_id'})
			d_f.reset_index(inplace = True)


			for i in range (len(d_f)): 
			    for j in range(4):
			        if int(d_f['option_id'+str(j)][i]) not in noid:# si identifica que no esta en el NOID.
			            pass
			        else:# se identifica los option id de cada item que no hacen parte directa y se le pone 0
			            d_f.loc[i,'product_option_id'+ str(j)] = str(0) 
			            d_f.loc[i,'display_value'+ str(j)] = str(0) 
			            d_f.loc[i,'value'+ str(j)] = str(0)
			            
			d_f = d_f.astype(str)
			d_f['qtzoho'] = 0

			return d_f,dfpromo,last_isp,isp_orders
		else:
			return isp_orders,last_isp
	def crear_listas_vacias(self,data):
	    lists = {}
	    columns = list(data)
	    for i in columns:
	        lists[i] = []
	    return lists
	def inf_promo_order_bcisp(self,dfpromo,vart,df):
		try:
			dfpromo.reset_index(inplace = True)
		except:
			pass	
		
		lists = self.crear_listas_vacias(df)
		if len(dfpromo) != 0:
			for j in range(len(dfpromo)):
				for h in list(df):
					if h =='id':
						lists[h].append(str(dfpromo['order_id'][j]))
					elif h =='qtzoho': 
						lists[h].append(1)
					elif h =='base_price': 
						lists[h].append(-int(dfpromo['amount'][j])) 
					elif h =='product_id': 
						lists[h].append('1') 
					elif h =='SKU_Big_Commerce': 
						lists[h].append(dfpromo['code'][j])
					elif h not in vart:
						lists[h].append('0')
					else:
						filte = df.loc[df['id'].isin([str(dfpromo['order_id'][j])])]
						try:
							filte.reset_index(inplace = True)
						except:
							pass
						data = filte[h][0]
						lists[h].append(data)
			return lists
		else:
			lists = pd.DataFrame(columns = ())

			return lists
	def create_kits_bcisp(self,infbcisp,vart):
		infbcisp = infbcisp.rename(columns = {'id0' :'order_product_id','id1':'id11','id2':'id22','id3':'id33'})
		infbcisp.columns = infbcisp.columns.str.replace('_y','')
		infbcisp.head()
		Kits = infbcisp.loc[infbcisp['KIT'].isin(['1'])]
		Kits.reset_index(inplace = True)
		Kits = self.t.deleted_columns(Kits)
		lists = self.crear_listas_vacias(Kits)
		if len(Kits) > 0 :
			for j in range(len(Kits)):
			    for k in range(int(Kits['QT'][j])):
			        for h in list(Kits):
			        	if h =='id_zoho':
			        		lists[h].append(Kits['id'+str(k)][j])
			        	elif h =='order_product_id':
			        		lists[h].append(Kits['order_product_id'][j])
			        	elif h =='qtzoho': 
			        		lists[h].append(int(Kits['q'+str(k)][j]) * int(Kits['quantity'][j]))
			        	elif h =='base_price': 
			        		lists[h].append((float(Kits['p'+str(k)][j]) * float(Kits['base_total'][j]) / int(Kits['q'+str(k)][j]))/ (int(Kits['quantity'][j]))) 
			        	elif h =='Active': 
			        		lists[h].append(k+1)  
			       		elif h not in vart:
			        		lists[h].append(0)
			        	else:
			        		lists[h].append(Kits[h][j])

			infbcisp['base_price'] = infbcisp['base_price'].astype(float)
			infbcisp['qtzoho'] = np.where((infbcisp['KIT'].astype(int)!=1) & (infbcisp['base_price'] >= 0),infbcisp['quantity'].astype(int)*infbcisp['QT'].astype(int),infbcisp['qtzoho'])
			infbcisp['qtzoho'] = np.where(infbcisp['KIT'].astype(int) == 1, infbcisp['quantity'].astype(int), infbcisp['qtzoho'])
			infbcisp['Active'] = np.where(infbcisp['KIT'].astype(int) == 1, 10, infbcisp['Active'])
			infbcisp['base_price'] = np.where(infbcisp['base_price'] > 0, (infbcisp['base_price'] *infbcisp['quantity'].astype(int))/ infbcisp['qtzoho'].astype(int), infbcisp['base_price'])
			infbcisp['base_price'] = np.where(infbcisp['KIT'].astype(int) == 1, 0, infbcisp['base_price'])  
			infbcisp1 = pd.DataFrame(lists)
			infbcispt = infbcisp.append(infbcisp1)
			infbcispt = infbcispt.sort_values(by = ['id','Active','base_price'], ascending=False)
			infbcispt.reset_index(inplace = True)
			infbcispt = self.t.deleted_columns(infbcispt)
			return infbcispt
		else:

			infbcisp['base_price'] = infbcisp['base_price'].astype(float)
			infbcisp['qtzoho'] = np.where((infbcisp['KIT'].astype(int) != 1) & (infbcisp['base_price'] >= 0 ) , infbcisp['quantity'].astype(int) * infbcisp['QT'].astype(int), infbcisp['qtzoho'])
			infbcisp['qtzoho'] = np.where(infbcisp['KIT'].astype(int) == 1, infbcisp['quantity'].astype(int), infbcisp['qtzoho'])
			infbcisp['Active'] = np.where(infbcisp['KIT'].astype(int) == 1, 10, infbcisp['Active'])
			infbcisp['base_price'] = np.where(infbcisp['base_price'] > 0, (infbcisp['base_price'] *infbcisp['quantity'].astype(int))/ infbcisp['qtzoho'].astype(int) , infbcisp['base_price'])
			infbcisp['base_price'] = np.where(infbcisp['KIT'].astype(int) == 1, 0, infbcisp['base_price'])  
			infbcisp = infbcisp.sort_values(by = ['id','Active','base_price'], ascending=False) 
			infbcisp.reset_index(inplace = True)
			infbcisp = self.t.deleted_columns(infbcisp)

			return infbcisp	
	def update_customer_bcisp(self,infbcisp,b):
		customer_id = infbcisp.loc[infbcisp['customer_id'].isin([0])]
		if len(customer_id) > 0:
			for i in customer_id['id']:
				try:

					r1 = b.get_shipping_addresses(i)

					r = b.get_customer_email(r1[0]['email'])

					infbcisp['customer_id'] = np.where(infbcisp['id']== int(i),int(r[0]['id']),infbcisp['customer_id'])	
				except:
					print(i)
					pass
		return infbcisp
	def replace(self,data,value=" "):
		data.reset_index(inplace = True)
		data = self.t.deleted_columns(data)
		list_columns = list(data)
		list_values = [';','"','  ']
		for i in list_columns:
			for j in list_values:
				data[i] = data[i].astype(str)
				data[i] = data[i].str.replace(j,value)
		return data  
	def json_customer_zoho(self,data_customer,i):


		Contact_data = {
			"contact_name": data_customer['ContactName'][i],
			"company_name": data_customer['company'][i],
			"billing_address": {
			"address": data_customer['billing_address.street_1'][i],
			  "city": data_customer['billing_address.city'][i],
			  "state": data_customer['billing_address.state'][i],
			  "country": data_customer['billing_address.country'][i],
			  "street2" : data_customer['billing_address.street_2'][i],
			   'zip' : str(data_customer['billing_address.zip'][i]),
			}
			  ,

			"shipping_address": {
			 "address": data_customer['street_1'][i],
			   "city": data_customer['city'][i],
			  "state": data_customer['state'][i],
			  "country": data_customer['country'][i],
			   "street2" : data_customer['street_2'][i],
			  'zip' : str(data_customer['zip'][i]),

			   },
			"contact_persons": [
			  {
			   "first_name": str(data_customer['first_name'][i]),
			  "last_name": str(data_customer['last_name'][i]),
			  'email' : str(data_customer['email'][i]),
			  'mobile' : str(data_customer['phone'][i]),
			  'phone' :str(data_customer['phone'][i]),
			  'zip' : str(data_customer['zip'][i])
			  } 
			   ],


			'is_taxable': False,
			'tax_authority_id': '1729377000000085005',
			'tax_exemption_id': '1729377000002313511',
			'tax_authority_name': 'FL State',
			'tax_exemption_code': 'OUT OF STATE',}

		return Contact_data   
	def create_columns(self,var,data,value=0):
	    for i in var:
	        data[i]=value
	    return data
	def date_format(self,date):
	    t = parser.parse(date)
	    t = t.strftime('%Y-%m-%d')
	    return t
	def unique_data(self,data,group,param,sort_values,date):
		data_unique = data.groupby(group, as_index=False).agg(param)
		data_unique[date] = data_unique[date].apply(self.date_format)
		data_unique = data_unique.sort_values(by=sort_values, ascending=False)
		data_unique.reset_index(inplace=True)
		return data_unique
	def update_customer_zoho(self,data,column_tax,colum_custom_zoho_id):
		for i in range(len(data)):
			if float(data[column_tax][i][0:5]) == 0.000:
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

			r = self.z.update_contact(data[colum_custom_zoho_id][i], cx_data)
			print(r['message'])
	def json_orders_zoho(self,i,data1,data2,order):

		if order[0:2] == 'SS':
			template_id = '1729377000028731199'
			Valkue = 'SS'
		else:
			template_id = '1729377000028731259'
			Valkue = 'ISP'
			
		so_items = []
		filtro = data2[data2['id'] == data1['id'][i]]
		filtro.reset_index(inplace=True)
		for s in range (len(filtro)):
			if float(filtro['total_tax'][s][0:5]) == 0.000:
				tax = ''
				adjustment = ''
				adjustment_description = ''
			else:
				tax = 1729377000027355808
				adjustment = float(filtro['base_shipping_cost'][s])*0.07
				adjustment_description = 'Tax Adjustment'
			so_line = {
			'item_id': int(filtro['id_zoho'][s]),
			'rate': filtro['base_price'][s],
			'quantity': int(filtro['qtzoho'][s]),
			'tax_id': tax,}
			so_items.append(so_line)

		so_data = {
		'template_id': template_id,
		'customer_id': int(data1['Zoho Customer ID'][i]),
		'salesorder_number': order,
		'date': data1['date_created'][i],
		'line_items': so_items,
		'shipping_charge': data1['base_shipping_cost'][i],
		'custom_fields': [{'customfield_id': 1729377000039969865, 'value': 'Internet'},
		{'customfield_id': 1729377000040961274, 'value': Valkue}],
		"adjustment" : adjustment,
		"adjustment_description" : adjustment_description,}

		
		return so_data
	def fill_data(self,data_full,data_unique,i,r1,lista,var):
		
		data_full['salesorder_id'] = np.where(data_full['id'] == data_unique['id'][i],
		r1['salesorder']['salesorder_id'],data_full['salesorder_id'])

		for y in range (len(r1['salesorder']['line_items'])):

			data_full['line_item_id'] = np.where((data_full['id'] == data_unique['id'][i]) & 
			(data_full['id_zoho'] == r1['salesorder']['line_items'][y]['item_id']) & (data_full['base_price'] == r1['salesorder']['line_items'][y]['rate']),
			r1['salesorder']['line_items'][y]['line_item_id'],data_full['line_item_id'])

			lista[var[0]].append(r1['salesorder']['salesorder_number'][4:len(r1['salesorder']['salesorder_number'])]) 
			lista[var[1]].append(r1['salesorder']['salesorder_id']) 
			lista[var[2]].append(r1['salesorder']['line_items'][y]['item_id']) 
			lista[var[3]].append(r1['salesorder']['line_items'][y]['line_item_id'])
			lista[var[4]].append(r1['salesorder']['line_items'][y]['quantity']) 
			lista[var[5]].append(r1['salesorder']['customer_id'])
			
		return data_full,lista
	def find_po(self,var,pos):
	    if pos == -1:
	        t = 'NO'
	    else:
	        t = var[pos:pos+9]
	    return t
	def buscar_frontline(self,infbcisp,link):
	    Frontline = infbcisp.loc[infbcisp['brand'].isin(['Frontline'])]
	    Frontline.reset_index(inplace = True)
	    data_full = pd.DataFrame(columns=[])
	    if len(Frontline) > 0:
	        for i in range(len(Frontline['brand'])):
	            
	            data = b.get_customer_id(Frontline['customer_id'][i])
	            data = json_normalize(data)
	            data['order'] = Frontline['id'][i]
	            data['Zoho Customer ID'] = Frontline['Zoho Customer ID'][i]
	            data['id_zoho'] = Frontline['id_zoho'][i]
	            data['preciounitario'] = Frontline['preciounitario'][i]
	            data['sku'] = Frontline['sku'][i]
	            data['qtzoho'] = Frontline['qtzoho'][i]
	            data_full = data_full.append(data)

	    data = pd.read_csv(link)
	    data.fillna('0', inplace=True)       
	    data_full = data.append(data_full)
	    data_full = self.t.deleted_columns(data_full)   
	    data_full.to_csv(link)
	    return data_full  
	def search_orders_bcisp1(self,isp_orders,b,var=None,var1=None,noid=None):
		
		dfpromo = pd. DataFrame(columns=())
		d_f = pd.DataFrame(columns=())
		col = {}

		   
		for i in isp_orders:
			r1 = b.get_order_product(i)
			r2 = b.get_order(i)
			inf_order = json_normalize(r2)
			r3 = b.get_order_coupons(i)
			if r3.status_code == 200: # se valioda si tiene cupones
		 		promo = json.loads(r3.text)
		 		data_promo = json_normalize(promo)
		 		dfpromo = dfpromo.append(data_promo)

			for k in var1:
				try:
					col[k] = inf_order[k][0]
				except:
					col[k] = 0


			for j in range(len(r1)):
				try:
					r1[j]['product_options'][0]['id']
					for t in range(len(r1[j]['product_options'])):
						del r1[j]['product_options'][t]['id']

					data = json_normalize(r1[j],'product_options',['order_id','product_id','base_total','sku','quantity','base_price','id'])
					for h in range(4):
						for k in var:
							try:
								col[k+str(h)] = data[k][h]
							except:
								col[k+str(h)] = 0
				except:
					data1 = json_normalize(r1[j])
					for h in range(4):
				 		for k in var:
				 			try:
				 				col[k+str(h)] = data1[k][h]
			 				except:
				 				col[k+str(h)] = 0

				df = pd.DataFrame([col])
				d_f = d_f.append(df)
			 
		d_f.columns = d_f.columns.str.replace('_x','')
		d_f.head() 
		d_f.reset_index(inplace = True)
		d_f = self.t.deleted_columns(d_f)
		d_f = d_f.rename(columns = {'product_id0' :'product_id','base_total0':'base_total','base_price0':'base_price','quantity0':'quantity'})#,'id0':'order_product_id'})
		d_f.reset_index(inplace = True)


		for i in range (len(d_f)): 
		    for j in range(4):
		        if int(d_f['option_id'+str(j)][i]) not in noid:# si identifica que no esta en el NOID.
		            pass
		        else:# se identifica los option id de cada item que no hacen parte directa y se le pone 0
		            d_f.loc[i,'product_option_id'+ str(j)] = str(0) 
		            d_f.loc[i,'value'+ str(j)] = str(0)
		            
		d_f = d_f.astype(str)
		d_f['qtzoho'] = 0

		return d_f,dfpromo
	