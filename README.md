# 0day.today unofficial API | 0.1 beta
![Banner.png](https://raw.githubusercontent.com/MrSentex/0day.today-API/master/banner.png?token=AorkL9f8tQVCKNF6tnFOxW4LHEu_1_E4ks5cPhNmwA%3D%3D)

Unofficial API for 0day.today database in Python (HTTP).

This API is not affiliated in any way with "0day.today" and its operation may be against the terms and conditions of "0day.today", therefore the execution of the API will be carried out under the legal responsibility of the user and MrSentex will be uncharged from any illegal use of the API.

## Dependencies
Main dependencies:

* Python 2.7 with PyPi (pip)
* fontconfig and libfontconfig (Linux only)
* screen (Linux only)
* PhantomJS (Already in repo for windows but in linux you need to download it (https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-i686.tar.bz2))

Python dependecies:

* selenium
* bs4
* unidecode
* flask
* colorama

These dependencies are available in PyPi so they can be installed from the command `pip install <package>` or they can be installed with the following command: `pip install -r requeriments.txt` (Must be executed from the folder).

## Usage

The use of the API is very simple:

#### In .py script

```python
import sys
from LibToday import Api0day

Search = Api0day("ssh")
results = Search.GetResult()
Search.CloseDriver()

if results["status"] == "fail":
    print "[ERROR] {}".format(results["exception"])
    sys.exit()

for result in results["response"]:
    print "====== Exploit ======="
    print "Date: {}\nDescription: {}\nPlatform: {}\nPrice: {}\nAuthor: {}\nURL: {}".format(result["date"], result["desc"], result["platform"], result["price"], result["author"], result["url"])
    print "======================"
```
#### PHP (See ExtraCode/0day.php)
```php
<?php

    include("0day.today");

    $ip = "127.0.0.1";
    $port = "5000";

    // $key = "1234" # Default: "sike"
    
    # WARNING: This function is working only in linux
    StartApi("/home/user/0day.today-API/start.py", $ip, $port); # This function only need to be exec one time (Multiple exec can create bugs) | StartApi("/home/user/0day.today-API/start.py", $ip, $port, $key);

    $ApiToday = new Api0day($ip, $port);  # $ApiToday = new Api0day($ip, $port, $key); | If an error ocurred with the connection the script will create an exception

    $results = $ApiToday->Search("ssh");

    if ($results["status"] == "fail") {
        die("[ERROR] ".$results["exception"]);
    }

    foreach($results["response"] as $result) {
        echo "====== Exploit =======\n";
        echo "Date: ".$result["date"]."\nDescription: ".$result["desc"]."\nPlatform: ".$result["platform"]."\nPrice: ".$result["price"]."\nAuthor: ".$result["author"]."\nURL: ".$result["url"]."\n";
        echo "======================";
    }

?>
```
#### Requests
First of all you need to start the api with the following command: `python api.py ip port key` (Key is optional and seted by default if not specified as "sike"). After seeing that everything works correctly, only the easiest part remains.

The api has two functional url:

* http://ip:port/test-conn?key=key 
  This url will allow you to verify that the key is valid and that the API responds.  
  Response: `{"status" : "success"}` / `{"status" : "fail", "exception" : "Some excpetion here"}`  
  
* http://ip:port/search?key=key&search_param=param  
  This url is the main one of the API and it is the one that allows you to search in 0day.today. It is suggested to set a high wait time since the connection to 0day.today is slow (courtesy of 0day.today).  
    Response: 
    ```json
    {"status" : "success", "response" : [{"date" : "2014-03-12", "desc" : "Sike, thats the wrong number", "platform" : "multiple", "price" : "free", "author" : "MrSentex", "url" : "https://0day.today/exploit/<exploit-id>"}]}
    ```
  or if the Api fail: `{"status" : "fail", "exception" : "Some exception here"}`
