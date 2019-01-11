<?php

    include("ApiLib.php");

    $api_0day_today = new api_0day_today();

    $search_param = "ssh";

    $search = $api_0day_today->search($search_param);

    if ($search["status"] === "fail") {
        printf("[Error] ".$search["exception"]."\n"); die();
    }

    foreach($search["response"] as $hit) {
        printf("====== Exploit ======\n");
        printf("Date: %s\n", $hit["date"]);
        printf("Description: %s\n", $hit["desc"]);
        printf("Platform: %s\n", $hit["platform"]);
        printf("Price: %s\n", $hit["price"]);
        printf("Author: %s\n", $hit["author"]);
        printf("URL : %s\n", $hit["url"]);
        printf("======================\n");
    }

?>