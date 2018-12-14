import sys
import os
from os import listdir
import csv
import numpy
#sys.path.append('E:\\Research\\python\lib\\') # local notebook
#sys.path.append('/home/kumpee/Research/python/lib/') # ubuntu server

from MyUtilities import get_doy, read_csv, convert_str_to_float

# -------------------------------------------------------------------------------------------
# Global variables
# -------------------------------------------------------------------------------------------
MY_NULL_VALUE = -9999
WTD_NULL_VALUE = -99.0

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def get_wmo_id(tmd_id, station_info):
	wmo = MY_NULL_VALUE
	n_data = len(station_info)
	for i in range(1, n_data):
		if(tmd_id == station_info[i][0]):
			wmo = station_info[i][1]
			#print(' {}, {}, {}, {}'.format(i, tmd_id, station_info[i][0], wmo))
			break
	return wmo

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def get_field_value(names, row, fields):
	print(names, fields)
	return MY_NULL_VALUE
	
# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def prepare_tmd_data(station_info, data):
	col_names = data[0]

	n_data = len(data) - 1
	n_p = n_data/40.0
	p = 0
	print('Processing data : {:6d} days '.format(n_data), end='', flush=True)
	for i in range(1, n_data):
		di = data[i]
		name = di[0]
		wmo = get_wmo_id(di[1], station_info)
		if(wmo == MY_NULL_VALUE):
			print('WMO-ID for {} ({}) not found'.format(name, di[1]))
			continue
	
		#print('{} {} {}'.format(i,n_data,wmo))
		if(p > n_p):
			p = 0
			print('*', end='', flush=True)
		else:
			p = p + 1
		
		# output: date,maxtmp,mintmp,rain,sunshine,avgrh,evapor,meantemp
		filename = '../data/TMD/tmd_historical_data/' + wmo + '.csv'
		# Create header
		if( os.path.isfile(filename) == False ):
			fs = open(filename, 'w')
			str = 'date,maxtmp,mintmp,rain,sunshine,avgrh,evapor,meantemp\n'
			fs.write(str)
			fs.close()
		
		# Extract values`
		fs = open(filename, 'a')
		stncode = di[1]
		year = int(di[2])
		month = int(di[3])
		dday = int(di[4])
		maxtmp = convert_str_to_float(di[5])
		mintmp = convert_str_to_float(di[6])
		rain = convert_str_to_float(di[7])
		sunshine = convert_str_to_float(di[8])
		avgrh = convert_str_to_float(di[9])
		evapor = convert_str_to_float(di[10])
		meantemp = convert_str_to_float(di[11])
		
		# Check null value
		# 2018-11-23 : use -99 for NULL
		if(maxtmp == MY_NULL_VALUE): 
			maxtmp = WTD_NULL_VALUE
		if(mintmp == MY_NULL_VALUE): 
			mintmp = WTD_NULL_VALUE
		if(rain == MY_NULL_VALUE): 
			rain = WTD_NULL_VALUE
		if(sunshine == MY_NULL_VALUE): 
			sunshine = WTD_NULL_VALUE
		if(avgrh == MY_NULL_VALUE): 
			avgrh = WTD_NULL_VALUE
		if(evapor == MY_NULL_VALUE): 
			evapor = WTD_NULL_VALUE
		if(meantemp == MY_NULL_VALUE): 
			meantemp = WTD_NULL_VALUE
		
		# write to file
		str = '{:04d}{:02d}{:02d},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}\n'.format(year,month,dday,maxtmp,mintmp,rain,sunshine,avgrh,evapor,meantemp)
		fs.write(str)
		fs.close()
		# if( os.path.isfile(filename) == False ):
			# fs = open(filename, 'w')
			# str = 'date,maxtmp,mintmp,rain,sunshine,avgrh,evapor,meantemp\n'
			# fs.write(str)
			# fs.close()
		# else:
			# fs = open(filename, 'a')
			# stncode = di[1]
			# year = int(di[2])
			# month = int(di[3])
			# dday = int(di[4])
			# maxtmp = convert_str_to_float(di[5])
			# mintmp = convert_str_to_float(di[6])
			# rain = convert_str_to_float(di[7])
			# sunshine = convert_str_to_float(di[8])
			# avgrh = convert_str_to_float(di[9])
			# evapor = convert_str_to_float(di[10])
			# meantemp = convert_str_to_float(di[11])
			
			# Check null value
			# 2018-11-23 : use -99 for NULL
			# if(maxtmp == MY_NULL_VALUE): 
				# maxtmp = WTD_NULL_VALUE
			# if(mintmp == MY_NULL_VALUE): 
				# mintmp = WTD_NULL_VALUE
			# if(rain == MY_NULL_VALUE): 
				# rain = WTD_NULL_VALUE
			# if(sunshine == MY_NULL_VALUE): 
				# sunshine = WTD_NULL_VALUE
			# if(avgrh == MY_NULL_VALUE): 
				# avgrh = WTD_NULL_VALUE
			# if(evapor == MY_NULL_VALUE): 
				# evapor = WTD_NULL_VALUE
			# if(meantemp == MY_NULL_VALUE): 
				# meantemp = WTD_NULL_VALUE
			
			# write to file
			# str = '{:04d}{:02d}{:02d},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}\n'.format(year,month,dday,maxtmp,mintmp,rain,sunshine,avgrh,evapor,meantemp)
			# fs.write(str)
			# fs.close()
	print('')
	
# -------------------------------------------------------------------------------------------
# Application entry point
# -------------------------------------------------------------------------------------------
if __name__ == "__main__":
	# load station codes
	station_info = read_csv('../data/TMD/tmd_station_id.csv')
	
	# load input file
	files = ['../data/TMD/tmd_historical_data/raw/381201.csv',
			 '../data/TMD/tmd_historical_data/raw/381301.csv',
			 '../data/TMD/tmd_historical_data/raw/388401.csv',
			 '../data/TMD/tmd_historical_data/raw/405201.csv',
			 '../data/TMD/tmd_historical_data/raw/405301.csv',
			 '../data/TMD/tmd_historical_data/raw/407301.csv',
			 '../data/TMD/tmd_historical_data/raw/407501.csv',
			 '../data/TMD/tmd_historical_data/raw/409301.csv']
	# files = ['../data/TMD/tmd_historical_data/raw/381201.csv']
			 
	for i in range(len(files)):
		data = read_csv(files[i])
		prepare_tmd_data(station_info, data)