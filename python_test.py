
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