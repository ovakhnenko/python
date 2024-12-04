import smtplib
import argparse
import requests
import subprocess
from requests.auth import HTTPBasicAuth
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

ROBOT_USERNAME = 'xxx'
ROBOT_PASSWORD = "yyy"

def ping(host):
	command = ['ping','-c 1',host]
	return subprocess.call(command) == 0

def hz_getauth():
	return HTTPBasicAuth(ROBOT_USERNAME, ROBOT_PASSWORD)

def hz_callgetapi(url):
	api_url=f"https://robot-ws.your-server.de{url}"
	response=requests.get(api_url,auth=hz_getauth())
	return response.json()

def hz_callpostapi(url,payload):
	api_url=f"https://robot-ws.your-server.de{url}"
	response=requests.post(api_url,auth=hz_getauth(),data=payload)
	return response.json()

def csv_list(string):
	return string.split(",")

def send_email(to_email, to_subject, to_message):
	sender_email = "xxx"
	password = "yyy"
	smtp_server = "smtp.ionos.de"
	smtp_port = 587

	message = MIMEMultipart()
	message["From"] = sender_email
	message["To"] = to_email
	message["Subject"] = to_subject
	message.attach(MIMEText(to_message, "plain"))

	with smtplib.SMTP(smtp_server, smtp_port) as server:
		server.starttls()
		server.login(sender_email, password)
		server.sendmail(sender_email, to_email, message.as_string())

parser=argparse.ArgumentParser(description="Comnovis Hetzner Failover Agent")
parser.add_argument("--master",default="111.111.192.66")
parser.add_argument("--failover",default="111.111.234.182")
parser.add_argument("--slaves","-l",type=csv_list,default="111.111.64.209")
args=parser.parse_args()

slave_erreichbar = True
master_erreichbar = ping(args.master)
failover_erreichbar = ping(args.failover)

print (f"Host {args.master} erreichbar? : {master_erreichbar}\n")
print (f"Host {args.failover} erreichbar? : {failover_erreichbar}\n")

api_failover = hz_callgetapi(f"/failover/{args.failover}") #status for failover
print ("Aktuelles Ziel von {args.failover}: ",api_failover["failover"]["active_server_ip"])

if master_erreichbar & (api_failover["failover"] == args.master):
	print("Master {args.master} ist erreichbar und ausfallsicher.")
elif master_erreichbar & (api_failover["failover"] != args.master):
	#api_failover = hz_callgetapi(f"/failover/{args.failover} -d active_server_ip={args.master}") #switch failover
	print("Failover-IP {args.failover} wurde zurück auf den Master umgeschaltet.")
	send_email("technik@comnovis.de", "Test Failover IP", "Failover-IP {args.failover} wurde zurück auf den Master umgeschaltet.")
else:
	for slave in args.slaves:
		slave_erreichbar = ping(slave)
		if slave_erreichbar:
			#api_failover = hz_callgetapi(f"/failover/{args.failover} -d active_server_ip={slave}") #switch failover 
			print("Failover IP wurde auf den Slave {slave} umgeschaltet.")
			send_email("technik@comnovis.de", "Test Failover IP", "Failover IP wurde auf den Slave {slave} umgeschaltet.")
			break

if not slave_erreichbar:
	print("Master und Slave(s) sind nicht verfügbar.")
	send_email("technik@comnovis.de", "Test Failover IP", "Master und Slave(s) sind nicht verfügbar.")

api_rdns = hz_callpostapi(f"/rdns/{args.failover}",{"ptr":"vpn-cloud-master.session.de"}) #RDNS
