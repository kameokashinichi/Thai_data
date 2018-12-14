<?php
/**
 *
 */
function cal_et0_daily() {
}

/**
 * http://www.fao.org/docrep/X0490E/x0490e07.htm
 */
function cal_sunshine_hour($lat, $lon) {
}

/**
 * Estimate extraterrestrial radiation
 * http://www.fao.org/docrep/X0490E/x0490e07.htm
 */
function cal_srad($lat, $lon, $n_days, $as=0.25, $bs=0.50) {
	// misc
	$pi = 3.1415926535897932384626433832795;
	$DEG_TO_RAD = $pi/180.0;

	// parameters
	$Ra = 0.0; // extraterrestrial radiation, MJ m-2 day-1
	$Gsc = 0.0820; // soalar constant, MJ m-2 min-1
	$lat_rad = $lat * $DEG_TO_RAD;
	$J = 0; // day of day (number of the day in the year)
	$dr = 0.0; // inverse relative distance Earth-sun
	$ws = 0.0; // sunset hour angle, radian
	$sig = 0.0; // solar decimation, radian
	$N = 0.0; // daylight hours
	$Rs = 0.0; // solar radiation (MJ m-2 may-2)

	// Aux
	$J_fac = $J/$n_days;

	// Calculate inverse distance Earth-sun (FAO, eq.23)
	$dr = 1 + (0.003 * cos(((2 * $pi)*$J_fac)));

	// Calcualte solar decimation
	$sig = 0.409 * sin(((2 * $pi)*$J_fac) - 1.39);

	// Sunset hour angle
	$t1 = -tan($lat_rad);
	$t2 = tan($sig);
	$ws = acos($t1*$t2);

	// Daylight hours
	$N = (24.0/$pi) * $ws;

	$odata_info = array(
			"ds"=>1,
			"de"=>$n_days,
			"as"=>$as,
			"bs"=>$bs,
			);
	$uom = array("Ra"=>"MJ m-2 may-2","Rs"=>"MJ m-2 may-2","N"=>"hours");

	$rs_data = array();
	for($d = 1; $d <= $n_days; $d++)
	{
		$J_fac = $d/$n_days;
		$dr = 1.0 + (0.003 * cos(((2.0 * $pi)*$J_fac)));
		$sig = 0.409 * sin(((2 * $pi)*$J_fac) - 1.39);
		$t1 = -tan($lat_rad);
		$t2 = tan($sig);
		$ws = acos($t1 * $t2);
		$N = (24.0/$pi) * $ws;
		
		// daily extraterrestrial solar radiation
		$Ra = ((24.0*60.0)/$pi) * $Gsc * $dr * (($ws * sin($lat_rad) * sin($sig)) + (cos($lat_rad) * cos($sig) * sin($ws)));
		$n = $N; // daily solar radiation (n = N means clear sky sunshine hours)
		
		// When no actual solar radiation data are available and no calibration 
		// has been carried out for improved as and bs parameters, 
		// the values as = 0.25 and bs = 0.50 are recommended.
		// @see http://www.fao.org/docrep/X0490E/x0490e07.htm
		$as = 0.25;
		$bs = 0.50;
		$Rs = ($as + ($bs * ($n/$N))) * $Ra; // daily solar radiation
		
		// Output array
		$rs_data[] = array(
			"doy"=>$d,
			"N"=>sprintf('%.4f', $N),
			"Ra"=>sprintf('%.4f', $Ra),
			"Rs"=>sprintf('%.4f', $Rs));
		//echo $d, ",", $Ra, ",", $Rs, "<br />";
	}

	$odata = array("Parameters"=>$odata_info, "UOM"=>$uom, "SRAD"=>$rs_data);
	return $odata;
}
?>