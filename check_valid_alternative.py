import requests
import json

# loops through all http and ftp links and test if there is a valid https alternative URL already.
# output is saved in a json file, to be later consumed by the javascript files on page load.

f = open('orgs_http_data.json')
data = json.load(f)

count = 0
https_count = []
for org in data:
  org_https_count = {
    'org': org,
    'https_alternative_count': 0,
    'urls': []
  }
  for res in data[org]:
    count += 1
    if count % 50 == 0:
      print('processing resource', count)

    try:
      https_url = res['url'].replace('http://', 'https://').replace('ftp://', 'https://')
      response = requests.head(https_url, timeout=4)
      if response.status_code < 400:
        org_https_count['https_alternative_count'] += 1
        org_https_count['urls'].append(res['url'])
    except Exception as e:
        continue
  
  https_count.append(org_https_count)

print('Done.')
f.close()

#write org count file 
jsonString = json.dumps(https_count)
jsonFile = open("https_alternative_count.json", "w")
jsonFile.write(jsonString)
jsonFile.close()


