import requests
import gzip
import shutil
import json
import jsonlines
import itertools
from collections import defaultdict

def get_org_index(list, name):
	for i, e in enumerate(list):
		if e['org'] == name:
			return i
	return -1

# download file
print("Downloading od-do-canada.jsonl.gz...")
url = 'https://open.canada.ca/static/od-do-canada.jsonl.gz'
r = requests.get(url, allow_redirects=True)
open('od-do-canada.jsonl.gz', 'wb').write(r.content)

#unzip file
print('Unzipping od-do-canada.jsonl.gz...')
with gzip.open('od-do-canada.jsonl.gz', 'r') as f_in, open('od-do-canada.jsonl', 'wb') as f_out:
  shutil.copyfileobj(f_in, f_out)

# count occurences of 'http:' in resource links per organization
print('Counting occurences of "http" in resource links...')
urls_count = []
urls_info = []
count = 0
with jsonlines.open('od-do-canada.jsonl') as reader:
  for obj in reader:
    for res in obj['resources']:
      
      org_index = get_org_index(urls_count, obj['organization']['title'])
      if org_index == -1:
        org_data = {
          'org': obj['organization']['title'],
          'http_count': 0,
          'ftp_count': 0,
          'total_count': 1
        }
        urls_count.append(org_data)
      else:
        urls_count[org_index]['total_count'] += 1
      
      #Look for http links
      if "http:" in res['url']:
        urls_count[org_index]['http_count'] += 1
        data = {
          'org': obj['organization']['title'],
          'title': res['name'],
          'url': res['url'],
          'url_type': 'http',
          'id': res['id'],
          'dataset': obj['title'],
          'dataset_id': obj['id'],
          'upload_date': 'portal_release_date' in obj
        }
        urls_info.append(data)

      #Look for FTP links
      if "ftp:" in res['url']:
        urls_count[org_index]['ftp_count'] += 1
        data = {
          'org': obj['organization']['title'],
          'title': res['name'],
          'url': res['url'],
          'url_type': 'ftp',
          'id': res['id'],
          'dataset': obj['title'],
          'dataset_id': obj['id'],
          'upload_date': 'portal_release_date' in obj
        }
        urls_info.append(data)
    if count % 1000 == 0:
      print('Processing dataset #{}'.format(count))
    count += 1

urls_count = [x for x in urls_count if x['http_count'] > 0 or x['ftp_count'] > 0]


sorted_urls_info = sorted(urls_info, key=lambda x : x['org'])
orgs_group = itertools.groupby(sorted_urls_info, lambda x : x['org'])
orgs_data_array = {}
for org, group in orgs_group:
    orgs_data_array[org] = list(group)


#write detailed http resources file 
jsonString = json.dumps(orgs_data_array)
jsonFile = open("orgs_http_data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()

#write org count file 
jsonString = json.dumps(urls_count)
jsonFile = open("orgs_with_http.json", "w")
jsonFile.write(jsonString)
jsonFile.close()


print('Processing done.')
