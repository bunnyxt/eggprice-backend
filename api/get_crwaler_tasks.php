<?php

require 'db.php';
require 'models.php';

header('Access-Control-Allow-Origin:*');

// query tasks
$tasks = [];
if ($taskRows = $conn->query('select * from crwal_task order by id  desc;')) {
    while ($taskRow = $taskRows->fetch(PDO::FETCH_ASSOC)) {
        $crwalTaskNode = new CrwalTaskNode();
        $crwalTaskNode->id = intval($taskRow['id']);
        $crwalTaskNode->start_time = intval($taskRow['start_time']);
        $crwalTaskNode->end_time = intval($taskRow['end_time']);
        $crwalTaskNode->latest_url_id = intval($taskRow['latest_url_id']);
        $crwalTaskNode->status = $taskRow['status'];
        $crwalTaskNode->error_info = $taskRow['error_info'];
        $tasks[] = $crwalTaskNode;
    }
}

echo (json_encode($tasks, JSON_UNESCAPED_UNICODE));

?>