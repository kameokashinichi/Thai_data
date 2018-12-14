<?php
/**
 *
 */
function jj_query($DB_HOST, $DB_USERNAME, $DB_PASSWORD, $DB_DATABASE, $sql) {
	$rows = array();
	
	// 1. connect
	$conn = @mysql_connect($DB_HOST, $DB_USERNAME, $DB_PASSWORD);
	//echo $conn;

	// 2. query
	mysql_query("SET NAMES 'utf8'");
	$db_selected = @mysql_select_db($DB_DATABASE, $conn);
	//var_dump($db_selected);
	
	$results = @mysql_query($sql, $conn);
	//var_dump($results);
	
	// 3. fetch 
	if (@mysql_num_rows($results) > 0) {
		//while($row = mysql_fetch_array($results)) {
        while($row = @mysql_fetch_assoc($results)) {
            
			//var_dump ($row);
			$rows[] = $row;
		}
	}
	
	return $rows;
}
?>