#############################
# 0day.today unofficial api #
#       By MrSentex         #
#############################

##############################################
#          <- Disclaimer ->                  #
# This API is not official and should not be #
# used without the consent of "0day.today".  #
# MrSentex is not responsible for any        #
# non-consensual use of the API. In the      #
# case of non-consensual use of the API,     #
# the utlizador will be responsible for      #
# the usage.                                 #
##############################################

# <- Api0day imports ->
from selenium import webdriver
from bs4 import BeautifulSoup as Soup
from codecs import ascii_encode
from unidecode import unidecode
from time import time
from os.path import devnull
# <- Api0day imports ->

# <- HttpApi imports ->
from flask import Flask, request, redirect, jsonify
import logging
# <- HttpApi imports ->

# <- CMD imports ->
from colorama import init, Fore
init()
from os import _exit as kill
# <- CMD imports ->

class CMD(object):

    def __init__(self):
        self.info = "[" + Fore.BLUE + "INFO" + Fore.RESET + "] "
        self.error = "[" + Fore.RED + "ERROR" + Fore.RESET + "] "
        self.correct = "[" + Fore.GREEN + "SUCCESS" + Fore.RESET + "] "
        self.welcome = "[" + Fore.LIGHTCYAN_EX + "WELCOME" + Fore.RESET + "] "    

    def p_info(self, msg):
        print self.info  + str(msg)
    
    def p_error(self, msg):
        print self.error + str(msg)
        kill(1)
    
    def p_correct(self, msg):
        print self.correct + str(msg)

    def p_welcome(self, msg):
        print self.welcome + str(msg)

class Api0day(object):

    def __init__(self, search_param):

        self.url = "https://0day.today"
        self.search_param = search_param.replace(" ", "+")
        try:
            self.driver = webdriver.PhantomJS(service_log_path=devnull)
            self.result = self.Search()
        except Exception as err:
            self.result = {"status" : "fail", "exception" : str(err)}
    
    def ClickButton(self, button_name):
        trys = 0
        while True:
            try:
                button = self.driver.find_element_by_name(button_name)
                button.click()
                return True
            except Exception:
                if trys >= 50:
                    return False
                trys += 1
                pass
    
    def FixString(self, string):

        string = ascii_encode(unidecode(string.replace("\n", "").replace("\t", "")))[0]

        if string.find("Comments:") != -1:
            string = string[:string.find("Comments: {}".format(string[string.find("Comments:")+10:string.find("Comments:")+len(string)-string.find("Comments:")-1]))]

        if string.find("Rate down:") != -1:
            string = string[:string.find("Rate down: {}".format(string[string.find("Rate down:")+11:string.find("Rate down:")+len(string)-string.find("Rate down:")-1]))]
        
        if string.find("Rate up:") != -1:
            string = string[:string.find("Rate up: {}".format(string[string.find("Rate up:")+9:string.find("Rate up:")+len(string)-string.find("Rate up:")-1]))]

        return string
    
    def FixPrice(self, price):

        price = self.FixString(price)

        if price.startswith("free"):
            return "free"

        btc = price[price.find("BTC")-2:price.find("BTC")-1]
        gold = price[price.find("GOLD")-2:price.find("GOLD")-1]

        return "{} BTC or {} GOLD".format(btc, gold)

    def BypassCF(self):

        self.driver.get(self.url)

        if self.ClickButton("agree"):
            return True
        return False

    def Search(self):

        if not self.BypassCF():
            return {"status" : "fail", "exception" : "Program couldn't bypass cloudflare security"}

        try:

            result = {"status" : "success", "response" : []}

            self.driver.get("{}/search?search_request={}".format(self.url, self.search_param))

            html_parser = Soup(self.driver.page_source, "lxml")

            tables = html_parser.find_all("div", attrs={"class" : "ExploitTableContent"})

            for table in tables:
                rows = table.find_all("div", attrs={"class" : "td"})

                date = self.FixString(rows[0].getText())
                desc = self.FixString(rows[1].getText())
                platform = self.FixString(rows[2].getText())
                price = self.FixPrice(rows[9].getText())
                author = self.FixString(rows[10].getText())[0:self.FixString(rows[10].getText()).find("Exploits")]
                url = rows[1].find("a", href=True)["href"].replace("/description", "")

                result["response"].append({"date" : date, "desc" : desc, "platform" : platform, "price" : price, "author" : author, "url" : self.url+url})
            
            return result
        
        except Exception as e:
            return {"status" : "fail", "exception" : str(e)}

    def GetResult(self):
        return self.result

    def CloseDriver(self):
        self.driver.quit()

class HttpApi(object):

    def __init__(self, ip, port, key, ver):

        self.ip = ip
        self.port = int(port)
        self.key = key
        self.ver = ver
    
    def GetCheck(self, data_array):

        for a in data_array:
            if a == None:
                return False
            if a.replace(" ", "") == "":
                return False 
        return True

    def Start(self):

        CMD().p_info("Starting the HttpApi in http://{}:{} | Key = {}\n".format(self.ip, self.port, self.key))

        api = Flask(__name__)

        @api.route("/test-conn")
        def test_conn():
            key = request.args.get("key")

            if key != self.key:
                return jsonify({"status" : "fail", "exception" : "Invalid key"})

            return jsonify({"status" : "success", "ver" : self.ver})
            
        @api.route("/search")
        def search():

            key = request.args.get("key")
            search_param = request.args.get("search_param")

            if not self.GetCheck([key, search_param]):
                return jsonify({"status" : "fail", "exception" : "Some fields are in blank"})
            
            if key != self.key:
                return jsonify({"status" : "fail", "exception" : "Invalid key"})
            
            search = Api0day(search_param)
            search.CloseDriver()
            return jsonify(search.GetResult())
        
        @api.route("/")
        def index():
            return redirect("https://github.com/MrSentex")
        
        try:
            api.logger.disabled = True
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)
            log.disabled = True
            api.run(host=self.ip, port=self.port, threaded=True)
            print("\n")
            CMD().p_correct("The HttpApi start correctly")
        except Exception as err:
            print("\n")
            CMD().p_error(err)