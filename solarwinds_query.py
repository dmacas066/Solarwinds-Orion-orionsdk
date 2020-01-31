import requests
from orionsdk import SwisClient
import getpass

#Creating variable for file with hostnames/IP addresses, getting rid of whitespace and new line for each host
hosts = open('PATH_TO_FILE', 'r')
hosts = hosts.read()
hosts = hosts.strip().splitlines()
#Creating variables for details used to connect to NPM Server
npm_server = 'IP ADDRESS'
username = input('Enter your username: ')
password = getpass.getpass('Enter your password: ')
#Ignore any Certificate insecure warnings
verify = False
if not verify:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#Variable for SwisClient, passing through variables created above
swis = SwisClient(npm_server, username, password)

print("Querying Devices:")
#For loop to iterate through hosts
for host in hosts:
    #Variable for the results of a query, looking for DisplayName & Uri
    results = swis.query("SELECT DisplayName, Uri FROM Orion.Nodes WHERE SysName ='{}'".format(host))
    #If device is not found, the value of dictionary key will be [], so this will catch those   
    if results['results'] == []:
        print("Not Found")
    #Else print out the key, value on each row in results    
    else:
        for row in results['results']:       
            print("{DisplayName} : {Uri}".format(**row))
