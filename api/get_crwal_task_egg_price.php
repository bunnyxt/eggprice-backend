<?php

require 'db.php';
require 'models.php';

header('Access-Control-Allow-Origin:*');

$task_id = 0;
if(isset($_GET['task_id'])){
    $task_id = $_GET['task_id'];
}

// query records
$records = [];
if ($recordRows = $conn->query('select * from egg_price where from_task_id = '.$task_id.';')) {
    while ($recordRow = $recordRows->fetch(PDO::FETCH_ASSOC)) {
        $priceRecordNode = new PriceRecordNode();
        $priceRecordNode->url_id = intval($recordRow['url_id']);
        $priceRecordNode->date = $recordRow['date'];
        $priceRecordNode->location_name = $recordRow['location_name'];
        $priceRecordNode->price = floatval($recordRow['price']);
        $priceRecordNode->from_task_id = intval($recordRow['from_task_id']);
        $records[] = $priceRecordNode;
    }
}

echo (json_encode($data, JSON_UNESCAPED_UNICODE));

?>