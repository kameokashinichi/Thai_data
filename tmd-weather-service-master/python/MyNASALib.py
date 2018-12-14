import urllib.request
import json
import collections
import os

class MyNASALib:
	def __init__(self):
		self.name = 'NASA'
		
	# -----------------------------------------------------------------------------
	# Load data
	# https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py?request=execute&identifier=SinglePoint&parameters=CLRSKY_SFC_SW_DWN&startDate=20180701&endDate=20180903&tempAverage=DAILY&userCommunity=AG&outputList=JSON&lat=16.333333&lon=102.81666&user=anonymous
	# -----------------------------------------------------------------------------
	def get_data(self, url, timeout):
		req = urllib.request.Request(url,None);
		data = urllib.request.urlopen(req, None, timeout).read()
		return data
		
	# -----------------------------------------------------------------------------
	# Generate URL
	# -----------------------------------------------------------------------------
	def gnerate_request_url_nasa_power_api(self,param_type,param,date_start,date_end,temporal_average,uc,lat,lon,user):
		url = "https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py?request=execute&identifier="+param_type+"&parameters="+param+"&startDate="+date_start+"&endDate="+date_end+"&tempAverage="+temporal_average+"&userCommunity="+uc+"&outputList=JSON&lat="+lat+"&lon="+lon+"&user="+user
		#url = 'http://127.0.0.1/test_nasa.json'
		return url
		
	# -----------------------------------------------------------------------------
	# Extract NASA POWER API's data.
	# -----------------------------------------------------------------------------
	# Input data is a JSON file.
	def extract_nasa_power_api_data(self,input, key):
		#print('  extraccting data, please wait...')
		try:
			data = input['features'][0]['properties']['parameter'][key]
			#print('  number of dates:'+str(len(data)))
			#doy = 1
			#for k,v in data.items():
			#	yy = k[0:4]
			#	mm = k[4:6]
			#	dd = k[6:8]
			#	#print(doy, k, yy, mm, dd, v)
			#	doy = doy + 1
		except:
			data = []
		return data
		
	# -----------------------------------------------------------------------------
	# -----------------------------------------------------------------------------
	def get_data_V1(self, param_type,param,date_start,date_end,temporal_average,uc,lat,lon,user):
		url = self.gnerate_request_url_nasa_power_api(param_type,param,date_start,date_end,temporal_average,uc,lat,lon,user)
		#print(url)
		timeout = 300
		data_html = self.get_data(url, timeout)
		data_json = json.loads(data_html.decode('utf-8'), object_pairs_hook=collections.OrderedDict)
		return data_json