import sys
import os
from os import listdir
import csv
import numpy
#sys.path.append('E:\\Research\\python\lib\\') # local notebook
#sys.path.append('/home/kumpee/Research/python/lib/') # ubuntu server
import time
from MyUtilities import get_doy, read_csv, convert_str_to_float
from get_srad_fao import get_srad_fao # load from local directory

# -------------------------------------------------------------------------------------------
# Global variables
# -------------------------------------------------------------------------------------------
MY_NULL_VALUE = -9999
WTD_NULL_VALUE = -99.0

# -------------------------------------------------------------------------------------------
# Load sunshine duration
# -------------------------------------------------------------------------------------------
def load_sunshine_duration(wmo_id):
	filename = '../data/TMD/tmd_historical_data/sunshine/' + wmo_id + '_sunshine.csv'
	is_file_exists = os.path.exists(filename)
	
	# If file is not exists, create it
	if(is_file_exists == False):
		print('Extracting sunshine duration data...')
		src_filename = '../data/TMD/tmd_historical_data/' + wmo_id + '.csv'
		is_file_exists = os.path.exists(src_filename)
		if(is_file_exists == False):
			print('Source data not found: '.format(wmo_id))
			return None,None
		
		# If the file is exists, load and format the data
		reformat_data(wmo_id,  '../data/TMD/tmd_historical_data/')

	# Load sunshine duration data
	data = read_csv(filename)
	n_data = len(data)
	su = []
	
	# calculate average of sunshine duration data
	su_avg = [0] * 365 # average, 365 dyas
	su_n = [0] * 365 # number of data for each data
	for i in range(n_data):
		#print(data[i][0])
		tmp = [WTD_NULL_VALUE] * 366
		tmp[0] = data[i][0]
		for j in range(1,366):
			val = data[i][j]
			tmp[j] = val
			if((val == 'NaN') or (float(val) == WTD_NULL_VALUE)):
				#print(i, j, 'x')
				tmp[j] = WTD_NULL_VALUE
				continue
			tmp[j] = float(val)
			su_avg[j-1] = su_avg[j-1] + float(val)
			su_n[j-1] = su_n[j-1] + 1
			#print('{},{},{},{},{}'.format(i,j,val,su_avg[j-1],su_n[j-1]))
		su.append(tmp)
	
	# verify data
	n = numpy.sum(su_n)
	if( n < 365 ):
		print('Not enough sunshine duration data! ({} record(s))'.format(n))
		return None,None
	
	for j in range(0,365):
		#print('{}, {}, {}'.format(j, su_avg[j], su_n[i]))
		if( su_n[j] == 0 ):
			su_avg[j] = WTD_NULL_VALUE
			continue;
		su_avg[j] = su_avg[j] / su_n[j]
	
	# done
	return (su,su_avg)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def reformat_data(wmo_id, filepath):
	in_filename = filepath + wmo_id + '.csv'
	data = read_csv(in_filename)
	n_data = len(data)
	#print(n_data)
	
	# raw, formatted csv
	print('Formatting input data...', end='')
	csv_header = 'wmoid,data_year,data_month,data_day,data_doy,tmax,tmin,rainfall,sunshine,rh,vp,tmean\n'
	out_filename = filepath + '/formatted_csv/' + wmo_id + '.csv'
	fs = open(out_filename, 'w')
	fs.write(csv_header)
	yyyy = [WTD_NULL_VALUE] * (n_data-1)
	for i in range(n_data):
		di = data[i]
		
		# skip header
		if(i == 0):
			continue
		
		# get line
		v_date = di[0]
		tmax = convert_str_to_float(di[1])
		tmin = convert_str_to_float(di[2])
		rainfall = convert_str_to_float(di[3])
		sunshine = convert_str_to_float(di[4])
		rh = convert_str_to_float(di[5])
		vp = convert_str_to_float(di[6])
		tmean = convert_str_to_float(di[7])

		# reformat date value
		data_year = v_date[0:4]
		data_month = int(v_date[4:6])
		data_day = int(v_date[6:8])
		data_doy = get_doy(data_day, data_month, data_year)
		yyyy[i-1] = data_year
		str = '{0:s},{1:s},{2:d},{3:d},{4:d},{5:.2f},{6:.2f},{7:.2f},{8:.2f},{9:.2f},{10:.2f},{11:.2f}\n'.format(
				wmo_id,data_year,data_month,data_day,data_doy,tmax,tmin,rainfall,sunshine,rh,vp,tmean)
		fs.write(str);
	fs.close()
	
	# Extract srad
	in_filename = filepath + '/formatted_csv/' + wmo_id + '.csv'
	data = read_csv(in_filename)
	n_data = len(data)
	years = numpy.unique(yyyy)
	n_years = len(years)
	y0 = int(min(yyyy))
	print('{} years ({} - {})'.format(n_years, min(years), max(years)))
	
	odata = []
	for i in range(n_years):
		tmp = [WTD_NULL_VALUE] * 367
		tmp[0] = years[i]
		odata.append(tmp)
	
	for i in range(n_data):
		# Skip header
		if(i == 0):
			continue
		
		# Get data
		di = data[i]
		
		yy = di[1] # year
		mm = di[2] # month
		dd = di[3] # day
		doy = get_doy(dd, mm, yy) # day of the year
		sunshine = di[8] # sunshine duration
		if( float(sunshine) < 0 ):
			sunshine = WTD_NULL_VALUE
		row = int(yy) - y0
		odata[row][doy] = sunshine
	
	out_filename = filepath + 'sunshine/' + wmo_id + '_sunshine.csv'
	print('Export TMD sunshine durations to '+ out_filename)
	fs = open(out_filename, 'w')
	for i in range(n_years):
		di = odata[i]
		for j in range((len(di))):
			fs.write('{},'.format(di[j]))
		fs.write('\n')
	fs.close()
	
# -------------------------------------------------------------------------------------------
# Estimated SRAD at the given (lat, lon)
# @param wmo_id WMO station id
# @lat lattitude of the station (degree)
# @lon longitude of the station (degree)
# -------------------------------------------------------------------------------------------
def estimate_srad_fao(wmo_id, lat, lon):
	# Load sunshine duration
	# Return None if the data cannot be loaded 
	sunshine, sunshine_avg= load_sunshine_duration(wmo_id);
	
	if((sunshine == None) or (sunshine_avg == None)):
		print('Cannot load TMD\'s sunsine duration data : {}, {}, {}'.format(wmo_id, lat, lon))
		return (None,None,None,None,None,None)
	n_years = len(sunshine);
	
	# Calculate Rs, Ra and N usind FAO's eq.35
	# See more details in get_srad_fao.py file.
	# Ra : extraterrestrial radiation, MJ m-2 day-1
	# Ra : solar radiation (MJ m-2 day-1)
	# N : daylight hours (hours)
	
	print('Calculaintg SRAD with FAO\'s default parameters...')
	Rs, Ra, N = get_srad_fao(lat, lon)
	
	# Update FAO-Rs using TMD's sunshine duration
	# by replacing n with the sunshine duration.
	a_s = 0.25; # recommended value
	b_s = 0.50; # recommended value
	srad = [] # empty array
	# yearly data
	print('Calculating SRAD from {} to {}'.format(sunshine[0][0], sunshine[n_years-1][0]));
	for i in range(n_years):
		#print('  {}'.format(sunshine[i][0]))
		tmp = [0] * 366
		tmp[0] = sunshine[i][0]
		for j in range(0, 365):
			# Rs = (as + (bs * (n/N)) * Ra
			_n = sunshine[i][j+1]
			_N = N[j]
			_Ra = Ra[j]
			if(_n == WTD_NULL_VALUE):
				tmp[j+1] = WTD_NULL_VALUE
			else:
				#print('    {}'.format(sunshine[i][j]))
				tmp[j+1] = (a_s + (b_s * (_n/_N))) * _Ra;
		srad.append(tmp)
	print('')
		
	# average data
	srad_avg = [0] * 365 # empty array
	for i in range(0, 365):
		# Rs = (as + (bs * (n/N)) * Ra
		srad_avg[i] = (a_s + (b_s * (sunshine_avg[i]/N[i]))) * Ra[i];
	
	# done
	return (srad, srad_avg, sunshine_avg, Rs, Ra, N)
	
# -------------------------------------------------------------------------------------------
# Application entry point
# -------------------------------------------------------------------------------------------
if __name__ == "__main__":
	# load tmd stations
	#stations = []
	#wmo_id = '48326'
	#lat = 11.0
	#lon = 102.1
	data = read_csv('../data/TMD/tmd_stations_study_area.csv')
	n_stations = len(data)
	n_good = 0
	for i in range(1,n_stations):
		s = data[i]
		tmd_id = s[0]
		wmo_id = s[1]
		name = s[2]
		lat = float(s[3])
		lon = float(s[4])
		print('---------------------------------------------------------')
		print('{}, {}, {}, {:.6f}, {:.6f}'.format(name, tmd_id, wmo_id, lat, lon))
		print('---------------------------------------------------------')
		if(int(wmo_id) == MY_NULL_VALUE):
			print('No WMO-ID!!!, please wait...\n')
			time.sleep(1)
			continue
	
		# Calculate the SRAD
		srad, srad_avg, sunshine, Rs, Ra, N = estimate_srad_fao(wmo_id, lat, lon)
		if(srad_avg == None):
			print('Cannot estimate SRAD for the station : {}'.format(wmo_id))
			continue
	
		# Export to csv
		out_filename = '../data/TMD/tmd_calculated_srad/' + wmo_id + '_srad.csv'
		fs = open(out_filename, 'w')
		for i in range(len(srad)):
			for j in range(len(srad[i])):
				str = '{},'.format(srad[i][j])
				fs.write(str)
				#print('{},{}'.format(i, j))
			fs.write('\n')
		fs.close()
	
		# Export to csv
		#out_filename = '../data/TMD/tmd_calculated_srad/' + wmo_id + '_srad_avg.csv'
		#fs = open(out_filename, 'w')
		#fs.write('doy,fao_Rs,fao_Ra,fao_N,tmd_sunshine,calculated_srad\n')
		#for i in range(0, 365):
		#	str = '{:d},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}\n'.format((i+1), Rs[i], Ra[i], N[i], sunshine[i], srad_avg[i])
		#	fs.write(str)
		#fs.close()
		
		n_good = n_good + 1
		#os.system("pause")
	print('Export {} from {} stations'.format(n_good, n_stations))