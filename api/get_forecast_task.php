<?php

require 'db.php';
require 'models.php';

header('Access-Control-Allow-Origin:*');

$forecast_id = 0;
if(isset($_GET['forecast_id'])){
    $forecast_id = $_GET['forecast_id'];
}

// query tasks
$task;
if ($result = $conn->query('select * from forecast_task where id = '.$forecast_id.';')) {
    $taskRow = $result->fetch(PDO::FETCH_ASSOC);
    $forecastTaskNode = new ForecastTaskNode();
    $forecastTaskNode->id = intval($taskRow['id']);
    $forecastTaskNode->location_name = $taskRow['location_name'];
    $forecastTaskNode->created_time = intval($taskRow['created_time']);
    $forecastTaskNode->RMSE = floatval($taskRow['RMSE']);
    $forecastTaskNode->MAPE = floatval($taskRow['MAPE']);
    $forecastTaskNode->forecast_date = $taskRow['forecast_date'];
    $forecastTaskNode->forecast_price = floatval($taskRow['forecast_price']);
    $task = $forecastTaskNode;
}

echo (json_encode($task, JSON_UNESCAPED_UNICODE));

?>