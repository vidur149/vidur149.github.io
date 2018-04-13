<?php
require 'mailer/PHPMailerAutoload.php';

$mail = new PHPMailer;

$formvars[]='contactName';
$contactName=urldecode($_POST['contactName']);

$formvars[]='contactEmail';
$contactEmail=urldecode($_POST['contactEmail']);

$formvars[]='contactSubject';
$contactSubject=urldecode($_POST['contactSubject']);

$formvars[]='contactMessage';
$contactMessage=urldecode($_POST['contactMessage']);

//$mail->SMTPDebug = 3;                               // Enable verbose debug output

$HOST_NAME = "smtp.mandrillapp.com";
$HOST_PORT = 587;
$SMTPAuth = true;
$HOST_USERNAME = "eswar.vankayalapati@gmail.com";
$HOST_API_KEY = "bdDUictChL8594HR6bKcbg";

$mail = new PHPMailer();
$mail->IsSMTP();
$mail->Host = $HOST_NAME;
$mail->Port = $HOST_PORT;
$mail->SMTPAuth = $SMTPAuth;
$mail->Username = $HOST_USERNAME;
$mail->Password = $HOST_API_KEY;

$mail->From = $contactEmail;
$mail->FromName = $contactName;
$mail->addAddress('eswar.vankayalapati@gmail.com', 'Eswara Sai');

$mail->WordWrap = 50;
$mail->isHTML(true);                                  // Set email format to HTML

$mail->Subject = $contactSubject;
$mail->Body    = 'Hey there!<br>You got a message.<br><b>'.$contactMessage.'</b>';

if(!$mail->send()) {
	$res_string='{"result":"failure","response":"Error"}';
	echo $res_string;
}
else {
    $res_string='{"result":"success","response":"OK"}';
	echo $res_string;
}