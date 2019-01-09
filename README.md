# 0day.today unofficial API | 0.2 beta
![Banner.png](https://raw.githubusercontent.com/MrSentex/0day.today-API/master/banner.png?token=AorkL9f8tQVCKNF6tnFOxW4LHEu_1_E4ks5cPhNmwA%3D%3D)

Unofficial API for 0day.today database in Python (HTTP).

This API is not affiliated in any way with "0day.today" and its operation may be against the terms and conditions of "0day.today", therefore the execution of the API will be carried out under the legal responsibility of the user and MrSentex will be uncharged from any illegal use of the API.

## Dependencies

All you need to use the API and start to work with it.

### Python

Dependencies needed to use the API with Python

* Python 2.7 with PyPi (pip)


Python packages needed:

* requests
* bs4
* unidecode

These dependencies are available in PyPi so they can be installed from the command `pip install <package>` or they can be installed with the following command: `pip install -r requeriments.txt` (Must be executed from the folder).

#### Usage

```python
from ApiLib import api_0day_today

search_param = "ssh"

Api = api_0day_today()

print "Searching '{}' in 0day.today database".format(search_param)

results = Api.search(search_param)

if results["status"] != "fail":

    for result in results["response"]:

        print "====== Exploit ======="
        print "Date: {}\nDescription: {}\nPlatform: {}\nPrice: {}\nAuthor: {}\nURL: {}".format(result["date"], result["desc"], result["platform"], result["price"], result["author"], result["url"])
        print "======================"

else:

    print "[ERROR] {}".format(results["exception"])
```
