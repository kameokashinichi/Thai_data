import datetime
import urllib.request
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import csv
import os

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def clear_screen():
	# for windows 
	if os.name == 'nt': 
		os.system('cls')
	# for mac and linux(here, os.name is 'posix') 
	else: 
		os.system('clear')
		
# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def validate_field(f):
	if type(f) is float:
		return f
	if type(f) is int:
		return f
	return f
	
# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def convert_str_to_float(v):
	try:
		if type(v) is str:
			vp = float(v)
		else:
			vp = -9999
	except:
		vp = -9999
	return vp
	
# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def convert_str_to_int(v):
	#print(v)
	try:
		if type(v) is str:
			vp = int(v)
		else:
			vp = -9999
	except:
		vp = -9999
	return vp

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def read_csv(filename):
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		data = list(csv_reader)
	return data

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def write_csv(filename, mode, data):
	fs = open(filename, mode)
	for item in data:
		fs.write("%s," % item)
	fs.write("\n")

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def get_current_datetime():
	tmp = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	tmp = tmp.split(" ")
	dddd = tmp[0].split('-')
	tttt = tmp[1].split(':')
	dt = {'year':dddd[0],'month':dddd[1],'day':dddd[2], 'hour':tttt[0], 'minute':tttt[1], 'second':tttt[2]}
	return dt
	
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def get_day_number_in_a_month(m):
	if(type(m) is str):
		m = int(m)
		
	if((m == 1) or (m == 3) or (m == 5) or (m == 7) 
	or (m == 8) or (m == 10) or (m == 12)):
		d = 31
	elif((m == 4) or (m == 6) or (m == 9) or (m == 11)):
		d = 30
	else:
		d = 28
	return d

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def get_doy(dd, mm, yy):
	dd = str(dd)
	mm = str(mm)
	yy = str(yy)
	return datetime.datetime.strptime(yy+" "+mm+" "+dd,'%Y %m %d').timetuple().tm_yday
	
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def update_remote_servers(url, post_data):
	encoded_data = urlencode(post_data).encode('utf-8')
	req = Request(url, encoded_data)
	response_data = urlopen(req).read().decode('utf-8')
