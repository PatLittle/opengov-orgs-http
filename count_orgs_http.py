import requests
import gzip
import shutil
import json
import jsonlines
import collections
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
urls_d = defaultdict(int)
count = 0
with jsonlines.open('od-do-canada.jsonl') as reader:
    for obj in reader:
      for res in obj['resources']:
        if "http:" in res['url']:
          urls_d[obj['organization']['title']] += 1
      if count % 1000 == 0:
        print('Processing dataset #{}'.format(count))
      count += 1

# print(urls_d)
with open('orgs_with_http.json', 'w') as f:
    json.dump({k: v for k, v in sorted(urls_d.items(), key=lambda item: item[1], reverse=True)}, f, indent=2)

print('Processing done.')
