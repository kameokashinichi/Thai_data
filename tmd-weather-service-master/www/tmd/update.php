<?php
include ('mysqllib.php');
include ('site_configuration.php');
include ('mytmdlib.php');

// Get request header and data
$req_header = getallheaders();
$req_data = $_POST;

$type = $req_data['type'];
$str = "";

if($type == 'wt')
{
	$t1 = $req_data['t1'];
	$tmd = $req_data['tmd'];
	$wmo = $req_data['wmo'];
	$t2 = $req_data['t2'];
	$t2 = explode(' ', $t2);
	$t2_dom = explode('-', $t2[0]);
	$t2_tom = explode(':', $t2[1]);
	$temperature = $req_data['temperature'];
	$t_min = $req_data['t_min'];
	$t_max = $req_data['t_max'];
	$msl_pres = $req_data['msl_pres'];
	$rh = $req_data['rh'];
	$wnd_dir = $req_data['wnd_dir'];
	$wnd_speed = $req_data['wnd_speed'];
	$rainfall = $req_data['rainfall'];

	$str  = $_SERVER['REMOTE_ADDR'] . ",";
	$str .= $_SERVER['HTTP_X_FORWARDED_FOR'] . ",";
	$str .= $_SERVER['HTTP_CLIENT_IP'] . ",";
	$str .= $type . ",";
	$str .= $t1 . ",";
	$str .= $tmd . ",";
	$str .= $wmo . ",";
	$str .= $t2[0] . ",";
	$str .= $t2[1] . ",";
	//$str .= $temperature . ","; 
	//$str .= $t_min . ",";
	//$str .= $t_max . ",";
	//$str .= $msl_pres . ","; 
	//$str .= $rh . ",";
	//$str .= $wnd_dir . ",";
	//$str .= $wnd_speed . ",";
	//$str .= $rainfall . ",";
	
	// update
	$t2_dom[0] = (int)$t2_dom[0]; // year
	$t2_dom[1] = (int)$t2_dom[1]; // month
	$t2_dom[2] = (int)$t2_dom[2]; // day
	$t2_tom[0] = (int)$t2_tom[0]; // hour
	$t2_tom[1] = (int)$t2_tom[1]; // minute
	$dom = array(
		"year"=>$t2_dom[0],
		"month"=>$t2_dom[1],
		"day"=>$t2_dom[2],
		"hour"=>$t2_tom[0],
		"minute"=>$t2_tom[1]);
	$n_found = check_for_duplicated_data_weathertoday($type, $wmo, $dom);
	if($n_found == 0)
	{
		// new measurement
		$tmd_data = array(
			't1'=>$t1,
			'tmd'=>-9999,
			'wmo'=>$wmo,
			'dom'=>$dom,
			'temperature'=>$temperature,
			't_min'=>$t_min,
			't_max'=>$t_max,
			'msl_pres'=>$msl_pres,
			'rh'=>$rh,
			'wnd_dir'=>$wnd_dir,
			'wnd_speed'=>$wnd_speed,
			'rainfall'=>$rainfall,
		);
		insert_new_measurement_weathertoday($tmd_data);
		$str .= "NEW,";
	} else 
	{
		// old measurement
		$str .= "OLD,";
	}
	$str .= "\n";
}
else if($type == 'w3')
{
	$t1 = $req_data['t1'];
	$tmd = $req_data['tmd'];
	$wmo = $req_data['wmo'];
	$t2 = $req_data['t2'];
	$t2 = explode(' ', $t2);
	$t2_dom = explode('/', $t2[0]);
	$t2_tom = explode(':', $t2[1]);
	$t_air = $req_data['t_air'];
	$sp = $req_data['sp'];
	$vp = $req_data['vp'];
	$vis = $req_data['vis'];
	$rh = $req_data['rh'];
	$wnd_dir = $req_data['wnd_dir'];
	$wnd_speed = $req_data['wnd_speed'];
	$rainfall = $req_data['rainfall'];
	$rainfall24 = $req_data['rainfall24'];

	$str  = $_SERVER['REMOTE_ADDR'] . ",";
	$str .= $_SERVER['HTTP_X_FORWARDED_FOR'] . ",";
	$str .= $_SERVER['HTTP_CLIENT_IP'] . ",";
	$str .= $type . ",";
	$str .= $t1 . ",";
	$str .= $tmd . ",";
	$str .= $wmo . ",";
	$str .= $t2[0] . ",";
	$str .= $t2[1] . ",";
	//$str .= $t_air . ","; 
	//$str .= $rh . ",";
	//$str .= $sp . ","; 
	//$str .= $vp . ","; 
	//$str .= $vis . ","; 
	//$str .= $wnd_dir . ",";
	//$str .= $wnd_speed . ",";
	//$str .= $rainfall . ",";
	//$str .= $rainfall24 . ",";
	
	// update
	$t2_dom[0] = (int)$t2_dom[0]; // year
	$t2_dom[1] = (int)$t2_dom[1]; // month
	$t2_dom[2] = (int)$t2_dom[2]; // day
	$t2_tom[0] = (int)$t2_tom[0]; // hour
	$t2_tom[1] = (int)$t2_tom[1]; // minute
	$dom = array(
		"year"=>$t2_dom[2],
		"month"=>$t2_dom[0],
		"day"=>$t2_dom[1],
		"hour"=>$t2_tom[0],
		"minute"=>$t2_tom[1]);
	$n_found = check_for_duplicated_data_weather3hours($type, $wmo, $dom);
	if($n_found == 0)
	{
		// new measurement
		$tmd_data = array(
			't1'=>$t1,
			'tmd'=>-9999,
			'wmo'=>$wmo,
			'dom'=>$dom,
			't_air'=>$t_air,
			'sp'=>$sp,
			'vp'=>$vp,
			'vis'=>$vis,
			'rh'=>$rh,
			'wnd_dir'=>$wnd_dir,
			'wnd_speed'=>$wnd_speed,
			'rainfall'=>$rainfall,
			'rainfall24'=>$rainfall24,
		);
		insert_new_measurement_weather3hours($tmd_data);
		$str .= "NEW,";
	} else 
	{
		// old measurement
		$str .= "OLD,";
	}
	$str .= "\n";
}

if(strlen($str) > 0)
{
	$filename = 'req.log';
	$fs = fopen($filename, 'a') or die('cannot open file');
	fprintf($fs, $str);
	fclose($fs);
	echo "OK";
}
else
{
	echo "ERROR";
}

/**
 *
 */
function check_for_duplicated_data_weathertoday($type, $wmo, $dom)
{
	$sql  = "SELECT id FROM tmd_weathertoday ";
	$sql .= "WHERE (wmo_id = '" . $wmo ."') ";
	$sql .= "AND (data_year = '" . $dom['year'] ."') ";
	$sql .= "AND (data_month = '" . $dom['month'] ."') ";
	$sql .= "AND (data_day = '" . $dom['day'] ."') ";
	$sql .= "AND (data_hour = '" . $dom['hour'] ."') ";
	$sql .= "AND (data_minute = '" . $dom['minute'] ."') ";
	//echo $sql;
	$rows = jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);
	
	return count($rows);
}

/**
 *
 */
function insert_new_measurement_weathertoday($data)
{	
	// SQL
	$sql  = "INSERT INTO tmd_weathertoday ";
	$sql .= "(tmd_id, wmo_id, upload_year, upload_month, upload_day, upload_hour, upload_minute, data_year, data_month, data_day, data_hour, data_minute, t, t_min, t_max, msl_p, rh, w_dir, w_speed, rainfall) ";
	$sql .= "VALUE ( ";
		$sql .= $data['tmd'] . ",";
		$sql .= $data['wmo'] . ",";
		$sql .= (int)date("Y") . ","; // A full numeric representation of a year, 4 digits
		$sql .= (int)date("n") . ","; // Numeric representation of a month, without leading zeros
		$sql .= (int)date("j") . ","; // Day of the month without leading zeros
		$sql .= (int)date("H") . ","; // 24-hour format of an hour with leading zeros
		$sql .= (int)date("i") . ","; // Minutes with leading zeros
		$sql .= (int)$data['dom']['year'] . ",";
		$sql .= (int)$data['dom']['month'] . ",";
		$sql .= (int)$data['dom']['day'] . ",";
		$sql .= (int)$data['dom']['hour'] . ",";
		$sql .= (int)$data['dom']['minute'] . ",";
		$sql .= (float)$data['temperature'] . ",";
		$sql .= (float)$data['t_min'] . ",";
		$sql .= (float)$data['t_max'] . ",";
		$sql .= (float)$data['msl_pres'] . ",";
		$sql .= (float)$data['rh'] . ",";
		$sql .= (float)$data['wnd_dir'] . ",";
		$sql .= (float)$data['wnd_speed'] . ",";
		$sql .= (float)$data['rainfall'] . "";
	$sql .= ")";
	jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);
	
	return $sql;
}

/**
 *
 */
function check_for_duplicated_data_weather3hours($type, $wmo, $dom)
{
	$sql  = "SELECT id FROM tmd_weather3hours ";
	$sql .= "WHERE (wmo_id = '" . $wmo ."') ";
	$sql .= "AND (data_year = '" . $dom['year'] ."') ";
	$sql .= "AND (data_month = '" . $dom['month'] ."') ";
	$sql .= "AND (data_day = '" . $dom['day'] ."') ";
	$sql .= "AND (data_hour = '" . $dom['hour'] ."') ";
	$sql .= "AND (data_minute = '" . $dom['minute'] ."') ";
	//echo $sql;
	$rows = jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);
	
	return count($rows);
}

/**
 *
 */
function insert_new_measurement_weather3hours($data)
{	
	// SQL
	$sql  = "INSERT INTO tmd_weather3hours ";
	$sql .= "(tmd_id, wmo_id, upload_year, upload_month, upload_day, upload_hour, upload_minute, data_year, data_month, data_day, data_hour, data_minute, t, rh, sp, vp, vis, w_dir, w_speed, rainfall, rainfall24) ";
	$sql .= "VALUE ( ";
		$sql .= $data['tmd'] . ",";
		$sql .= $data['wmo'] . ",";
		$sql .= (int)date("Y") . ","; // A full numeric representation of a year, 4 digits
		$sql .= (int)date("n") . ","; // Numeric representation of a month, without leading zeros
		$sql .= (int)date("j") . ","; // Day of the month without leading zeros
		$sql .= (int)date("H") . ","; // 24-hour format of an hour with leading zeros
		$sql .= (int)date("i") . ","; // Minutes with leading zeros
		$sql .= (int)$data['dom']['year'] . ",";
		$sql .= (int)$data['dom']['month'] . ",";
		$sql .= (int)$data['dom']['day'] . ",";
		$sql .= (int)$data['dom']['hour'] . ",";
		$sql .= (int)$data['dom']['minute'] . ",";
		$sql .= (float)$data['t_air'] . ",";
		$sql .= (float)$data['rh'] . ",";
		$sql .= (float)$data['sp'] . ",";
		$sql .= (float)$data['vp'] . ",";
		$sql .= (float)$data['vis'] . ",";
		$sql .= (float)$data['wnd_dir'] . ",";
		$sql .= (float)$data['wnd_speed'] . ",";
		$sql .= (float)$data['rainfall'] . ",";
		$sql .= (float)$data['rainfall24'] . "";
	$sql .= ")";
	jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);
	
	return $sql;
}
?>