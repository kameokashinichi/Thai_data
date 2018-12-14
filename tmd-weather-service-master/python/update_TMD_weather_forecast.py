import time
import threading
import datetime
import csv
import json
import collections
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from os import system, name # import only system from os
from MyTMDLib import MyTMDLib
from MyUtilities import *

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def get_TMD_stations(filename):
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		stations = list(csv_reader)
	return stations

# -------------------------------------------------------------------------------------------
# Load TMD stations
# -------------------------------------------------------------------------------------------
if __name__ == "__main__":
	clear_screen()
	tmd = MyTMDLib()
	today = get_current_datetime()
	token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjNhOGQ1YjY1NmFmOWU4MTA0N2RjM2Q1YjAzNzgzYjY1NWVjMTczZmU2OTA1NDQyZGQ2M2Y3OGM4MDc1YWIxYWIxOTIzNWRjM2IyYTMwZjM0In0.eyJhdWQiOiIyIiwianRpIjoiM2E4ZDViNjU2YWY5ZTgxMDQ3ZGMzZDViMDM3ODNiNjU1ZWMxNzNmZTY5MDU0NDJkZDYzZjc4YzgwNzVhYjFhYjE5MjM1ZGMzYjJhMzBmMzQiLCJpYXQiOjE1MzUxNjI2MDAsIm5iZiI6MTUzNTE2MjYwMCwiZXhwIjoxNTY2Njk4NjAwLCJzdWIiOiIxNjkiLCJzY29wZXMiOltdfQ.ae2Ir2HrEYGsw6KDlHuW5wTUE_DOCPD0BmBvhUykusEEW3JfQr8eOV_WtqxabYaij6d-16br1xVPHLWIivFAdhSpNlkKqmUm3oeds6jS81-7zTx8O9ecOD73XNedm7YX5s5wxNM_GCP4zy1YaR31ZLBOFA9DTfKSFIcWiGnLsQNns9y-90ZSNE8Irg5JCVpStLbHFJyw7urq6xyCpMYCHvwJwfmFLPFhsXfG-lx21X8d-WKvtcaCdTobfhI7QbVcbfNuTQpA3bMAnSV3LZeAwh_Rsw2Pf9OGlr7vHZfpwc0jzI_-ddyQJ76PPzFYX-w0UABGqyYqL-Xej_idv8fKGM9uribCpfqtXLT45nqowW_w8FuzKhVXV32vCpPnQ3dkMxdz6OZJx3vxpddMYKS6_C6cMxk8Vc0uJuz0xcvsf8MOyF1QOZN3WByJytJSMVLv0GB3M-3Z42fNdfax3l-KVLDgJbuufBqKiplddGq3w3Jai20YtiAlV5y6WNYNw0Y5wIA2dO7IEkOidE0GJqBy5rMU5d6bc2YVi0YhTgkH9E8tLRqZmA_xfwTHooSBzYSMWrGfur9y0R0h9O5GTQ6af3ToKweB0pSLJaXjYTHmQDrJ4Y3UrDFBHC0NsVtwQxVM4qBHbPVKykJo9cfTYZJfUr-eDFORlZ58Y8qChrNnntM'
	tmd.set_token(token)
	
	stations = get_TMD_stations("tmd_stations.csv")
	line = 0
	for station in stations:
		if(line == 0):
			line = line + 1
			continue
		line = line + 1
		
		# Test : 
		wmo = station[1]
		name = station[2]
		lat = station[3]
		lon = station[4]
		#print(lon, type(lon))
		#print(wmo, lat, lon, type(wmo), type(lat), type(lon))
		#continue
		
		if((wmo == '-9999') or (lat == '-9999') or (lon == '-9999')):
			continue

		forecast_date = today['year']+'-'+today['month']+'-'+today['day']
		duration = '14'
		fields = {'tc_min', 'tc_max', 'rh', 'rain', 'swdown', 'ws10m', 'wd10m'}
		fields = ','.join(fields)
		
		# Prepare parameters
		params = {
			'lat':lat, 
			'lon':lon,
			'date':forecast_date,
			'duration':duration,
			'fields':fields}
		
		data = tmd.get_forecast_data(params)
		
		#print(data)
		metadata = data['WeatherForecasts']
		forecasts_data = data['WeatherForecasts'][0]['forecasts']
		n_days = len(forecasts_data)
		
		print(wmo, name, lat, lon, n_days)
		
		if(n_days == 0):
			continue
		
		#print(json.dumps(forecasts_data))
		dates = []
		values = []
		odata = ""
		for i in range(n_days):
			d = forecasts_data[i]['time']
			v = forecasts_data[i]['data']
			
			d = '"'+str(d[:10])+'"'
			tmp = []
			for key in v:
				val = str(forecasts_data[i]['data'][key])
				tmp.append(val)
				#print(key+':'+val+", ", end='')
			#print('')
			tmp = ','.join(tmp)
			#print(tmp)
			
			#odata.append('{"date":'+d + ', "values":[' + tmp + ']}')
			odata = odata + '{"date":' + d + '}'
			if(i < n_days):
				odata = odata + ','
			#values.append('"data":{'+tmp+'}')
			#for key in forecasts[i]['data']:
			#	val = str(forecasts[i]['data'][key])
			#	print(key+':'+val+", ", end='')
			#print('')
		#print(','.join(odata))
		#print(values)
		
		#data_json = {"header":{"wmo":wmo, "date":forecast_date}, "data":forecasts_data}
		odata = json.dumps(data)
		#print(odata)
		# Thaigeomatics server
		data = {
				'service':'set',
				'wmo':wmo,
				'forecast_date':forecast_date,
				'fields':fields,
				'data': odata}
		#url = 'http://127.0.0.1/tmd/forecast.php'
		#send_request_to_remote_servers(url, data)
		url = 'http://www.thaigeomatics.com/webservice/tmd/forecast.php'
		update_remote_servers(url, data)
			
		time.sleep(3)

	# done
	del tmd