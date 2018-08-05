import time
import json
import requests


from urllib.parse import urlencode
from urllib.request import Request, urlopen

response = requests.post("https://symbiote-open.man.poznan.pl/coreInterface/get_guest_token")

x_auth_token = response.headers["x-auth-token"]
#print("Auth Token: " + x_auth_token)

x_auth = { "token" : x_auth_token, "authenticationChallenge":"", "clientCertificate":"", "clientCertificateSigningAAMCertificate":"", "foreignTokenIssuingAAMCertificate":"" }
security_header = { "x-auth-timestamp" : str(int(round(time.time()*1000))), "x-auth-size" : "1", "x-auth-1" : json.dumps(x_auth) }

#url = "https://symbiote-open.man.poznan.pl/coreInterface/query?location_name=*Vienna*"
#url = "https://symbiote-open.man.poznan.pl/coreInterface/query?platform_name=AITopenUwedat"
#url = "https://symbiote-open.man.poznan.pl/coreInterface/query?id=5adf03733a6fd8053048643d"
url = "https://symbiote-open.man.poznan.pl/coreInterface/query?location_name=*Vienna*"

print()
#Preparing and executing a query
response = requests.get(url,headers=security_header)
print(response)
json_data_one = json.loads(response.text)
print("All possible data (platforms, places, etc): ")
#print(json_data_one)

sensor_urls = []
print()
counter = 0
lista = json_data_one["body"]
for id in lista:
    id = lista[counter]["id"]
    sensor_urls.append(id)
    counter+=1


#Retrieving sensor readings
#BROKENresponse = requests.get("https://enviro5.ait.ac.at/symbiote/rap/Sensors('5adf03733a6fd8053048643d')/Observations",headers=security_header)
#response = requests.get("https://enviro5.ait.ac.at/symbiote/rap/Sensors('5ae189913a6fd8053048662f')",headers=security_header)
#response = requests.get("https://symbiote.connectedcitizen.eu/rap/Sensors('5b0fc6d73a6fd84439337eab')/Observations?$top=3",headers=security_header)

sensor_finals = []

for element in sensor_urls:
    new_link = "https://symbiote-open.man.poznan.pl/coreInterface/resourceUrls?id="+element
    response = requests.get(new_link,headers=security_header)
    #print(response)
    json_data_two = json.loads(response.text)
    item = json_data_two["body"][element]
    sensor_finals.append(item)

print()

counter = 0
for item in sensor_finals:
    string_url = item+"/Observations?$top=1"
    response = requests.get(string_url,headers=security_header)
    json_data_three = json.loads(response.text)
    print(json_data_three)
    print()
    #print(json_data_three[counter])
    #counter+=1

    print()
    #item = json_data_three["body"][element]
