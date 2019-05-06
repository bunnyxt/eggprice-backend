<?php

require 'db.php';
require 'models.php';

header('Access-Control-Allow-Origin:*');

$province = '';
if(isset($_GET['province'])){
    $province = $_GET['province'];
}

$city = '';
if(isset($_GET['city'])){
    $city = $_GET['city'];
}

$country = '';
if(isset($_GET['country'])){
    $country = $_GET['country'];
}

$data = [];

// query location name
$locationName = '';
if ($locations = $conn->query('select * from location where province="'.$province.'" && city="'.$city.'" && country="'.$country.'" limit 1;')) {
    $location = $locations->fetch(PDO::FETCH_ASSOC);
    $locationName = $location['location_name'];
}

// query data
if ($dataRows = $conn->query('select * from egg_price where location_name="'.$locationName.'";')) {
    while ($dataRow = $dataRows->fetch(PDO::FETCH_ASSOC)) {
        $priceNode = new PriceNode();
        $priceNode->date = $dataRow['date'];
        $priceNode->price = floatval($dataRow['price']);
        $data[] = $priceNode;
    }
}

echo (json_encode($data, JSON_UNESCAPED_UNICODE));

?>