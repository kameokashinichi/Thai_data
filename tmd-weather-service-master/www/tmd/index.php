<?php
include ('mysqllib.php');
include ('site_configuration.php');
include ('mytmdlib.php');
include ('myuserslib.php');
date_default_timezone_set("Asia/Bangkok");

$uname = $_POST['uname'];
$psw = $_POST['psw'];
$service = $_GET['service'];

if(($uname == 'gi') && ($psw == 'gi')) {
	$is_user_ok = true;
} else {
	$is_user_ok = false;
}

$wmo = $_GET['wmo'];
$today = date("Y-m-d");

/*$year = '2018';
$wmo = $_GET['wmo'];
$type = $_GET['type'];
$data_type = $_GET['dt'];
if(strlen($wmo) == 5) {
	if($type == 'wt') {
		show_tmd_station_data_wt($wmo, $type);
	}
	elseif($type == 'w3') {
		if(is_null($data_type)) {
			show_tmd_station_data_w3($wmo, $type);
		} else {
			show_tmd_station_data_w3_detail($wmo, $data_type);
		}
	}
}
else {
	$stations = get_tmd_stations();
	show_tmd_data($year, $stations);
}
*/
?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>RBRU-GI</title>
	<link rel="stylesheet" href="css/style.css">
</head>
<body>
<div id="header">
<!--ul>
<li><b><a href="http://data.tmd.go.th/api/index1.php">TMD-WeatherToday:</a></b>
	ข้อมูลจากกรมอุตุนิยมวิทยา แสดงข้อมูลผลการตรวจวัดรายวัน ปรับปรุงข้อมูลเวลา 07:00 น. 
	ดึงข้อมูลตามเวลาจริงจากเครื่องบริการของกรมอุตุนิยมวิทยา โดยใช้บริการ WeatherToday V2.0
</li>
<li><b><a href="http://data.tmd.go.th/api/index1.php">TMD-Weather3Hours:</a></b> 
	ข้อมูลจากกรมอุตุนิยมวิทยา แสดงข้อมูลผลการตรวจวัดทุก 3 ชั่วโมง ปรับปรุงข้อมูลเวลา 01:00, 04:00, 07:00,10:00,13:00,16:00,19:00,22:00 
	ดึงข้อมูลตามเวลาจริงจากเครื่องบริการของกรมอุตุนิยมวิทยา โดยใช้บริการ Weather3Hours V2.0
</li>
<li><b><a href="https://power.larc.nasa.gov/docs/v1/">NASA:</a></b> ข้อมูลสภาพอากาศจาก NASA 
	ดึงข้อมูลแบบเวลาจริงจากเครื่องบริการของ NASA โดยใช้บริการ NASA Power API V1.0 
</li>
</ul-->
</div>
<?php
	//if($is_user_ok == false) {
	//	show_login_form('?');
	//} else {
	//}
	//show_weather_forecast($wmo, $forecast_date);
	show_weather_forecast($wmo, $today);
	/*$year = '2018';
	$wmo = $_GET['wmo'];
	$type = $_GET['type'];
	$data_type = $_GET['dt'];
	if(strlen($wmo) == 5) {
		if($type == 'wt') {
			show_tmd_station_data_wt($wmo, $type);
		}
		elseif($type == 'w3') {
			if(is_null($data_type)) {
				show_tmd_station_data_w3($wmo, $type);
			} else {
				show_tmd_station_data_w3_detail($wmo, $data_type);
			}
		}
	}
	else {
		$stations = get_tmd_stations();
		show_tmd_data($year, $stations);
	}*/
?>
<div id="footer">
Geoinformatics Program,<br />
Faculty of Computer Science and Information Technology, Rambhai Barni Rajabhat University,<br />
Chanthaburi, Thailand, 22000.
</div>
</body>
</html>