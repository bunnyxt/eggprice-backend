<?php

require 'db.php';
require 'models.php';

header('Access-Control-Allow-Origin:*');

// query tasks
$tasks = [];
if ($taskRows = $conn->query('select * from forecast_task order by id desc;')) {
    while ($taskRow = $taskRows->fetch(PDO::FETCH_ASSOC)) {
        $forecastTaskNode = new ForecastTaskNode();
        $forecastTaskNode->id = intval($taskRow['id']);
        $forecastTaskNode->location_name = $taskRow['location_name'];
        $forecastTaskNode->created_time = intval($taskRow['created_time']);
        $forecastTaskNode->RMSE = floatval($taskRow['RMSE']);
        $forecastTaskNode->MAPE = floatval($taskRow['statuMAPEs']);
        $forecastTaskNode->forecast_date = $taskRow['forecast_date'];
        $forecastTaskNode->forecast_price = floatval($taskRow['forecast_price']);
        $tasks[] = $forecastTaskNode;
    }
}

echo (json_encode($tasks, JSON_UNESCAPED_UNICODE));

?>