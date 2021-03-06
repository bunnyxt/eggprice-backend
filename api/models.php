<?php

class OptionNode {
    public $value;
    public $label;
    public $children;
}

class PriceNode {
    public $date;
    public $price;
}

class CrwalTaskNode {
    public $id;
    public $start_time;
    public $end_time;
    public $latest_url_id;
    public $status;
    public $error_info;
}

class PriceRecordNode {
    public $url_id;
    public $date;
    public $location_name;
    public $price;
    public $from_task_id;
}

class ForecastTaskNode {
    public $id;
    public $location_name;
    public $created_time;
    public $RMSE;
    public $MAPE;
    public $forecast_date;
    public $forecast_price;
}

class ForecastRecordNode {
    public $date;
    public $true_price;
    public $forecast_price;
    public $forecast_id;
}

?>