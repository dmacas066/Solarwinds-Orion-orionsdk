import requests
from orionsdk import SwisClient
import getpass


#Opening path to a host file with list of hostnames/IPs, stripping any whitespace, new line per host
hosts = open('PATH_TO_FILE', 'r')
hosts = hosts.read()
hosts = hosts.strip().splitlines()


#Details for connecting with the NPM server
npm_server = 'IP ADDRESS'
username = input('Enter your username: ')
password = getpass.getpass('Enter your password: ')

#Ignore any Certifcate not secure warnings
verify = False
if not verify:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#creating variable for calling the SwisClient function
swis = SwisClient(npm_server, username, password)

print("Querying Uris:")
#Looping through host file to query each host for its Uri
for host in hosts:
    results = swis.query("SELECT Uri FROM Orion.Nodes WHERE SysName ='{}'".format(host))
    for row in results['results']:
        print("{Uri}".format(**row))

