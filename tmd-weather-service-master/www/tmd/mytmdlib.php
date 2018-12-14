<?php
/**
 *
 */
function get_tmd_stations() {
	// Get the latest WeatherToday data
	$sql  = "SELECT TmdCode, WmoCode, StationNameEnglish FROM tmd_stations ";
	$sql .= "ORDER BY TmdCode ";
	$rows = jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);
	$stations = array();
	//var_dump($stations);
	foreach($rows as $row)
	{
		$s = array(
			'tmd'=>$row['TmdCode'],
			'wmo'=>$row['WmoCode'],
			'name'=>$row['StationNameEnglish'],
		);
		$stations[] = $s;
	}
	return $stations;
}

/**
 *
 */
function show_tmd_data($year, $stations) {
	if(SHOW_UPLOAD_TIME == true) {
		$n_col_span_total = 14;
		$n_col_span = 4;
	} else {
		$n_col_span_total = 12;
		$n_col_span = 2;
	}
	
	echo "<table id=\"tb_TMD_data\">";
	echo "<tr>";
		echo "<th colspan=\"16\">LATEST DATA</th>";
	echo "</tr>";
	echo "<tr>";
		echo "<th>TMD-ID</th>";
		echo "<th>WMO-ID</th>";
		echo "<th>NAME</th>";
		echo "<th colspan=\"2\">TMD-WeatherToday</th>";
		echo "<th colspan=\"11\">TMD-Weather3Hours</th>";
		//echo "<th colspan=\"".$n_col_span."\">NASA</th>";
	echo "</tr>";
	foreach($stations as $station) {
		// Get the latest WeatherToday data
		$sql  = "SELECT * FROM tmd_weathertoday ";
		$sql .= "WHERE wmo_id = '" . $station['wmo'] . "' ";
		$sql .= "ORDER BY id DESC ";
		$sql .= "LIMIT 1 ";
		$rows = jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);
		$wt = $rows[0];
		$wt_latest_data_date = sprintf('%4d-%02d-%02d', $wt['data_year'], $wt['data_month'], $wt['data_day']);
		$wt_latest_data_time = sprintf('%02d:%02d', $wt['data_hour'], $wt['data_minute']);
		$wt_latest_record_date = sprintf('%4d-%02d-%02d', $wt['upload_year'], $wt['upload_month'], $wt['upload_day']);
		$wt_latest_record_time = sprintf('%02d:%02d', $wt['upload_hour'], $wt['upload_minute']);
		
		// Get the latest Weather3Hours data
		$sql  = "SELECT * FROM tmd_weather3hours ";
		$sql .= "WHERE wmo_id = '" . $station['wmo'] . "' ";
		$sql .= "ORDER BY id DESC ";
		$sql .= "LIMIT 1 ";
		$rows = jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);
		$w3 = $rows[0];
		$w3_latest_data_date = sprintf('%4d-%02d-%02d', $w3['data_year'], $w3['data_month'], $w3['data_day']);
		$w3_latest_data_time = sprintf('%02d:%02d', $w3['data_hour'], $w3['data_minute']);
		$w3_latest_record_date = sprintf('%4d-%02d-%02d', $w3['upload_year'], $w3['upload_month'], $w3['upload_day']);
		$w3_latest_record_time = sprintf('%02d:%02d', $w3['upload_hour'], $w3['upload_minute']);
		
		// Show
		echo "<tr>";
			echo "<td class=\"td_center\">" . $station['tmd'] . "</td>";
			echo "<td class=\"td_center\">" . $station['wmo'] . "</td>";
			echo "<td class=\"td_normal\">" . $station['name'] . "</td>";
			echo "<td class=\"td_center\"><a href=\"index.php?wmo=" . $station['wmo'] . "&type=wt\">" . $wt_latest_data_date . "</a></td>";
			echo "<td class=\"td_center\">" . $wt_latest_data_time . "</td>";
			
			echo "<td class=\"td_center\"><a href=\"index.php?wmo=" . $station['wmo'] . "&type=w3\">" . $w3_latest_data_date . "</a></td>";
			echo "<td class=\"td_center\">" . $w3_latest_data_time . "</td>";
			
			// Each Weather3hours data
			echo "<td class=\"td_center\"><a href=\"?wmo=" . $station['wmo'] . "&type=w3&dt=t\">Temp</a></td>";
			echo "<td class=\"td_center\"><a href=\"?wmo=" . $station['wmo'] . "&type=w3&dt=rh\">RH</a></td>";
			echo "<td class=\"td_center\"><a href=\"?wmo=" . $station['wmo'] . "&type=w3&dt=sp\">SP</a></td>";
			echo "<td class=\"td_center\"><a href=\"?wmo=" . $station['wmo'] . "&type=w3&dt=vp\">VP</a></td>";
			echo "<td class=\"td_center\"><a href=\"?wmo=" . $station['wmo'] . "&type=w3&dt=vi\">VI</a></td>";
			echo "<td class=\"td_center\"><a href=\"?wmo=" . $station['wmo'] . "&type=w3&dt=wd\">WD</a></td>";
			echo "<td class=\"td_center\"><a href=\"?wmo=" . $station['wmo'] . "&type=w3&dt=ws\">WS</a></td>";
			echo "<td class=\"td_center\"><a href=\"?wmo=" . $station['wmo'] . "&type=w3&dt=ra\">RA</a></td>";
			echo "<td class=\"td_center\"><a href=\"?wmo=" . $station['wmo'] . "&type=w3&dt=r24\">R24</a></td>";
		echo "</tr>";
	}
	echo "</table>";
}

/**
 * Show TMD's WeatherToday data
 */
function show_tmd_station_data_wt($wmo, $tmd) {
	$sql  = "SELECT s.* FROM tmd_stations AS s ";
	$sql .= "WHERE s.WmoCode = '" . $wmo . "' ";
	$rows = jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);
	$info = $rows[0];
	
	$sql  = "SELECT s.*, w.* FROM tmd_stations AS s, tmd_weathertoday as w ";
	$sql .= "WHERE s.WmoCode = w.wmo_id ";
	$sql .= "AND w.wmo_id = '" . $wmo . "' ";
	$sql .= "ORDER BY w.data_year, w.data_month, w.data_day, w.data_hour, w.data_minute ";
	$rows = jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);
	echo "<table id=\"tb_TMD_data\">";
		echo "<tr>";
			echo "<th colspan=\"13\">Station DATA : WeatherToday</th>";
		echo "</tr>";
		echo "<tr>";
			echo "<td colspan=\"13\" class=\"td_normal\">";
				echo "<b>TMD-ID :</b> " . $info['TmdCode'] . "<br />";
				echo "<b>WMO-ID :</b> " . $info['WmoCode'] . "<br />";
				echo "<b>Name :</b> " . $info['StationNameEnglish'] . "<br />";
				echo "<b>Latitude (degree) :</b> " . $info['Latitude'] . "<br />";
				echo "<b>Longitude (degree) :</b> " . $info['Longitude'] . "<br />";
				echo "<b>HeightAboveMSL (m) :</b> " . $info['HeightAboveMSL'] . "<br />";
				echo "<b>HeightofWindVane (m) :</b> " . $info['HeightofWindWane'] . "<br />";
				echo "<b>HeightofBarometer (m) :</b> " . $info['HeightofBarometer'] . "<br />";
				echo "<b>HeightofThermometer (m) :</b> " . $info['HeightofThermometer'] . "<br />";
			echo "</td>";
		echo "</tr>";
		echo "<tr>";
		echo "<th>Year</th>";
		echo "<th>Month</th>";
		echo "<th>Day</th>";
		echo "<th>Hour</th>";
		echo "<th>Minute</th>";
		echo "<th>T</th>";
		echo "<th>T_min</th>";
		echo "<th>T_max</th>";
		echo "<th>MSL_P</th>";
		echo "<th>RH</th>";
		echo "<th>W_DIR</th>";
		echo "<th>W_SPEED</th>";
		echo "<th>RAINFALL</th>";
		echo "</tr>";
		foreach($rows as $row) {
			echo "<tr>";
				echo "<td class=\"td_normal\">" . $row['data_year'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['data_month'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['data_day'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['data_hour'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['data_minute'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['t'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['t_min'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['t_max'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['msl_p'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['rh'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['w_dir'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['w_speed'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['rainfall'] . "</td>";
			echo "</tr>";
		}
	echo "</table>";
}

/**
 * Show TMD's Weather3Hours data
 */
function show_tmd_station_data_w3($wmo, $type) {
	$sql  = "SELECT s.* FROM tmd_stations AS s ";
	$sql .= "WHERE s.WmoCode = '" . $wmo . "' ";
	$rows = jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);
	$info = $rows[0];
	
	$sql  = "SELECT s.*, w.* FROM tmd_stations AS s, tmd_weather3hours as w ";
	$sql .= "WHERE s.WmoCode = w.wmo_id ";
	$sql .= "AND w.wmo_id = '" . $wmo . "' ";
	$sql .= "ORDER BY w.data_year, w.data_month, w.data_day, w.data_hour, w.data_minute ";
	$rows = jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);
	echo "<table id=\"tb_TMD_data\">";
		echo "<tr>";
			echo "<th colspan=\"14\">Station DATA : Weather3Hours</th>";
		echo "</tr>";
		echo "<tr>";
			echo "<td colspan=\"14\" class=\"td_normal\">";
				echo "<b>TMD-ID :</b> " . $info['TmdCode'] . "<br />";
				echo "<b>WMO-ID :</b> " . $info['WmoCode'] . "<br />";
				echo "<b>Name :</b> " . $info['StationNameEnglish'] . "<br />";
				echo "<b>Latitude (degree) :</b> " . $info['Latitude'] . "<br />";
				echo "<b>Longitude (degree) :</b> " . $info['Longitude'] . "<br />";
				echo "<b>HeightAboveMSL (m) :</b> " . $info['HeightAboveMSL'] . "<br />";
				echo "<b>HeightofWindVane (m) :</b> " . $info['HeightofWindWane'] . "<br />";
				echo "<b>HeightofBarometer (m) :</b> " . $info['HeightofBarometer'] . "<br />";
				echo "<b>HeightofThermometer (m) :</b> " . $info['HeightofThermometer'] . "<br />";
			echo "</td>";
		echo "</tr>";
		echo "<tr>";
		echo "<th>Year</th>";
		echo "<th>Month</th>";
		echo "<th>Day</th>";
		echo "<th>Hour</th>";
		echo "<th>Minute</th>";
		echo "<th>Air Temperature</th>";
		echo "<th>Relative Humidity</th>";
		echo "<th>Station Pressure</th>";
		echo "<th>Vapor Pressure</th>";
		echo "<th>Visibility</th>";
		echo "<th>Wind Direction</th>";
		echo "<th>Wind Speed</th>";
		echo "<th>Rainfall</th>";
		echo "<th>Rainfall24</th>";
		echo "</tr>";
		foreach($rows as $row) {
			echo "<tr>";
				echo "<td class=\"td_normal\">" . $row['data_year'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['data_month'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['data_day'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['data_hour'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['data_minute'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['t'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['rh'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['sp'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['vp'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['vis'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['w_dir'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['w_speed'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['rainfall'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['rainfall24'] . "</td>";
			echo "</tr>";
		}
	echo "</table>";
}

/**
 *
 */
function show_tmd_station_data_w3_detail($wmo, $data_type) {
	$css_class_td_normal = 'td_center';
	
	switch($data_type) {
		case "t": $data_type_name = "Air Temperature"; $field = "t"; break;
		case "rh": $data_type_name = "Relative Humidity"; $field = "rh"; break;
		case "sp": $data_type_name = "Station Pressure"; $field = "sp"; break;
		case "vp": $data_type_name = "Vapor Pressure"; $field = "vp"; break;
		case "vi": $data_type_name = "Visibility"; $field = "vis"; break;
		case "wd": $data_type_name = "Wind Direction"; $field = "w_dir"; break;
		case "ws": $data_type_name = "Wind Speed"; $field = "w_speed"; break;
		case "ra": $data_type_name = "Rainfall"; $field = "rainfall"; break;
		case "r24": $data_type_name = "Rainfall24"; $field = "rainfall24"; break;
		default: $data_type_name = ""; break;
	}
	
	if($data_type_name == "") {
		return;
	}
	
	$t_interval = array(1,4,7,11,13,16,19,22);
	
	// Weather3Hours data
	$sql  = "SELECT data_year, data_month, data_day, data_hour, data_minute, " . $field . " as value FROM tmd_weather3hours \n";
	$sql .= "WHERE wmo_id = '" . $wmo . "' ";
	$sql .= "ORDER BY data_year, data_month, data_day, data_hour, data_minute ";
	$rows = jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);
	//var_dump($rows);
	$n_data = count($rows);
	
	// Reorganize data
	$year0 = $rows[0]['data_year'];
	$month0 = $rows[0]['data_month'];
	$day0 = $rows[0]['data_day'];
	$odata = array();
	$daily_data = array("date"=>sprintf('%04d-%02d-%02d', $year0, $month0, $day0), "data"=>array(-9999,-9999,-9999,-9999,-9999,-9999,-9999,-9999));
	foreach($rows as $row) {
		$day = $row['data_day'];
		$h = $row['data_hour'];
		switch($h) {
			case  1: $idx = 0; break;
			case  4: $idx = 1; break;
			case  7: $idx = 2; break;
			case 10: $idx = 3; break;
			case 13: $idx = 4; break;
			case 16: $idx = 5; break;
			case 19: $idx = 6; break;
			case 22: $idx = 7; break;
		}
		if($day != $day0) {
			$odata[] = $daily_data;
			//echo "<br />" . $row['data_year'] . "," . $row['data_month'] . "," . $row['data_day'] . "," . $row['data_hour'] . "," . $row['value'] . ", ";
			//echo "<br />" . $h . ",";
			$year0 = $row['data_year'];
			$month0 = $row['data_month'];
			$day0 = $day;
			$daily_data = array("date"=>sprintf('%04d-%02d-%02d', $year0, $month0, $day0), "data"=>array(-9999,-9999,-9999,-9999,-9999,-9999,-9999,-9999));
			
		} else {
			//$h = $row['data_hour'];
			//echo ", ";
			//echo $row['data_year'] . "," . $row['data_month'] . "," . $row['data_day'] . "," . $row['data_hour'] . "," . $row['value'] . ", ";
			//echo $h . ", ";
		}
		$daily_data['data'][$idx] = $row['value'];
	}
	$odata[] = $daily_data;
	//var_dump($odata);
	//echo "<br />";
	
	echo "<h3>" . $data_type_name . "</h3>";
	echo "<table id=\"tb_TMD_data\">";
	echo "<tr>";
		echo "<th>Date</th>";
		echo "<th>01:00</th>";
		echo "<th>04:00</th>";
		echo "<th>07:00</th>";
		echo "<th>10:00</th>";
		echo "<th>13:00</th>";
		echo "<th>16:00</th>";
		echo "<th>19:00</th>";
		echo "<th>22:00</th>";
	echo "</tr>";
	foreach($odata as $daily_data) {
		/*foreach($daily_data['data'] as $hourly_data) {
			echo $hourly_data['1'] . ", ";
		}*/
		//echo $daily_data['date'] . ", ";
		echo "<tr>";
		echo "<td class=\"$css_class_td_normal\">" . $daily_data['date'] . "</td>";
		$keys = array_keys($daily_data['data']);
		for($i = 0; $i < 8; $i++) {
			$value = (float)$daily_data['data'][$i];
			if($value == -9999) {
				$value = "&nbsp;";
			} else {
				$value = sprintf('%.2f', $value);
			}
			//echo sprintf("%02d: %'.10.2f,", $t_interval[$i], (float)$daily_data['data'][$i]);
			echo sprintf("<td class=\"$css_class_td_normal\">%s</td>", $value);
		}
		echo "</tr>";
	}
	echo "</table>";
}

/**
 *
 */
function show_weather_forecast($wmo, $forecast_date) {
	//echo $wmo;
	$n_days = 14;
	$fields = array('rain', 'ws10m', 'wd10m', 'tc_min', 'tc_max', 'rh', 'swdown');
	$n_fields = count($fields);
	if(strlen($wmo) == 0) {
		$sql  = "SELECT * FROM tmd_stations ";
		$rows = jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);
		
		echo "<table id=\"tb_TMD_data\">";
		echo "<tr>";
			echo "<th>WMO</th>";
			echo "<th>NAME</th>";
			echo "<th colspan=\"" . ($n_fields+1) . "\">" . $n_days . " Days Forecast Data</th>";
		echo "</tr>";
		foreach($rows as $row) {
			echo "<tr>";
				echo "<td class=\"td_center\">" . $row['WmoCode'] . "</td>";
				echo "<td class=\"td_normal\">" . $row['StationNameEnglish'] . "</td>";
				echo "<td class=\"td_center\"><a href=\"?wmo=" . $row['WmoCode'] . "\">all</a></td>";
				for($i = 0; $i < $n_fields; $i++) {
					echo "<td class=\"td_center\">" . $fields[$i] . "</td>";
				}
			echo "</tr>";
		}
		echo "</table>";
	} else {
		if(strlen($wmo) == 0) {
			 $forecast_date = date("Y-m-d");
		}
		$sql  = "SELECT * FROM tmd_weather_forecast_daily \n";
		$sql .= "WHERE wmo_id = '" . $wmo . "' \n";
		$sql .= "AND date = '" . $forecast_date . "' \n";
		//$sql .= "AND field = 'tc_min' \n";
		$sql .= "ORDER BY date, day_no, field \n";
		$rows = jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);
		//var_dump($rows);
		
		$n_data = count($rows);
		
		
		echo "<table id=\"tb_TMD_data\">";
		echo "<tr>";
			echo "<th colspan=\"2\">Date</th>";
			for($i = 0; $i < $n_fields; $i++) {
				echo "<th>" . $rows[$i]['field'] . "</th>";
			}
		echo "</tr>";
		
		$k = 0;
		$d = 1;
		echo "<tr>";
		echo "<td class=\"td_center\">" . $d . "</td>";
		echo "<td class=\"td_center\">" . $rows[0]['day_no'] . "</td>";
		for($i = 0; $i < $n_data; $i++) {
			$ri = $rows[$i];
			
			if($k == ($n_fields-1)) {
				echo "<td class=\"td_center\">" . $ri['value'] . "</td>";
				echo "</tr>";
				if($i < ($n_data-1)) {
					$k = 0;
					$d++;
					echo "<tr>";
					echo "<td class=\"td_center\">" . $d . "</td>";
					echo "<td class=\"td_center\">" . $rows[$i+1]['day_no'] . "</td>";
				}
			} else {
				echo "<td class=\"td_center\">" . $ri['value'] . "</td>";
				$k++;
			}
		}
		echo "</table>";
	}
}
?>