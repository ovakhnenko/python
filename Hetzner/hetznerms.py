import time
import re
import random
import sys

file_path = "hetzner.ip"
ip_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
ips = ["111.111.111.111", "112.112.112.112", "113.113.113.113", "114.114.114.114", "115.115.115.115"]

def get_active_ip_addresses(file_path):

    #resp = requests.post('https://robot-ws.your-server.de/rdns/123.123.123.123', data={'ptr':'testen.de'}, auth=(USER, PASS))
    
    try:
        with open(file_path, 'r') as file:
                result = file.readline().strip()
        if not re.match(ip_pattern, result):
            result = ips[0]
    except Exception as e:
        result = ips[0]
    
    return result

def ip_verfuegbar_pruefen(ip):
    
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.settimeout(timeout)
    
    #try:
    #    s.connect((ipOrName, int(port)))
    #    s.shutdown(socket.SHUT_RDWR)
    #    return True
    #except:
    #    return False
    #finally:
    #    s.close()
    
    return random.random() < 0.8

def get_naechste_verfuegbare_ip(ip):

    index = ips.index(ip)

    for i in range(index + 1, len(ips)):
        ip_neu = ips[i]
        if ip_verfuegbar_pruefen(ip_neu):
            print("  test -> " + ip_neu + " ist verfügbar und neue ip adresse\n")
            return ip_neu
        else:
            print("  test -> " + ip_neu + " ist unverfügbar")    

    for i in range(0, index - 1):
        ip_neu = ips[i]
        if ip_verfuegbar_pruefen(ip_neu):
            print("  test -> " + ip_neu + " ist verfügbar und neue ip adresse\n")
            return ip_neu
        else:
            print("  test -> " + ip_neu + " ist unverfügbar")    

    print("  test -> test war unerfolgreich\n")    
    return ip_neu

def set_active_ip_adresse(ip):

    with open(file_path, 'w') as file:
        file.write(ip)

def failover_ip_pruefen():

    ip = get_active_ip_addresses(file_path)
    if not ip_verfuegbar_pruefen(ip):
        print(ip + " ist unverfügbar ->\n")
        ip = get_naechste_verfuegbare_ip(ip)
        set_active_ip_adresse(ip)
    else:
        print(ip + " ist verfügbar")    

def get_meine_ip():

    return "112.112.112.112"

def gibt_es_lebende():

    lebende = 0
    
    for ip in ips:
        if ip_verfuegbar_pruefen(ip):
            lebende += 1

    if lebende == 1:
        set_active_ip_adresse(get_meine_ip())
        print("  ** ich bin der letzte **")
        return False
    else:
        print("  lebende hosts: ", lebende)
        return True

#while True:
    #if gibt_es_lebende():
    #    failover_ip_pruefen()
    #time.sleep(1)  

arguments = sys.argv
print(arguments)

index = arguments.index("--master") # master ip lesen
if index > 0:
    ip_master = arguments[index + 1]
    #ip_master_passt = re.match(ip_pattern, ip_master)

index = arguments.index("--failover") # failover ip lesen
if index > 0:
    ip_failover = arguments[index + 1]
    #ip_failover_passt = re.match(ip_pattern, ip_failover)

index = arguments.index("--slaves") # slave ips lesen
if index > 0:
    ip_slaves = arguments[index + 1].strip('[]').split(',')

print("master ip   : ", ip_master)
print("slaves ip   : ", ip_slaves)
print("failover ip : ", ip_failover)
