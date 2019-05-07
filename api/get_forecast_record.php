<?php

require 'db.php';
require 'models.php';

header('Access-Control-Allow-Origin:*');

$forecast_id = 0;
if(isset($_GET['forecast_id'])){
    $forecast_id = $_GET['forecast_id'];
}

// query records
$records = [];
if ($recordRows = $conn->query('select * from forecast_record where forecast_id = '.$forecast_id.';')) {
    while ($recordRow = $recordRows->fetch(PDO::FETCH_ASSOC)) {
        $forecastRecordNode = new ForecastRecordNode();
        $forecastRecordNode->date = $recordRow['date'];
        $forecastRecordNode->true_price = floatval($recordRow['true_price']);
        $forecastRecordNode->forecast_price = floatval($recordRow['forecast_price']);
        $forecastRecordNode->forecast_id = intval($recordRow['forecast_id']);
        $records[] = $forecastRecordNode;
    }
}

echo (json_encode($records, JSON_UNESCAPED_UNICODE));

?>