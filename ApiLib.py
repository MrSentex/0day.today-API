
#############################
# 0day.today unofficial api #
#       By MrSentex         #
#############################

# <= Imports =>
from random import SystemRandom
from requests import Session
from codecs import ascii_encode
from unidecode import unidecode
from bs4 import BeautifulSoup as Soup
# <= Imports =>

class api_0day_today:

    def __init__(self):

        self.url = "http://{}.0day.today".format(self.randomSubDomain(5))
        self.session_obj = Session()

        self.terms = self.acceptTerms()
    
    def acceptTerms(self):
        try:
            self.session_obj.post(self.url, data={"agree" : "Yes, I agree"})
            return (True, None)
        except Exception as err:
            return (False, str(err))

    def randomSubDomain(self, interactions):

        string = ""

        for _ in range(1, interactions):
            string += SystemRandom().choice("abcdefghijklmnopqrstuvwxyz1234567890")
        
        return string
    
    def fixString(self, string):

        string = ascii_encode(unidecode(string.replace("\n", "").replace("\t", "")))[0]

        if string.find("Comments:") != -1:
            string = string[:string.find("Comments: {}".format(string[string.find("Comments:")+10:string.find("Comments:")+len(string)-string.find("Comments:")-1]))]

        if string.find("Rate down:") != -1:
            string = string[:string.find("Rate down: {}".format(string[string.find("Rate down:")+11:string.find("Rate down:")+len(string)-string.find("Rate down:")-1]))]
        
        if string.find("Rate up:") != -1:
            string = string[:string.find("Rate up: {}".format(string[string.find("Rate up:")+9:string.find("Rate up:")+len(string)-string.find("Rate up:")-1]))]

        return string
    
    def fixPrice(self, price):

        price = self.fixString(price)

        if price.startswith("free"):
            return "free"

        btc = price[price.find("for")+4:price.find("BTC")-1]
        pre_gold = price[price.find("BTC")+4:len(price)]
        gold = pre_gold[pre_gold.find("for")+4:pre_gold.find("GOLD")-1]
        return "{} BTC or {} GOLD".format(btc, gold)

    def search(self, param):

        if not self.terms[0]:
            return {"status" : "fail", "exception" : "An error ocurred in the acceptTerms function | {}".format(self.terms[1])}

        param = param.replace(" ", "+")

        try:

            response = self.session_obj.get("{}/search?search_request={}".format(self.url, param))
            parser = Soup(response.text, "lxml")

            result = []

            tables = parser.find_all("div", attrs={"class" : "ExploitTableContent"})

            for table in tables:
                rows = table.find_all("div", attrs={"class" : "td"})

                date = self.fixString(rows[0].getText())
                desc = self.fixString(rows[1].getText())
                platform = self.fixString(rows[2].getText())
                price = self.fixPrice(rows[9].getText())
                author = self.fixString(rows[10].getText())[0:self.fixString(rows[10].getText()).find("Exploits")]
                url = rows[1].find("a", href=True)["href"].replace("/description", "")

                result.append({"date" : date, "desc" : desc, "platform" : platform, "price" : price, "author" : author, "url" : self.url+url})
        
            return {"status" : "success", "response" : result}

        except Exception as err:
            return {"status" : "fail", "exception" : str(err)}
    
    def getIndex(self):

        if not self.terms[0]:
            return {"status" : "fail", "exception" : "An error ocurred in the acceptTerms function | {}".format(self.terms[1])}

        try:

            response = self.session_obj.get("{}".format(self.url))
            parser = Soup(response.text, "lxml")

            result = []

            tables = parser.find_all("div", attrs={"class" : "ExploitTableContent"})

            for table in tables:
                rows = table.find_all("div", attrs={"class" : "td"})

                date = self.fixString(rows[0].getText())
                desc = self.fixString(rows[1].getText())
                platform = self.fixString(rows[2].getText())
                price = self.fixPrice(rows[9].getText())
                author = self.fixString(rows[10].getText())[0:self.fixString(rows[10].getText()).find("Exploits")]
                url = rows[1].find("a", href=True)["href"].replace("/description", "")

                result.append({"date" : date, "desc" : desc, "platform" : platform, "price" : price, "author" : author, "url" : self.url+url})
        
            return {"status" : "success", "response" : result}

        except Exception as err:
            return {"status" : "fail", "exception" : str(err)}