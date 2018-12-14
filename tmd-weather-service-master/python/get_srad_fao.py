import math
import numpy as np


# ------------------------------------------------------------------
# Estimate extraterrestrial radiation
# http://www.fao.org/docrep/X0490E/x0490e07.htm
# Kumpee Teeravech
# ------------------------------------------------------------------
def get_srad_fao(lat, lon):
	# convert degree to radian
	lat = lat * (math.pi/180.0)
	
	# parameters
	Ra = 0.0 # extraterrestrial radiation, MJ m-2 day-1
	Gsc = 0.0820 # soalar constant, MJ m-2 min-1
	J = 0 # day of day (number of the day in the year)
	dr = 0.0 # inverse relative distance Earth-sun
	ws = 0.0 # sunset hour angle, radian
	sig = 0.0 # solar decimation, radian
	N = 0.0 # daylight hours
	Rs = 0.0 # solar radiation (MJ m-2 day-1)
	
	# Aux
	J_fac = J/365

	# Calculate inverse distance Earth-sun (FAO, eq.23)
	dr = 1 + (0.033 * math.cos(((2 * math.pi)*J_fac)))

	# Calcualte solar decimation
	sig = 0.409 * math.sin(((2 * math.pi)*J_fac) - 1.39)

	# Sunset hour angle
	t1 = -math.tan(lat)
	t2 = math.tan(sig)
	ws = math.acos(t1*t2)
	
	# Daylight hours (day-length)
	N = (24/math.pi) * ws
	
	# ------------------------------------------------------------------
	# Daily Ra
	# ------------------------------------------------------------------
	Ra_d = [0] * 365 # daily extraterrestrial solar radiation
	Rs_d = [0] * 365 # daily solar radiation
	N_d  = [0] * 365 # daylight hours

	for d in range(0, 365): # 0 to 364
		dd = d + 1 # 1 to 365
		J_fac = dd/365
		dr = 1 + (0.003 * math.cos(((2 * math.pi)*J_fac)))
		sig = 0.409 * math.sin(((2 * math.pi)*J_fac) - 1.39)

		t1 = -math.tan(lat)
		t2 = math.tan(sig)
		ws = math.acos(t1*t2)
		N = (24/math.pi) * ws
		N_d[d] = N

		Ra = ((24*60)/math.pi) * Gsc * dr * ((ws * math.sin(lat) * math.sin(sig)) + (math.cos(lat) * math.cos(sig) * math.sin(ws)))
		Ra_d[d] = Ra
		
		n = N
		
		# Where no actual solar radiation data are available and no calibration 
		# has been carried out for improved as and bs parameters, 
		# the values as = 0.25 and bs = 0.50 are recommended.
		# @see http://www.fao.org/docrep/X0490E/x0490e07.htm
		a_s = 0.25
		b_s = 0.50
		Rs = (a_s + (b_s * (n/N))) * Ra
		Rs_d[d] = Rs
		
	return (Rs_d, Ra_d, N_d)