<?php

require 'db.php';
require 'models.php';

header('Access-Control-Allow-Origin:*');

$options = [];

if ($provinces = $conn->query('select distinct province from location where is_valid=1;')) {

    // set province
    while ($province = $provinces->fetch(PDO::FETCH_NUM)) {
        $optionNode = new OptionNode();
        $optionNode->value = $province[0];
        $optionNode->label = $province[0];
        $options[] = $optionNode;
    }

    // for each province
    for ($i = 0; $i < count($options); $i++) {
        
        $provinceName = $options[$i]->value;
        if ($cities = $conn->query('select distinct city from location where province="'.$provinceName.'" && is_valid=1;')) {

            // set cities
            while ($city = $cities->fetch(PDO::FETCH_NUM)) {
                $optionNode = new OptionNode();
                $optionNode->value = $city[0];
                $optionNode->label = $city[0];
                $options[$i]->children[] = $optionNode;
            }

            // for each city
            for ($j = 0; $j < count($options[$i]->children); $j++) {

                $cityName = $options[$i]->children[$j]->value;
                if ($countries = $conn->query('select distinct country from location where province="'.$provinceName.'" && city="'.$cityName.'" && is_valid=1;')) {

                    // set countries
                    while ($country = $countries->fetch(PDO::FETCH_NUM)) {
                        $optionNode = new OptionNode();
                        $optionNode->value = $country[0];
                        $optionNode->label = $country[0];
                        $options[$i]->children[$j]->children[] = $optionNode;
                    }

                }

            }

        }
    }
}

echo (json_encode($options, JSON_UNESCAPED_UNICODE));

?>