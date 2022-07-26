import requests
import json
import boto3
class upsapi:
	def __init__(self):
		self.endpoint = "https://onlinetools.ups.com/rest/Track"
	def UPS_Track(self,Tracking):
	  self.params = {
					   'UPSSecurity':{
					   	'UsernameToken': {
					   		'Username': 'saferitesolution', 
					   		'Password': 'Safety2017XX'
					   		},
					 'ServiceAccessToken': {'AccessLicenseNumber': '7D489C3A9A678718'}},
					   'TrackRequest':{'Request':{'RequestOption': '15','TransactionReference':{'CustomContext': 'Excel Package Tracker'}},
					   'InquiryNumber': str(Tracking),'TrackingOption':'02'}}
	  self.request = requests.post(url=self.endpoint,json=self.params)
	  self.R1 = json.dumps(self.request.json())
	  self.Result=json.loads(self.R1)
	  return self.Result
		    