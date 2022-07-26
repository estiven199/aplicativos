

import numpy as np
import pandas as pd
from zohoapi import zohoapi
from bcispapi import bcispapi
from dateutil import parser
from fedex.config import FedexConfig
from pandas.io.json import json_normalize
from fedex.tools.conversion import sobject_to_dict
from fedex.services.track_service import FedexTrackRequest

class information():
    aws = zohoapi.get_aws_token()
    zoho_token = zohoapi.get_s3_file(aws['AWS_KEY'],aws['SECRET_KEY'], 'zoho_token.json')
    #z = zohoapi.InventoryZohoApi(zoho_token['INV_KEY'])
    z = zohoapi.BooksZohoApi(zoho_token['BOOKS_KEY'])
    b = bcispapi()

    def __init__(self):
         pass

    def traking_not_information(self,var,name_list,data,iteracion,value_except):

        """
        var = It is a list that has all the empty lists that will be used.
        name_list = It is a list that has all the names of lists that will be used.
        data = It is a DataFrame that has all the data that will be used.
        iteracion = It is the row in the range of length of the DataFrame.
        value_except = It is a value that will put on if there is an error.
        IMPORTAN = Both the names of the lists and the empty lists must be in the same order.

        """
        k = 0
        for j in name_list:
            try:
                var[k].append(data[j][iteracion])
            except:
                var[k].append(value_except)
            k+=1

    def tracking_voided(self,var,name_list,data,iteracion,value_except,name_except=None,name_void='Voided'):

        """

        var = It is a list that has all the empty lists that will be used.
        name_list = It is a list that has all the names of lists that will be used.
        data = It is a DataFrame that has all the data that will be used.
        iteracion = It is the row in the range of length of the DataFrame.
        value_except = It is a value that will put on if there is an error.
        name_except = It is the column name to which will be put on an except value different.
        name_void = It is the except value that will put.
        IMPORTAN = Both the names of the lists and the empty lists must be in the same order.

        """

        k = 0
        for j in name_list:
            if j == name_except:
                var[k].append(name_void)
            else:
                try:
                    var[k].append(data[j][iteracion])
                except:
                    var[k].append(value_except)
            k+=1

    def deleted_columns(self,data):

        """
        data = It is a database to which you are going to delete columns is

        """

        data.drop(data.columns[data.columns.str.contains('level',case = False)],axis = 1, inplace = True)
        data.drop(data.columns[data.columns.str.contains('index',case = False)],axis = 1, inplace = True)
        data.drop(data.columns[data.columns.str.contains('Unnamed',case = False)],axis = 1, inplace = True)
        data.drop(data.columns[data.columns.str.contains('Column',case = False)],axis = 1, inplace = True)

        return data

    def search_orders_BCISP(self,data,name_columns):

        """
        data = It is a database where are all orders that we will be searched in BCSIP store.
        name_columns = Column name with to which It will be measured the length of the database.

        """

        data_full = pd.DataFrame(columns = ())
        for j in range(len(data[name_columns])):
            order_product =  self.b.get_order_product(str(data[name_columns][j]))
            dataR = json_normalize(order_product)
            data_full = data_full.append(dataR)
        data_full.reset_index(inplace = True)
        data_full  = self.deleted_columns(data_full)
        return data_full

    def date_format(self,date):
        t = parser.parse(date)
        t = t.strftime('%Y-%m-%d')
        return t

    def tracking_number_fedex(self,tracking):
        CONFIG_OBJ = FedexConfig(key='IQ0pj89hOfSYrwgQ',
                             password='RBLXQOHhlSdboNTRgv2Okt2BX',
                             account_number='298371936',
                             meter_number='250875909')
        track = FedexTrackRequest(CONFIG_OBJ)
        tracking_num = tracking
        track.SelectionDetails.PackageIdentifier.Type = 'TRACKING_NUMBER_OR_DOORTAG'
        track.SelectionDetails.PackageIdentifier.Value = tracking_num
        track.ProcessingOptions = 'INCLUDE_DETAILED_SCANS'
        track.send_request()
        r = sobject_to_dict(track.response)
        return r

    def data_for_carrier(self,carrier,var,name_list,unique,iteracion,value_except,name_except,Value):

        """

        carrier = It is the carrier's name to which we will be to keep the information.
        var = It is a list that has all the empty lists that will be used.
        name_list = It is a list that has all the names of lists that will be used.
        unique = It is the DataFrame without repeated data.
        iteracion = It is the row in the range of length of the DataFrame.
        value_except = It is a value that will put on if there is an error.
        name_except = It is the column name to which will be put on an except value different.
        Value = It is the except value that will put.


        """

        if unique['shipping_provider'][iteracion].upper() =="UPS":
            status = carrier[0]['Status']['Description']
            date = self.date_format(carrier[0]['Date'])
        elif unique['shipping_provider'][iteracion].upper() =="USPS" :
            status = carrier['Event'][0:9]
            date = self.date_format(carrier['EventDate'])
        elif unique['shipping_provider'][iteracion].upper() =="FEDEX" :
            status = carrier[0]['EventDescription']
            date = self.date_format(str(carrier[0]['Timestamp']))

        k = 0
        for j in name_list:
            try:
                if j == name_except:
                    var[k].append(Value)
                elif j == 'Status':
                     var[k].append(status)
                elif j == 'Date':
                    var[k].append(self.date_format(date))
                else:
                     var[k].append(unique[j][iteracion])
            except:
                var[k].append(value_except)
            k+=1


    def information(self,var,name_list,unique,iteracion,value_except,name_except,Value,name_except1=None,Value1=None):

        """

        NOTE:This function will be used when will be tried created the package, but it is not created.
        carrier = It is the carrier's name to which we will be to keep the information.
        var = It is a list that has all the empty lists that will be used.
        name_list = It is a list that has all the names of lists that will be used.
        unique = It is the DataFrame without repeated data.
        iteracion = It is the row in the range of length of the DataFrame.
        value_except = It is a value that will put on if there is an error.
        name_except = It is the column name to which will be put on an except value different.
        Value = It is the except value that will put.
        name_except1 = It is the column name to which will be put on an except value different - optional
        Value1 = It is the except value that will put. - optional

        """
        k = 0
        for j in name_list:
            if j == name_except:
                var[k].append(Value)
            elif  j == name_except1:
                var[k].append(Value1)
            else:
                try:
                    var[k].append(unique[j][iteracion])
                except:
                    var[k].append(value_except)
            k+=1
    def update_Warehouse(self,i,data,unique,value):
        r3 = self.z.retrieve_sorder(data['salesorder_id'][0])
        items = []
        for k in range(len(r3['salesorder']['line_items'])):
            quantity = int(r3['salesorder']['line_items'][k]['quantity'])
            try:
                warehouse_id = r3['salesorder']['line_items'][k]['warehouse_id']
            except:
                warehouse_id = ''

            for j in range (len(data['id_zoho'])):
                if r3['salesorder']['line_items'][k]['line_item_id']==data['line_item_id'][j]:
                    if data['KIT'][j]=='1':# si es un KIt entonces es un servicio
                        print(data['id_zoho'][j])
                        quantity = int(r3['salesorder']['line_items'][k]['quantity'])
                        # se le pone el total de cantidades que hay en  Zoho
                    else:
                        if data['QT'][j]=='0': # si no es KIT, y El QT es igual aun entonces
                            quantity = int(data['qtzoho'][j])
                        elif data['QT'][j]=='1': # si no es KIT, y El QT es igual aun entoncess
                            if int(r3['salesorder']['line_items'][k]['quantity'])==int(data['quantity'][j]):
                                quantity = int(data['quantity'][j])
                            else:
                                quantity = int(data['quantity'][j])
                                line_update = {
                                    'item_id':r3['salesorder']['line_items'][k]['item_id'],
                                    'line_item_id':r3['salesorder']['line_items'][k]['line_item_id'],
                                    'quantity':-int(data['quantity'][j])+int(r3['salesorder']['line_items'][k]['quantity']),
                                    'warehouse_id':r3['salesorder']['line_items'][k]['warehouse_id'],}
                                items.append(line_update)
                        else:# Entra ca si el QT es diferente de unoc

                            if int(r3['salesorder']['line_items'][k]['quantity'])==(int(data['quantity'][j])*int(data['QT'][j])):

                                quantity = int(r3['salesorder']['line_items'][k]['quantity'])
                            else:
                                quantity = (int(data['quantity'][j])*int(data['QT'][j]))
                                line_update = {
                                    'item_id':r3['salesorder']['line_items'][k]['item_id'],
                                    'line_item_id':r3['salesorder']['line_items'][k]['line_item_id'],
                                    'quantity':-(int(data['quantity'][j])*int(data['QT'][j]))+int(r3['salesorder']['line_items'][k]['quantity']),
                                    'warehouse_id':r3['salesorder']['line_items'][k]['warehouse_id'],}
                                items.append(line_update)
                    warehouse_id = '1729377000268984982'
                    break

            line_update = {
                    'item_id':r3['salesorder']['line_items'][k]['item_id'],
                    'line_item_id':r3['salesorder']['line_items'][k]['line_item_id'],
                    'quantity':quantity,
                    'warehouse_id':warehouse_id ,}
            items.append(line_update)


        if value == 'ISP':
            order = str("ISP-0"+ str(data['id'][0]))
            customer_id = str(data['Zoho Customer ID'][0])
        else:
            order = str(data['order'][0])
            customer_id = str(data['customer_id'][0])

        update_data = {'salesorder_number':order,
                      'customer_id':customer_id,
                      'line_items': items, }
        orders_update = self.z.update_order(str(unique['salesorder_id'][i]),update_data)
        print(orders_update['message'] + "  TX")

        return orders_update['message']


    def update_data(self,i,historial,unique,data,shipment,status,value):

        for k in range (len(data['id_zoho'])):

            historial['validation'] = np.where(
            historial['order_product_id'] == data['order_product_id'][k],value,
            historial['validation'])

            historial['status_traking'] = np.where(
            historial['order_product_id'] == data['order_product_id'][k],status,
            historial['status_traking'])

            historial['shipment_id'] = np.where(
            historial['order_product_id'] == data['order_product_id'][k],shipment,
            historial['shipment_id'])


    def update_data_Amazon(self,i,historial,unique,data,shipment,status,value):

        for k in range (len(data['id_zoho'])):

            historial['validation'] = np.where(
            historial['order_value'] == data['order'][k],value,
            historial['validation'])

            historial['status_traking'] = np.where(
            historial['order_value'] == data['order'][k],status,
            historial['status_traking'])

            historial['shipment_id'] = np.where(
            historial['order_value'] == data['order'][k],shipment,
            historial['shipment_id'])


    def update_validation2(self,iteracion,data,historial,unique,data2=None,Value=None):

        """

        data = It is the DataFrame that contains the products for each tracking.
        historial = It is the DataFrame that has all the orders entered into zoho.
        unique = It is the DataFrame without repeated data.
        data2 = It is the DataFrame of the orders that has no tracking.

        """

        try:
            for k in range (len(data['id_zoho'])):
                historial['validation'] = np.where((historial['id'] == unique['id'][iteracion]) & (historial['order_product_id'] == data['order_product_id'][k]),10,historial['validation'])
        except:
                historial['q6'] = np.where(historial['orderNumber'] == unique['order'][iteracion],10,historial['q6'])



    def create_pakcage(self,carrier,trackig,i,data,unique):

        """
        carrier = It is the carrier's name to which we will be to keep the information.
        iteracion = It is the row in the range of length of the DataFrame.
        unique = It is the DataFrame without repeated data.
        data = It is the filtre of each tracking and its respective items

        """


        if carrier =="UPS":
            date = self.date_format(trackig[0]['Date'])
        elif carrier =="USPS" :
            date = self.date_format(trackig['EventDate'])
        elif carrier =="FEDEX" :
            try:
                date = self.date_format(str(trackig[0]['Timestamp']))
            except:
                date = self.date_format(str(trackig))


        package_items = []

        for k in range (len(data['salesorder_id'])):
            package_line = {
            'so_line_item_id':str(data['line_item_id'][k]),
            'quantity':str(data['qtzoho'][k]),}
            package_items.append(package_line)

        package_data = {
        'date': date,
        'line_items': package_items,
        'template_id': '1729377000036843002',}

        r1 = self.z.create_package(str(unique['salesorder_id'][i]), package_data)
        print(r1['message'])

        return r1


    def validation_errores(self,i,message,unique,status):

        """
        iteracion = It is the row in the range of length of the DataFrame.
        message = Is the response that it will be had one time will be creates the package
        unique = It is the DataFrame without repeated data.


        0 = There is no error to create the package.
        110 = Sales Order does not exist.
        111 = Has package but had not shipment
        112 = Hay un problema con los artículos.

        """
        validation = 0
        shipment = 0
        if message['message'] == 'Sales Order does not exist.':
            shipment = 110
            validation = 5
            status = 'Sales Order does not exist.'

        elif message['message'] == 'Quantity recorded cannot be more than quantity ordered.':
            try:
                ry = self.z.retrieve_order(str(unique['salesorder_id'][i]))
                shipment = ry['salesorder']['packages'][0]['shipment_id']
                status = ry['salesorder']['packages'][0]['status'].capitalize()
                validation = 3
            except:
                shipment = 111
                validation = 5
                status = 'Quantity recorded cannot be more than quantity ordered.'

        elif message['message'] =='Invalid value passed for salesorder_id':
            try:
                ry = self.z.retrieve_order(str(unique['salesorder_id'][i]))
                shipment = ry['salesorder']['packages'][0]['shipment_id']
                status = ry['salesorder']['packages'][0]['status'].capitalize()
                validation = 5
            except:
                shipment = 112
                validation = 5
                status = 'Invalid value passed for salesorder_id.'

        elif message['message'][0:14] =='The line items':
            shipment = 113
            validation = 5
            status = 'The line items'

        elif message['message'] =='The package date should be on or after sales order date.':
            shipment = 114
            validation = 5
            status = 'The package date should be on or after sales order date.'

        elif message['message'] =='Invalid value passed for so_line_item_id':
            shipment = 115
            validation = 5
            status = 'Invalid value passed for so_line_item_id'

        elif message['message'] =='Hang on, you cannot package services!':
            shipment = 116
            validation = 5
            status = 'Hang on, you cannot package services!'

        elif message['message'] =='Sales order marked as drop shipment cannot create package and shipment.':
            shipment = 117
            validation = 5
            status = 'Sales order marked as drop shipment cannot create package and shipment.'

        elif message['message'] =='The Package Number given has already been used. Please enter a different number.':
            shipment = 118
            validation = 5
            status = 'The Package Number given has already been used. Please enter a different number.'



        return  validation,shipment,status




    def create_shipment(self,carrier,trackig,i,unique,value_id,r1=None):

        """
        carrier = It is the carrier's name to which we will be to keep the information.
        iteracion = It is the row in the range of length of the DataFrame.
        unique = It is the DataFrame without repeated data.
        message = Is the response that it will be had one time will be creates the package

        """


        if carrier =="UPS":
            status = trackig[0]['Status']['Description']
            date = self.date_format(trackig[0]['Date'])
        elif carrier =="USPS" :
            status = trackig['Event'][0:9]
            date = self.date_format(trackig['EventDate'])
        elif carrier=="FEDEX":
            try:
                status = trackig[0]['EventDescription']
                date = self.date_format(str(trackig[0]['Timestamp']))
            except:
                date = self.date_format(str(trackig))
                status ='Delivered'

        if value_id == 'Create':
            so_data_shi = {

            "date":date,
            "delivery_method":carrier,
            "tracking_number": str(unique['tracking_number'][i]),}
            r2 = self.z.create_shipment(r1['package']['package_id'],str(unique['salesorder_id'][i]),so_data_shi)
            shipment = r2['shipmentorder']['shipment_id']
            print(r2['message'])
            value  = 2

            if status == 'Delivered':
                r = self.z.delivered(str(shipment))
                print(r['message'])
                value  = 1
            return shipment,status,value

        elif value_id == 'Validate':
            if status == 'Delivered':
                r = self.z.delivered(str(unique['shipment_id'][i]))
                print(r['message'])
                value  = 1
                shipment = unique['shipment_id'][i]
            else:
                value  = 2
                shipment = unique['shipment_id'][i]

            return shipment,status,value



    def orders_errors(self,data,historial):
        """
        data = It is the filtre of each tracking and its respective items
        historial = File with all orders of BCSIP store.

        """
        order = []
        data.drop_duplicates('id' , keep = "last", inplace = True)
        data.reset_index(inplace=True)

        data_full = pd.DataFrame(columns = ())
        for j in range(len(data[['id']])):
            order_product =  self.b.get_order_product(str(data['id'][j]))
            dataR = json_normalize(order_product)
            data_full = data_full.append(dataR)
        data_full.reset_index(inplace = True)
        data_full  = self.deleted_columns(data_full)


        data = data_full

        data = data.rename(columns = {'id':'order_product_id'})
        data = data.rename(columns = {'order_id':'id'})

        data['id'] =data['id'].astype(int)
        data['order_product_id'] =data['order_product_id'].astype(int)
        historial['id'] = historial['id'].astype(int)
        historial['order_product_id'] = historial['order_product_id'].astype(int)
        historial = historial.loc[~historial['SKU_Big_Commerce'].isin(['ISP15OFF'])]

        merge = data.merge(historial,how='left', on = ['id','order_product_id'])
        merge = merge.astype(str)
        merge = merge.loc[~merge['name_x'].isin(['None'])]
        merge = merge.loc[~merge['product_id_x'].isin(['10506','10559','11232','10495'])]

        data1 = data
        data1.drop_duplicates('id' , keep = "last", inplace = True)
        data1 = self.deleted_columns(data1)
        data1.reset_index(inplace=True)

        for i in range(len(data1['id'])):
            filtro_in_historial = historial.loc[historial['id'].isin([data1['id'][i]])]
            filtro_in_merge = merge.loc[merge['id'].isin([str(data1['id'][i])])]
            if len(filtro_in_historial) != len(filtro_in_merge):
                order.append(data1['id'][i])
                print('order errada  ' + str(data1['id'][i]))
        return order

    def update_data_BO(self,carrier,iteracion,data,historial,unique,shipment):

            if unique['shipping_provider'][iteracion].upper() =="UPS":
                status = carrier[0]['Status']['Description']
                date = self.date_format(carrier[0]['Date'])
            elif unique['shipping_provider'][iteracion].upper() =="USPS" :
                status = carrier['Event'][0:9]
                date = self.date_format(carrier['EventDate'])
            else:
                status = carrier[0]['EventDescription']
                date = self.date_format(str(carrier[0]['Timestamp']))

            """
            carrier = It is the carrier's name to which we will be to keep the information.
            iteracion = It is the row in the range of length of the DataFrame.
            data = It is the DataFrame that contains the products for each tracking.
            historial = It is the DataFrame that has all the orders entered into zoho with tracking.
            unique = It is the DataFrame without repeated data.


            """
            try:
                for k in range (len(data['id'])):
                    historial['Date'] = np.where(historial['tracking_number'] == data['tracking_number'][k],date,historial['Date'])
                    historial['Status'] = np.where(historial['tracking_number'] == data['tracking_number'][k],status,historial['Status'])
                    historial['shipment_id'] = np.where(historial['tracking_number'] == data['tracking_number'][k],shipment,historial['shipment_id'])
                    historial['tracking_number'] = np.where(historial['tracking_number'] == data['tracking_number'][k],unique['tracking_number'][iteracion],historial['tracking_number'])
            except:
                historial['q6'] = np.where(historial['orderNumber'] == unique['order'][iteracion],10,historial['q6'])
                historial['q5'] = np.where(historial['orderNumber'] == unique['order'][iteracion],shipment,historial['q5'])
                historial['q4'] = np.where(historial['orderNumber'] == unique['order'][iteracion],unique['tracking_number'][iteracion],historial['q4'])
                historial['q3'] = np.where(historial['orderNumber'] == unique['order'][iteracion],status,historial['q3'])
                historial['q2'] = np.where(historial['orderNumber'] == unique['order'][iteracion],date,historial['q2'])
