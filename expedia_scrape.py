import requests
import json

#https://www.expedia.com/Fortaleza-Hotels-Beach-Park-Oceani-Hotel.h5389392.Hotel-Information?&chkin=11/14/2018&chkout=11/17/2018&rm1=a2&exp_dp=129.42&exp_ts=1539527422076&exp_curr=USD&swpToggleOn=false&exp_pg=HSR

hotel_id = "5389392"  #ID do Hotel Oceani no Expedia
start_date = "03/14/2019"
end_date = "03/17/2019"


base_url = f"https://www.expedia.com/api/hotels/pricehotel/{hotel_id}"
query_string = f"?start={start_date}&end={end_date}&channel=2&_=153952770102"

base_url2 = f"https://www.expedia.com/Fortaleza-Hotels-Beach-Park-Oceani-Hotel.h{hotel_id}.Hotel-Information"
query_string2 = f"?&chkin={start_date}&chkout={end_date}&rm1=a2&exp_dp=129.42&exp_ts=1539527422076&exp_curr=USD&swpToggleOn=false&exp_pg=HSR"

url = base_url + query_string
url2 = base_url2 + query_string2

response = requests.get(url)
response2 = requests.get(url2)

data = response.json()
html = response2.text

print(json.dumps(data, indent=4))  #Identação do json

#for line in html.split('\n'):
#	if 'var roomsAndRatePlans' in line:
#		quartos = line[24:-1]

#print(quartos)

#quartos2 = (json.loads(quartos))

#print(json.dumps(quartos2, indent=4))