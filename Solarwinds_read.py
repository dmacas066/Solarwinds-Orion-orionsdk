import requests
from orionsdk import SwisClient
import getpass

# Creating a variable for a file with a list of hostnames/IP addresses to use in a readable manner
hosts = open('\\PATH_TO_FILE', 'r')
hosts = hosts.read()
hosts = hosts.strip().splitlines()
#Creating another variable to store the output of the code
myfile = open('\\PATH_TO_FILE', 'a')

#Creating more variables for use with authenticating to to NPM server.
npm_server = 'IP ADDRESS/Hostname'
username = input('Enter your username: ')
password = getpass.getpass('Enter your password: ')

#Ignoring any Certificate not secure warnings
verify = False
if not verify:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#Creating a variable to use with the SwisClient function, passing through the variables created earlier
swis = SwisClient(npm_server, username, password)
#Message to print to console to let you know where we are at
print("Trying to read URIs, if an issue occurs, a message will appear in console")
myfile.write('________________________________________________________________________________')

#Now we are going to use a for loop to iterate over each host in the hosts file (every new line is a new host in my case,
#as should be in yours, if you decide to use a similar method
for host in hosts:
#I am using the try and except because I had an Error thrown to me in cases where the host did not exist within Solarwinds
    try:
        #So creating more variables, this query will actually query Solarwinds for data within the orion.nodes container where the sysname is =
        #to the hostname of the hosts in my hosts file
        query = swis.query("SELECT Uri FROM Orion.Nodes WHERE SysName ='{}'".format(host))
        #results will read the results of the above query and filter out specifically the URI used to obtain device details for the node
        results = swis.read(query['results'][0]['Uri'])
        #further filtering the results so that i have a tidy list of dictionary values with the key : value on its own line 
        output = results.items() 
        #using a for loop to iterate through the dictionary values  
        for key, value in output:
            #printing out the values in a file        
            myfile.write('\n {}'.format(key) + ' {}'.format(value))
        myfile.write('\n________________________________________________________________________________')
    #if something goes wrong the except block will catch the error and simply print out that something went wrong with whatever
    #device had the issue    
    except:
        print("Something went wrong")
        myfile.write("\nSomething went wrong with Device {}".format(host))
        myfile.write('\n________________________________________________________________________________')
        continue
#lines used to seperate host details          
myfile.write('\n________________________________________________________________________________')      