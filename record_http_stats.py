import csv
import json
from datetime import datetime

input_file = open('orgs_with_http.json')
dep_array = json.load(input_file)
date = datetime.today().strftime('%Y-%m-%d')

with open('orgs_http_stats.csv', 'a', newline='') as f:
    writer = csv.writer(f)

    for item in dep_array:
        writer.writerow([date, item['org'].split(' | ')[0], item['http_count'], item['ftp_count']])

