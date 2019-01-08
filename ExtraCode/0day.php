<?php

    function StartAPI($python_script, $ip, $port, $key="sike") {
        system("screen -S test -d -m ".$python_script." ".$ip." ".$port." ".$key."");
    }

    class Api0day {

        function __construct($ip, $port, $key="sike", $curl=false) {
            $this->ip = $ip;
            $this->port = $port;
            $this->key = $key;
            $this->curl = $curl;
            
            if ($this->curl) {
                $this->curl_obj = curl_init();
            }

            $this->url = "http://".$this->ip.":".$this->port."/";

            $this->TestConnection();

        }

        function Request($url) {
            if ($this->curl) {
                curl_setopt($this->curl_obj, CURLOPT_URL, $this->url.$url);

                $response = curl_exec($this->curl_obj);

                if (curl_getinfo($this->curl_obj, CURLINFO_HTTP_CODE) !== 200) {
                    $response = false;
                }

            } else {
                $response = file_get_contents($this->url.$url);
            }

            return $response;
        }

        function AddGetParams($array_values, $url) {
            if (count($array_values) == 0) {
                return $url;
            }

            $url .= "?";

            foreach($array_values as $value) {
                $url .= $value[0]."=".$value[1]."&";
            }

        }

        function ParseJson($response) {
            try {
                return json_encode($response);
            } catch (Exception $err) {
                return json_encode(array(
                    "status" => "fail",
                    "exception" => $err->getMessage()
                ));
            }
        }

        function TestConnection() {
            $params = array(
                array("key", $this->key)
            );

            $url = $this->AddGetParams($params, "test-conn") ;

            $response = $this->Request($url);

            if (!$response) {return false;}

            $response = $this->ParseJson($response);

            if ($response["status"] != "success") {
                throw new Exception($response["exception"], 6);
            }

            return true;

        }
    
        function Search($search_param) {
            $params = array(
                array("key", $this->key),
                array("search_param", $search_param)
            );

            $url = $this->AddGetParams($params, "search");

            $response = $this->Request($url);

            $response = $this->ParseJson($response);

            return $response;

        }
        
        function Close() {
            if ($this->curl) {
                curl_close($this->curl_obj);
            }
            return;
        }

    }

?>