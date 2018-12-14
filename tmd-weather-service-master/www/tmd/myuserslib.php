<?php
/**
 *
 */
function show_login_form($target_url) {
?>
<div id="kp_login_form_container">
<form id="kp_login_form" name="kp_login_form" action="<?php echo $target_url; ?>" method="POST" accept-charset="utf-8">
<label for="uname"><b>Username</b></label>
<input type="text" class="kp_login_form_input" placeholder="Enter Username" name="uname" required>
<label for="psw"><b>Password</b></label>
<input type="password" class="kp_login_form_input" placeholder="Enter Password" name="psw" required>
<button type="submit">Login</button>
</form>
</div>
<?php
}

/**
 *
 */
function check_user($u, $p, $url) {
	return false;
}
?>