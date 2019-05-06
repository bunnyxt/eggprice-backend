<?php

try {
    $conn = new PDO('mysql:host=localhost;dbname=db;charset=utf8','username','password');
}
catch(PDOException $e)
{
    echo ('<script>alert("'.$e->getMessage().'")</script>');
    die;
}

?>