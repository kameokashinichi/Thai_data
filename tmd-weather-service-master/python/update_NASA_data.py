import urllib.request
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import collections
import datetime
import time
import os
import csv
#import mysql.connector
from MyUtilities import *
from MyNASALib import MyNASALib

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def get_TMD_stations(filename):
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		stations = list(csv_reader)
	return stations
	
# -----------------------------------------------------------------------------
# Extract NASA POWER API's data.
# -----------------------------------------------------------------------------
# Input data is a JSON file.
def extract_nasa_power_api_data(input, key):
	data = input['features'][0]['properties']['parameter'][key]
	return data

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def update_remote_servers(url, post_data):
	encoded_data = urlencode(post_data).encode('utf-8')
	req = Request(url, encoded_data)
	response_data = urlopen(req).read().decode('utf-8')
	
# -----------------------------------------------------------------------------
# Get NASA data
# -----------------------------------------------------------------------------
def update_nasa_power_data(year_start, year_end, month_end):
	nasa = MyNASALib()
	#print('  Year start: ' + str(year_start))
	#print('  Year end: ' + str(year_end))
	#print('  Month start: ' + str(month_end))
	param_type = "SinglePoint"
	params = ["T2M_MIN", "T2M_MAX", "PRECTOT", "CLRSKY_SFC_SW_DWN", "RH2M"]
	#params = ["T2M_MIN"]
	temporal_average = "DAILY"
	user = "anonymous"
	progress_max = 50
	
	# last day of the month
	tmp = get_day_number_in_a_month(month_end)
	day_end = '{0:02d}'.format(tmp)
		
	# Load stations
	stations = get_TMD_stations("tmd_stations_for_nasa.csv")
	n_stations = len(stations)
	for i in range(n_stations):
		if(i == 0):
			continue
			
		tmd_id = stations[i][0]
		wmo_id = stations[i][1]
		name = stations[i][2]
		lat = stations[i][3]
		lon = stations[i][4]
		
		# no WMO 
		if(wmo_id == '-9999'):
			continue
			
		# No location, skip this station
		if(lat == '-9999'):
			continue
		
		if(lon == '-9999'):
			continue
			
		# Create (overwrite) a log file
		f = open('output/'+wmo_id+'.csv', 'w')
		f.write('wmo_id,data_year,data_month,data_day,data_doy,data_type,data_value\n')
		f.close()
			
		# check starting and ending dates
		current_date = get_current_datetime() # get current datetime
		date_start = year_start + '0101'
		if(year_end == current_date['year']):
			date_end = year_end + month_end + day_end
		else:
			date_end  = year_start + '1231'
		#print(year_start, year_end, date_start, date_end)

		print('----------------------------------------------------------------------------------------------------')
		print('StationID: ' + tmd_id + ', WMO: ' + wmo_id  + ' Name: ' + name)
		print('Location: (' + lat + ', ' + lon + ')')
		print('Date: ' + date_start + ' - ' + date_end);
		print('----------------------------------------------------------------------------------------------------')
				
	
		# Get each paremeter
		for param_k in range(len(params)):
			time_init = get_current_datetime()
			
			if(params[param_k] == 'CLRSKY_SFC_SW_DWN'):
				uc = 'AG'
			else:
				uc = 'SSE'
			
			# Get the data
			print('Loading station-'+wmo_id+'-'+params[param_k]+', please wait...', end='', flush=True)
			data_raw = nasa.get_data_V1(param_type,params[param_k],date_start,date_end,temporal_average,uc,lat,lon,user)
			time_ellapsed = get_current_datetime()
			
			data = extract_nasa_power_api_data(data_raw, params[param_k])
			dp = list(data.items())
			num_data = len(dp)
			print('\r', end='', flush=True)
			
			# Update info
			print('{0:4s}-{1:2s}-{2:2s} {3:2s}:{4:2s}:{5:2s} | {6:4s}-{7:2s}-{8:2s} {9:2s}:{10:2s}:{11:2s} | {12:32s} | {13:18s} | {14:s} | {15:s} | {16:s}'.format(
				time_init['year'],time_init['month'],time_init['day'],
				time_init['hour'],time_init['minute'],time_init['second'],
				time_ellapsed['year'],time_ellapsed['month'],time_ellapsed['day'],
				time_ellapsed['hour'],time_ellapsed['minute'],time_ellapsed['second'],
				name,
				params[param_k],
				date_start, date_end,
				'{0:,d}'.format(num_data)
				))
			
			if(num_data == 0):
				continue
				
			progress_k = 0
			progress_step = num_data/progress_max
			data_date = []
			data_doy = []
			data_value = []
			
			# create local file
			f = open('output/'+wmo_id+'.csv', 'a')
			print('Creating a backup (' + '{0:,d}'.format(num_data) + ')...', end='', flush=True)
			for i in range(num_data):
				# upload data
				k = dp[i][0] # date
				v = dp[i][1] # value
				yy = k[0:4]
				mm = k[4:6]
				dd = k[6:8]
				doy = get_doy(dd, mm, yy)
				data_date.append(k)
				data_value.append(v)
				data_doy.append(doy)
				
				f.write('{0:s},{1:s},{2:d},{3:d},{4:d},{5:s},{6:.4f}\n'.format(
					wmo_id,yy,int(mm),int(dd),int(doy),params[param_k],v))
				# update progress bar
				if(progress_k > progress_step):
					progress_k = 0
					print('.', end='', flush=True)
				else:
					progress_k = progress_k + 1
				time.sleep(0.0005)
			# close file
			f.close()
			print('\r', end='', flush=True)
			time.sleep(1.0)
			
			# update server
			print('Preparing HTTP request (' + '{0:,d}'.format(len(data_value)) + ')...\r', end='', flush=True)
			data = {
				'type':params[param_k], # data type
				't1':str(datetime.datetime.now()), # system's current date and time
				'wmo':wmo_id,
				'data_date':data_date,
				'data_value':data_value,
				'data_doy':data_doy}

			# RBRU-GI server
			print('Uploading to server-1' + '{0:,d}'.format(len(data_value)) + '...\r', end='', flush=True)
			#url = 'http://127.0.0.1/update_nasa_data.php'
			url = 'http://org.rbru.ac.th/~gi/webservice/tmd/update_nasa_data.php'
			#update_remote_servers(url, data)
			# Thaigeomatics server
			print('Uploading to server-2' + '{0:,d}'.format(len(data_value)) + '...\r', end='', flush=True)
			url = 'http://www.thaigeomatics.com/webservice/tmd/update_nasa_data.php'
			#update_remote_servers(url, data)
			time.sleep(30)
	del nasa
	
# -----------------------------------------------------------------------------
# TEST
# -----------------------------------------------------------------------------
# Load TMD stations
if __name__ == "__main__":
	# clear screen
	# for windows 
	if os.name == 'nt': 
		os.system('cls')
	# for mac and linux(here, os.name is 'posix') 
	else: 
		os.system('clear')

	# NASA Power API
	current_date = get_current_datetime()
	y = current_date['year']
	m = current_date['month']
	m = '{0:02d}'.format(int(m) - 1)
	update_nasa_power_data('1985', y, m)
	