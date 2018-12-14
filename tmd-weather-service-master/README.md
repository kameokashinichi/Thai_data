# How to prepare TMD's historical data
* Prepare data with 12 columnds : 
	* stn_name : station name (EN)
	* stncode : TMD's station code
	* year : 4-digit
	* month : 2-digit
	* dday : 2-digit
	* maxtmp : maximum temperature (C)
	* mintmp : minimum temperature (C)
	* rain : rainfall (mm)
	* sunshine : sunshine duration (hours)
	* avgrh : average relative humidity (%)
	* evapor : 
	* meantemp : mean temperature (C)
* Export the data as CSV files (See 48407.csv as an examnple). Save these original csv files in /TMD/tmd_historical_data/raw.
	* -9999 = null/no value
* Prepare station data :
	* tmd_station_data_all.csv : whole country
	* tmd_station_study_area.csv : 7 - 8 stations in the NE of Thailand.
	* tmd_station_id.csv : tmd's station-id and wmo-id
* Preprea python script:
	* Open prepare_tmd_historical_data.py
	* Edit variable 'files' in the main section. This is a list of the CSV files to be converted.
	* Run the script. It will read each of csv files and save the data to '/TMD/tmd_historical_data/WMO-ID.csv'. These csv files are daily data : one line = one day.
	* Also, it will extract sunshine duration and save in '/TMD/tmd_historical_data/sunshine/WMO-ID_sunshine.csv'. These csv files are yearly data : one line = one year
	
# How to calculate SRAD from sunshine duration
* Make sure that you have sunshine duration data in /TMD/tmd_historical_data/sunshine/.
* Open cal_srad_from_sunshine.py
	* Edit variable 'data' in the main section to point to tmd station info csv file.
	* The sunshine duration will be used as 'n' in FAO's eq.35.
	* Run the script. It will read sunshine duration and calculate SRAD using FAO's eq.35 with the default parametesrs.
	* The results are exported to '/TMD/tmd_calculated_SRAD/WMO-ID_srad.csv'. These csv files are daily data : one row = one day.