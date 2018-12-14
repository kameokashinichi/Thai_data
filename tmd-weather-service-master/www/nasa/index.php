<?php
include ('mysqllib.php');
include ('site_configuration.php');

$type = $_GET['type']; //"T2M_MIN";
$wmo  = $_GET['wmo']; //"48409";

?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>RBRU-GI</title>
	<link rel="stylesheet" href="css/style.css">
</head>
<body>
<?php
if(strlen($wmo) != 5) {
	show_nasa_data();
}
else {
	show_nasa_data_station($wmo, $type);
}
?>
<div id="footer">
Geoinformatics Program,<br />
Faculty of Computer Science and Information Technology, Rambhai Barni Rajabhat University,<br />
Chanthaburi, Thailand, 22000.
</div>
</body>
</html>

<?php
/**
 *
 */
function show_nasa_data() {
	$css_class_td_normal = 'td_normal';
	//$sql  = "SELECT * FROM tmd_stations WHERE WmoCode IN ('48409', '48407', '48408', '48381', '48384', '48405', '48404', '48390') ";
	$sql  = "SELECT * FROM tmd_stations ";
	$sql .= "ORDER BY TmdCode ";
	$rows = jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);
	
	echo "<table id=\"tb_NASA_data\">";
	echo "<tr>";
		echo "<th class=\"$css_class_td_normal\">No.</th>";
		echo "<th class=\"$css_class_td_normal\">TMD</th>";
		echo "<th class=\"$css_class_td_normal\">WMO</th>";
		echo "<th class=\"$css_class_td_normal\" colspan=\"6\">DATA</th>";
	echo "</tr>";
	$k = 1;
	foreach($rows as $row) {
		echo "<tr>";
			echo "<td class=\"$css_class_td_normal\">" . $k . "</td>";
			echo "<td class=\"$css_class_td_normal\">" . $row['TmdCode'] . "</td>";
			echo "<td class=\"$css_class_td_normal\">" . $row['WmoCode'] . "</td>";
			echo "<td class=\"$css_class_td_normal\">" . $row['StationNameEnglish'] . "</td>";
			echo "<td class=\"$css_class_td_normal\"><a href=\"index.php?wmo=" . $row['WmoCode'] . "&type=T2M_MIN\">T2M_MIN</a></td>";
			echo "<td class=\"$css_class_td_normal\"><a href=\"index.php?wmo=" . $row['WmoCode'] . "&type=T2M_MAX\">T2M_MAX</a></td>";
			echo "<td class=\"$css_class_td_normal\"><a href=\"index.php?wmo=" . $row['WmoCode'] . "&type=PRECTOT\">PRECTOT</a></td>";
			echo "<td class=\"$css_class_td_normal\"><a href=\"index.php?wmo=" . $row['WmoCode'] . "&type=RH2M\">RH2M</a></td>";
			echo "<td class=\"$css_class_td_normal\"><a href=\"index.php?wmo=" . $row['WmoCode'] . "&type=CLRSKY_SFC_SW_DWN\">CLRSKY_SFC_SW_DWN</a></td>";
			$k++;
		echo "</tr>";
	}
	echo "</table>";
}

/**
 *
 */
function show_nasa_data_station($wmo, $type) {
	$sql  = "SELECT * FROM nasa_power_data ";
	$sql .= "WHERE wmo_id = '" . $wmo . "' ";
	$sql .= "AND data_type = '" . $type . "' ";
	$sql .= "ORDER BY data_year, data_month, data_day ";

	$rows = jj_query(DB_HOST, DB_USER, DB_PASSWORD, DB_DB, $sql);

	$y0 = $rows[0]['data_year'];
	$m0 = $rows[0]['data_month'];
	
	echo "<table id=\"tb_NASA_data\">";
	echo "<tr>";
		echo "<th class=\"td_normal\">Yr</th>";
		echo "<th class=\"td_normal\">Mo</th>";
		for($i = 1; $i <= 31; $i++) {
			echo "<th class=\"td_normal\">".$i."</th>";
		}
	echo "</tr>";
	echo "<tr>";
	echo "<td class=\"td_normal\">" . $y0 . "</td>";
	echo "<td class=\"td_normal\">" . $m0 . "</td>";
	foreach($rows as $row) {
		$yi = $row['data_year'];
		$mi = $row['data_month'];
		
		if($mi != $m0) {
			while($k < 31) {
				echo "<td class=\"td_normal\">&nbsp;</td>";
				$k++;
			}
			$k = 1;
			$m0 = $mi;
			echo "</tr>";
			
			echo "<tr>";
			echo "<td class=\"td_normal\">" . $row['data_year'] . "</td>";
			echo "<td class=\"td_normal\">" . $row['data_month'] . "</td>";
			//echo "<td class=\"td_normal\">" . $row['data_doy'] . "</td>";
			echo "<td class=\"td_normal\">" . $row['data_value'] . "</td>";
			//$k = 0;
			//for($i = 0; $i < 31; $i++) {
			//	
			//}
		} else {
			$k++;
			echo "<td class=\"td_normal\">" . $row['data_value'] . "</td>";
		}
		
		/*echo "<tr>";
		echo "<td>" . $row['data_year'] . "</td>";
		echo "<td>" . $row['data_month'] . "</td>";
		for($i = 0; $i < 31; $i++) {
			echo "<td class=\"td_normal\">12.34</td>";
			$k++;
		}
		echo "</tr>";
		*/
		/*echo "<tr>";
			echo "<td>" . $row['data_year'] . "</td>";
			echo "<td>" . $row['data_month'] . "</td>";
			echo "<td>" . $row['data_day'] . "</td>";
			echo "<td>" . $row['data_doy'] . "</td>";
			echo "<td>" . $row['data_value'] . "</td>";
		echo "</tr>";*/
	}
	echo "</tr>";
	echo "</table>";
}
?>