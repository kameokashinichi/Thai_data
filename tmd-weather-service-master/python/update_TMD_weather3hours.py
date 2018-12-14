#!/usr/bin/env python3

import time
import threading
import datetime
import csv
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from os import system, name # import only system from os
from MyTMDLib import MyTMDLib
from MyUtilities import get_doy, write_csv, convert_str_to_float, convert_str_to_int, update_remote_servers

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def get_TMD_stations(filename):
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		stations = list(csv_reader)
	return stations

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def check_w3hours_time_slot(h, m):
	s = -999
	h = float(h) - 1.0
	h = h + (float(m)/60.0)
	
	if (  h >= 0.0) and (h <=  3.0): # 00:00 - 03:00 = 01:00 - 04:00
		s = 0
	elif (h >  3.0) and (h <=  6.0): # 03:01 - 06:00 = 04:01 - 07:00
		s = 1
	elif (h >  6.0) and (h <=  9.0): # 06:01 - 09:00 = 07:01 - 10:00
		s = 2
	elif (h >  9.0) and (h <= 12.0): # 09:01 - 12:00 = 10:01 - 13:00
		s = 3
	elif (h > 12.0) and (h <= 15.0): # 12:01 - 15:00 = 13:01 - 16:00
		s = 4
	elif (h > 15.0) and (h <= 18.0): # 15:01 - 18:00 = 16:01 - 19:00
		s = 5
	elif (h > 18.0) and (h <= 21.0): # 18:01 - 21:00 = 19:01 - 22:00
		s = 6
	else:                        	 # 21:01 - 00:00 = 22:01 - 00:00
		s = 7

	return s

# -------------------------------------------------------------------------------------------
# Update WeatherT3Hours data
# -------------------------------------------------------------------------------------------
def update_tmd_weather_3hours(tmd, tmd_stations, max_data_per_page):	
	# Get WeatherT3Hours V 2.0 data
	header,station_data = tmd.get_Weather3Hours_V2('')
	
	n_tmd_stations = len(tmd_stations)
	
	# show table header
	tmd.show_top_banner()
	tmd.show_table_header_weather_3hours(header)

	# update the data
	ns = 1
	k = 0
	for s in station_data:
		# extract data
		wmo_code = s['WmoStationNumber']
		obs = s['Observation']
		date_time = obs['DateTime']
		dto = datetime.datetime.strptime(date_time, '%m/%d/%Y %H:%M:%S')
		sp = convert_str_to_float(obs['StationPressure'])
		msl_pres = convert_str_to_float(obs['MeanSeaLevelPressure'])
		t_air = convert_str_to_float(obs['AirTemperature'])
		dp = convert_str_to_float(obs['DewPoint'])
		rh = convert_str_to_float(obs['RelativeHumidity'])
		vp = convert_str_to_float(obs['VaporPressure'])
		vis = convert_str_to_float(obs['LandVisibility'])
		wnd_dir = convert_str_to_int(obs['WindDirection'])
		wnd_speed = convert_str_to_float(obs['WindSpeed'])
		rainfall = convert_str_to_float(obs['Rainfall'])
		rainfall24 = convert_str_to_float(obs['Rainfall24Hr'])
		#print('{0:f},{1:f}'.format(rainfall,rainfall24))
		
		tmd_code = ''
		for i in range(n_tmd_stations):
			if(tmd_stations[i][1] == wmo_code):
				tmd_code = tmd_stations[i][0]
				break
				
		# Show 30 items per page
		if(k > max_data_per_page):
			tmd.show_top_banner()
			tmd.show_table_header_weather_3hours(header)
			k = 0;
			
		# update file and databases
		data = [
			str(datetime.datetime.now()),
			tmd_code,
			wmo_code,
			date_time,
			dto.hour,
			dto.minute,
			t_air,
			rh,
			sp,
			vp,
			vis,
			wnd_dir,
			wnd_speed,
			rainfall,
			rainfall24]
		write_csv('tmd_weather_3hours_v2.csv', 'a', data)
		
		# update server
		data = {
			'type':'w3',
			't1':str(datetime.datetime.now()),
			'tmd':tmd_code,
			'wmo':wmo_code,
			't2':date_time,
			't_air':t_air,
			'rh':rh,
			'sp':sp,
			'vp':vp,
			'vis':vis,
			'wnd_dir':wnd_dir,
			'wnd_speed':wnd_speed,
			'rainfall':rainfall,
			'rainfall24':rainfall24}
		# RBRU-GI server
		url = 'http://org.rbru.ac.th/~gi/webservice/tmd/update.php'
		update_remote_servers(url, data)
		# Thaigeomatics server
		url = 'http://www.thaigeomatics.com/webservice/tmd/update.php'
		update_remote_servers(url, data)
			
		# print values
		print('{13:03d} | {0:10s} | {1:>6s} | {2:02d}:{3:02d} | {4:4.2f} | {5:>4.2f} | {6:>7.2f} | {7:>7.2f} | {8:>5.1f} | {9:>03d} | {10:>5.2f} | {11:>7.2f} | {12:>7.2f}'.format(
			tmd_code,
			wmo_code,
			dto.hour,
			dto.minute,
			t_air,
			rh,
			sp,
			vp,
			vis,
			wnd_dir,
			wnd_speed,
			rainfall,
			rainfall24,
			ns
			))
		time.sleep(0.1)
		
		ns = ns + 1
		k = k + 1

# -------------------------------------------------------------------------------------------
# Update TMD data
# -------------------------------------------------------------------------------------------
def update_tmd_data(tmd_stations):
	k = 0
	max_data_per_page = 20		
	
	# TMD object
	tmd = MyTMDLib()
	update_tmd_weather_3hours(tmd, tmd_stations, max_data_per_page)
	del tmd # done
	
# -------------------------------------------------------------------------------------------
# Load TMD stations
# -------------------------------------------------------------------------------------------
if __name__ == "__main__":
	stations = get_TMD_stations("tmd_stations.csv")
	n_stations = len(stations)
	
	# Show UI
	update_tmd_data(stations)