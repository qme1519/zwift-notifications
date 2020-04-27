<?php
$content = $_GET['preferences'];
$fileLocation = "/home/jakub9367/zwift/preferences.txt";
$file = fopen($fileLocation,"w");
fwrite($file,$content);
fclose($file);
?>
