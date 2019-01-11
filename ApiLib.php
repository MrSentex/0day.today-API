<?php

    include("parser.php");

    class api_0day_today {

        function __construct() {

            $this->url = sprintf("http://%s.0day.today/", 8, $this->randomSubDomain(5));

            $this->curl_obj = curl_init();
            curl_setopt($this->curl_obj, CURLOPT_COOKIEJAR, dirname(__FILE__) . '/cookie.txt');
            curl_setopt($this->curl_obj, CURLOPT_RETURNTRANSFER,1);

            $this->terms = $this->acceptTerms();

            $this->platforms = array("aix", "Android", "bsd", "freebsd", "hp-ux", "iOS", "irix", "linux", "macOS", "minix", "netware", "novell", "openbsd", "plan9", "QNX", "sco", "solaris", "Symbian", "tru64", "ultrix", "unix", "windows", "hardware", "multiple", "unsorted", "aix", "alpha", "arm", "bsd", "bsd/ppc", "bsd/x86", "bsdi/x86", "freebsd/x86", "freebsd/x86-64", "generator", "hardware", "hpux", "irix", "linux/amd64", "linux/mips", "linux/ppc", "linux/sparc", "linux/x86", "linux/x86-64", "multiple", "netbsd/x86", "openbsd/x86", "os-x/ppc", "os-x/x86", "sco/x86", "solaris/sparc", "solaris/x86", "unixware", "win32", "win64", "asp", "cgi", "java", "jsp", "perl", "php", "python", "ruby", "tricks", "xml");

        }

        function acceptTerms() {
            try {

                curl_setopt($this->curl_obj, CURLOPT_URL, $this->url);
                curl_setopt($this->curl_obj, CURLOPT_POST, true);
                curl_setopt($this->curl_obj, CURLOPT_POSTFIELDS, "agree=Yes, I agree");
                $ot = curl_exec($this->curl_obj);

                curl_setopt($this->curl_obj, CURLOPT_POST, false);
                
                $s_code = curl_getinfo($this->curl_obj, CURLINFO_HTTP_CODE);

                if ($s_code != 200) {
                    return array(false, "Status code: ".$s_code);
                }

                return array(true, null);

            } catch (Exception $err) {
                return array(false, $err->getMessage());
            }

        }

        function randomSubDomain($interactions) {

            $string = "";

            foreach(range(1, $interactions) as $n) {
                $string .= "abcdefghijklmnopqrsuvwxzy1234567890"[rand(0, 35)];
            }

            return $string;

        }

        function findUrl($array) {
            foreach($array as $hit) {

                if (strpos($hit->href, "exploit")) {
                    $url = explode("/", $hit->href);
                    return $url[count($url)-1];
                }

            }
        }

        function fixArray($array_str, $url) {

            $array = explode(" ", $array_str);
            $array_fix = array();

            for($i = 0; $i < count($array); $i++) {
                if (trim($array[$i]) !== "") {
                    $array_fix[$i] = trim($array[$i]);
                }
            }

            $array = $array_fix;

            $date = $array[0];
            $desc = "";

            for($i = 1; $i < count($array); $i++) {
                if ($array[$i] === "Comments:") {
                    $last = $i;
                    break;
                }

                $desc .= $array[$i]." ";

            }

            for($i = $last; $i < count($array); $i++) {
                if (in_array($array[$i], $this->platforms)) {
                    $platform = $array[$i];
                    $last = $i;
                    break;
                }
            }

            if (!in_array("BTC", $array)) {
                $price = "free";
            } else {

                for($i = $last; $i < count($array); $i++) {

                    if ($array[$i] === "BTC") {
                        $btc = $array[$i-1];
                    }

                    if ($array[$i] === "GOLD") {
                        $gold = $array[$i-1];
                    }

                    if(isset($btc) && isset($gold)) {
                        $last = $i;
                        $price = $btc." BTC or ".$gold." GOLD";
                        break;
                    }

                }

            }

            $name = "";

            for($i = $last; $i < count($array); $i++) {

                if($array[$i] === "Exploits:") {
                    $l = $i;
                    for($i = $l-3; $i < $l; $i++) {

                        if ($array[$i] !== "free" && $array[$i] !== "GOLD") {
                            $name .= $array[$i]." ";
                        }

                    }
                }

            }

            $name = utf8_decode(substr($name, 0, count($name)-2));
            $desc = substr($desc, 0, count($desc)-2);

            return array(
                "date" => $date,
                "desc" => $desc,
                "platform" => $platform,
                "price" => $price,
                "author" => $name,
                "url" => "https://0day.today/exploit/".$url
            );

        }

        function search($param) {

            if (!$this->terms[0]) {
                return array(
                    "status" => "fail",
                    "exception" => "An error ocurred in the acceptTerms function | ".$this->terms[1]
                );
            }

            $param = str_replace(" ", "+", $param);

            try {

                curl_setopt($this->curl_obj, CURLOPT_URL, $this->url."search?search_request=".$param);
                $response = curl_exec($this->curl_obj);

                $exploits = array();

                if (!$response) {
                    return array(
                        "status" => "fail",
                        "exception" => "Bad response form 0day.today"
                    );
                }

                $parser = str_get_html($response);

                foreach($parser->find("div") as $divs) {
                    if ($divs->class === "ExploitTableContent") {
                        $url = $this->findUrl($divs->find("a"));
                        $tmp_parser = str_get_html($divs->plaintext);
                        $data = $tmp_parser->plaintext;
                        array_push($exploits, $this->fixArray($data, $url));
                    }
                }


                return array(
                    "status" => "success",
                    "response" => $exploits
                );

            } catch (Exception $err) {
                return array(
                    "status" => "fail",
                    "exception" => "Scrape error | ".$err->getMessage()
                );
            }

        } 
    }
?>