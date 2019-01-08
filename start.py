
from LibToday import HttpApi, CMD
from sys import argv
from os import name, popen, system as UnsafeCommand

global allowed_commands
global system
global ver

ver = "0.1b"
allowed_commands = ["cls", "clear"]

def SecureCommand(command, get_output=False):

    if not type(command) == str: CMD().p_error("Invalid command: {} | The command need to be a str".format(str(command)))
    
    if not command.replace(" ", "") in allowed_commands: CMD().p_error("Command not allowed | Command couldn't be executed | Command: {}".format(command))
    
    try:
        if get_output:
            system = popen(command)
        else:
            UnsafeCommand(command)
    except Exception:
        return False

    if get_output:
        return system.read()
    
    return True

system = SecureCommand

def ClearCMD():
    if name == "nt":
        system("cls")
    else:
        system("clear")

def CheckIpStruct(ip_str):
    
    ip = ip_str.split(".")

    if len(ip) != 4:    return False

    for a in ip:
         
        if a.replace(" ", "") != "":
            try:
                int(a)
            except Exception:
                return False
        else:   return False
        
        return True

def CheckPort(port_str):

    try:
        int(port_str)
        return True
    except Exception: return False

def GetOptions():


    if not len(argv) >= 3:
        CMD().p_error("Some args are not satisfied | Usage {} ip port key | key is optional and seted by default as 'sike'".format(argv[0]))

    ip = argv[1]
    port = argv[2]
    
    if len(argv) >= 4:   key = argv[3]
    else:   key = "sike"
    
    if not CheckIpStruct(ip):
        CMD().p_error("{} is an invalid ip address | Example: 127.0.0.1 or 192.168.1.23")
    
    if not CheckPort(port):
        CMD().p_error("{} is an invalid port | Example:  8080 or 80")
    
    return {"ip" : ip, "port" : port, "key" : key}

ClearCMD()
CMD().p_welcome("Welcome to the unofficial 0day.today search api | Version: {}".format(ver))
options = GetOptions()

HttpApi(ip=options["ip"], port=options["port"], key=options["key"], ver=ver).Start()