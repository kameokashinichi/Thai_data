# Filename: MyTMDLib.py
# Author: Kumpee Teeravech
# Last modified: 2018-09-22
import urllib.request
from urllib.request import Request, urlopen
import json
import collections
import os
import datetime
from MyUtilities import *

# A class for collecting data from TMD server
class MyTMDLib:
	def __init__(self):
		self.name = 'TMD'
		self.version = '1.0.2'
		self.token = ''

	# Set token key for accessing weather forecast API
	def set_token(self, token):
		self.token = token;
		
	# -------------------------------------------------------------------------------------------
	# -------------------------------------------------------------------------------------------
	def show_top_banner(self):
		clear_screen()
		print('-------------------------------------------------------------------------------------------------------------------------')
		print('RBRU-GI\'s TMD data fetcher V-1.03')
		print('-------------------------------------------------------------------------------------------------------------------------')

	# -------------------------------------------------------------------------------------------
	# -------------------------------------------------------------------------------------------
	def show_table_header_weather_today(self, header):
		print('Dataset: ' + header['Title'])
		print('Description: ' + header['Description'])
		print('LastBuildDate: ' + header['LastBuildDate'])
		print('CopyRight: ' + header['CopyRight'])
		print('Current date/time:' + str(datetime.datetime.now()))
		print('-------------------------------------------------------------------------------------------------------------------------')
		print('No  |   SID      |   WMO  | TIME  |   T   | T-MIN | T-MAX |   MSL   |   RH  |  WD |  WS |   RAIN  ')

	# -------------------------------------------------------------------------------------------
	# -------------------------------------------------------------------------------------------
	def show_table_header_weather_3hours(self, header):
		print('Dataset: ' + header['Title'])
		print('Description: ' + header['Description'])
		print('LastBuildDate: ' + header['LastBuildDate'])
		print('CopyRight: ' + header['CopyRight'])
		print('Current date/time:' + str(datetime.datetime.now()))
		print('-------------------------------------------------------------------------------------------------------------------------')
		print('No  |   SID      |   WMO  | TIME  |   T   |   RH  |    SP   |    VP   |  VIS  |  WD |   WS  |     R   |    R24')

	# -----------------------------------------------------------------------------
	# Get weather forecast data
	# http://data.tmd.go.th/nwpapi/doc/apidoc/location/forecast_daily.html
	# -----------------------------------------------------------------------------
	def get_forecast_data(self, params):
		url = 'http://data.tmd.go.th/nwpapi/v1/forecast/location/daily/at?lat='+params['lat']+'&lon='+params['lon']+'&duration='+params['duration']+'&fields='+params['fields']
		req = Request(url)
		req.add_header('accept', 'application/json')
		req.add_header('authorization', self.token)
		data_html = urlopen(req).read()
		data_json = json.loads(data_html.decode('utf-8'), object_pairs_hook=collections.OrderedDict)
		return data_json
	
	# -----------------------------------------------------------------------------
	# -----------------------------------------------------------------------------
	def get_tmd_id_from_wmocode(stations, wmo):
		n_tmd_stations = len(stations)
		id = ''
		return id
		
	# -----------------------------------------------------------------------------
	# Load data
	# http://data.tmd.go.th/api/WeatherToday/V1/
	# -----------------------------------------------------------------------------
	def get_data(self,url):
		req = urllib.request.Request(url,None);
		data = urllib.request.urlopen(req).read()
		return data
	
	# -----------------------------------------------------------------------------
	# Get TMD stations information
	# -----------------------------------------------------------------------------	
	def get_stations_V1(self):
		url = "http://data.tmd.go.th/api/Station/v1/?uid=demo&ukey=demokey&format=json"
		data_html = self.get_data(url)
		data_json = json.loads(data_html.decode('utf-8'), object_pairs_hook=collections.OrderedDict)
		return data_json
		
	# -----------------------------------------------------------------------------
	# Generate URL
	# -----------------------------------------------------------------------------
	# WeatherToday V1.0
	def generate_request_url_WeatherToday_V1(self,output_type):
		url = "http://data.tmd.go.th/api/WeatherToday/V1/?type="+output_type
		return url
	# WeatherToday V2.0
	def generate_request_url_WeatherToday_V2(self,u,pwd,output_type):
		url = "http://data.tmd.go.th/api/WeatherToday/V2/?uid="+u+"&ukey="+pwd+"&format="+output_type
		return url
	# Weather3Hours V1.0
	def generate_request_url_Weather3Hours_V1(self,output_type):
		url = "http://data.tmd.go.th/api/Weather3Hours/V1/?type="+output_type
		return url
	# Weather3Hours V2.0
	def generate_request_url_Weather3Hours_V2(self,u,pwd,output_type):
		url = "http://data.tmd.go.th/api/Weather3Hours/V2/?uid="+u+"&ukey="+pwd+"&format="+output_type
		return url
		
	# -----------------------------------------------------------------------------
	# Extract TMD 'WeatherTodat' V 1.0
	# -----------------------------------------------------------------------------
	# WeatherToday V1.0
	def extract_WeatherToday_V1(self,input, target_WMO_station):
		#print('  extraccting data, please wait...')
		if(target_WMO_station == ''):
			s = input['Stations']
		else:
			for s in input['Stations']:
				if(s['WmoNumber'] == target_WMO_station):
					obs = s['Observe']
					obs_time = obs['Time']
					dd,mm,yy = obs_time.split('/')
					lat = s['Latitude']['Value']
					lon = s['Longitude']['Value']
					t_min = obs['MinTemperature']['Value']
					t_max = obs['MaxTemperature']['Value']
					t_0700 = obs['Temperature']['Value']
					rf_now = obs['Rainfall']['Value']
					break
		return s
	# WeatherToday V2.0
	def extract_WeatherToday_V2(self, input, target_WMO_station):
		h = input['Header']
		# no data
		if(len(input['Stations']) == 0):
			s = []
		else:
			stations = input['Stations']['Station']
			if(target_WMO_station == ''):
				# return all stations
				s = stations
			else:
				# search for specific targget
				for s in stations:
					if(s['WmoStationNumber'] == target_WMO_station):
						break
		return h, s
		
	# Weather3Hours V1.0
	def extract_Weather3Hours_V1(self,input, target_WMO_station):
		#print('  extraccting data, please wait...')
		s = ""
		for s in input['Stations']:
			if(s['WmoNumber'] == target_WMO_station):
				at = s['Latitude']['Value']
				lon = s['Longitude']['Value']
				obs = s['Observe']
				obs_time = obs['Time']
				dd,mm,yy = obs_time.split('/')
				t_now = obs['Temperature']['Value']
				rf_now = obs['Rainfall']['Value']
				break
		return s
	# Weather3Hours V2.0
	def extract_Weather3Hours_V2(self,input,target_WMO_station):
		h = input['Header']
		# no data
		if(len(input['Stations']) == 0):
			s = []
		else:
			stations = input['Stations']['Station']
			if(target_WMO_station == ''):
				# return all stations
				s = stations
			else:
				# search for specific targget
				for s in stations:
					if(s['WmoStationNumber'] == target_WMO_station):
						break
		return h,s
		
	# -----------------------------------------------------------------------------
	# Get NASA data
	# -----------------------------------------------------------------------------
	# WeatherToday V1.0
	def get_WeatherToday_V1(self,target_WMO_station):
		print('Requesting, please wait...')
		url = self.generate_request_url_WeatherToday_V1('json')
		data_html = self.get_data(url)
		data_json = json.loads(data_html.decode('utf-8'), object_pairs_hook=collections.OrderedDict)
		data = self.extract_WeatherToday_V1(data_json, target_WMO_station)
		return data
	# WeatherToday V2.0
	def get_WeatherToday_V2(self,target_WMO_station):
		#print('Requesting WeatherToday V2.0, please wait...')
		url = self.generate_request_url_WeatherToday_V2('api','api12345','json')
		data_html = self.get_data(url)
		data_json = json.loads(data_html.decode('utf-8'), object_pairs_hook=collections.OrderedDict)
		header,data = self.extract_WeatherToday_V2(data_json, target_WMO_station)
		return header,data
		
	# Weather3Hours V1.0
	def get_Weather3Hours_V1(self,target_WMO_station):
		print('Requesting, please wait...')
		url = self.generate_request_url_Weather3Hours_V1('json')
		data_html = self.get_data(url)
		data_json = json.loads(data_html.decode('utf-8'), object_pairs_hook=collections.OrderedDict)
		data = self.extract_Weather3Hours_V1(data_json, target_WMO_station)
		return data
	# Weather3Hours V2.0
	def get_Weather3Hours_V2(self,target_WMO_station):
		url = self.generate_request_url_Weather3Hours_V2('api','api12345','json')
		data_html = self.get_data(url)
		data_json = json.loads(data_html.decode('utf-8'), object_pairs_hook=collections.OrderedDict)
		header, data = self.extract_Weather3Hours_V2(data_json, target_WMO_station)
		return header, data