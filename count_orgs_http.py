import requests
import gzip
import shutil
import json
import jsonlines
import itertools
from collections import defaultdict

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
urls_count = defaultdict(int)
count = 0
urls_info = []
with jsonlines.open('od-do-canada.jsonl') as reader:
    for obj in reader:
      for res in obj['resources']:
        if "http:" in res['url']:
          urls_count[obj['organization']['title']] += 1
          data = {
            'org': obj['organization']['title'],
            'title': res['name'],
            'url': res['url'],
            'id': res['id'],
            'dataset': obj['title'],
            'dataset_id': obj['id']
          }
          urls_info.append(data)
      if count % 1000 == 0:
        print('Processing dataset #{}'.format(count))
      count += 1

sorted_urls_info = sorted(urls_info, key=lambda x : x['org'])
orgs_group = itertools.groupby(sorted_urls_info, lambda x : x['org'])
orgs_data_array = {}
for org, group in orgs_group:
    orgs_data_array[org] = list(group)


#write file 
jsonString = json.dumps(orgs_data_array)
jsonFile = open("orgs_http_data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()

with open('orgs_with_http.json', 'w') as f:
    json.dump({k: v for k, v in sorted(urls_count.items(), key=lambda item: item[1], reverse=True)}, f, indent=2)

print('Processing done.')
