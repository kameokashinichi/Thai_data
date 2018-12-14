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
# Update WeatherToday data
# -------------------------------------------------------------------------------------------
def update_tmd_weather_today(tmd, tmd_stations, max_data_per_page):
	# Get WeatherToday V 2.0 data
	header,station_data = tmd.get_WeatherToday_V2('')

	# show table header
	tmd.show_top_banner()
	tmd.show_table_header_weather_today(header)
	
	n_tmd_stations = len(tmd_stations)
	#print(n_tmd_stations)
	# update the data
	k = 0
	ns = 1
	for s in station_data:
		#print(str(k), s['Observation'])
		wmo_code = s['WmoStationNumber']
		obs = s['Observation']
		date_time = obs['DateTime']
		dto = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M')
		temperature = convert_str_to_float(obs['Temperature'])
		t_max = convert_str_to_float(obs['MaxTemperature'])
		t_min = convert_str_to_float(obs['MinTemperature'])
		msl_pres = convert_str_to_float(obs['MeanSeaLevelPressure'])
		rh = convert_str_to_float(obs['RelativeHumidity'])
		wnd_dir = convert_str_to_int(obs['WindDirection'])
		wnd_speed = convert_str_to_int(obs['WindSpeed'])
		rainfall = convert_str_to_float(obs['Rainfall'])
		
		tmd_code = ''
		for i in range(n_tmd_stations):
			if(tmd_stations[i][1] == wmo_code):
				tmd_code = tmd_stations[i][0]
				break
		
		# Show 30 items per page
		if(k > max_data_per_page):
			tmd.show_top_banner()
			tmd.show_table_header_weather_today(header)
			k = 0;
		
		# update file and databases
		data = [
			str(datetime.datetime.now()),
			tmd_code,
			wmo_code,
			date_time,
			dto.hour,
			dto.minute,
			temperature,
			t_min,
			t_max,
			msl_pres,
			rh,
			wnd_dir,
			wnd_speed,
			rainfall]
		write_csv('tmd_weather_today_v2.csv', 'a', data)

		# update server
		data = {
			'type':'wt',
			't1':str(datetime.datetime.now()),
			'tmd':tmd_code,
			'wmo':wmo_code,
			't2':date_time,
			'temperature':temperature,
			't_min':t_min,
			't_max':t_max,
			'msl_pres':msl_pres,
			'rh':rh,
			'wnd_dir':wnd_dir,
			'wnd_speed':wnd_speed,
			'rainfall':rainfall}
		# RBRU-GI server
		url = 'http://org.rbru.ac.th/~gi/webservice/tmd/update.php'
		update_remote_servers(url, data)
		# Thaigeomatics server
		url = 'http://www.thaigeomatics.com/webservice/tmd/update.php'
		update_remote_servers(url, data)
			
		# print values
		print('{12:03d} | {0:10s} | {1:>6s} | {2:02d}:{3:02d} | {4:4.2f} | {5:>4.2f} | {6:>4.2f} | {7:>7.2f} | {8:>5.1f} | {9:>03d} | {10:03d} | {11:>7.2f}'.format(
			tmd_code,
			wmo_code,
			dto.hour,
			dto.minute,
			temperature,
			t_min,
			t_max,
			msl_pres,
			rh,
			wnd_dir,
			wnd_speed,
			rainfall,
			ns
			))
		time.sleep(0.1)

		k = k + 1
		ns = ns + 1
	
# -------------------------------------------------------------------------------------------
# Update TMD data
# -------------------------------------------------------------------------------------------
def update_tmd_data(tmd_stations):
	k = 0
	max_data_per_page = 20		
	
	# TMD object
	tmd = MyTMDLib()
	update_tmd_weather_today(tmd, tmd_stations, max_data_per_page)	
	del tmd # done
	
# -------------------------------------------------------------------------------------------
# Load TMD stations
# -------------------------------------------------------------------------------------------
if __name__ == "__main__":
	stations = get_TMD_stations("tmd_stations.csv")
	n_stations = len(stations)
	
	# Show UI
	update_tmd_data(stations)