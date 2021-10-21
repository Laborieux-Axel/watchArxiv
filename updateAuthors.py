import sys
import smtplib
import requests
import bs4
import os
import re
import json
from email.mime.text import MIMEText

# adapter
with open('/Users/axellaborieux/watchArxiv_perso/watchAuthors.json', 'r') as f:
    args = json.loads(f.read())
    old_total = args['total']
    names = args['names']
    surnames = args['surnames']

if sys.argv[1]=='add':
    names.append(sys.argv[3])
    surnames.append(sys.argv[2])
elif sys.argv[1]=='remove':
    names.remove(sys.argv[3])
    surnames.remove(sys.argv[2])
else:
    print('something is not right, exiting!')
    exit()

link = "https://arxiv.org/search/advanced?advanced="
for idx, (name, surname) in enumerate(zip(names, surnames)):
    link += "&terms-"+str(idx)+"-operator=OR&terms-"+str(idx)+"-term="+name+"%2C+"+surname+"&terms-"+str(idx)+"-field=author"


link += "&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=2021&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=100&order=-announced_date_first"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

res = requests.get(link, headers=headers)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, features="html.parser")
results = soup.select('li.arxiv-result')
new_total = soup.select('h1.title')[0].getText().strip()
new_total = new_total.split(' ')
new_total = int(new_total[3].replace(',', ''))

with open('/Users/axellaborieux/watchArxiv_perso/watchAuthors.json', 'w') as json_file:
    new = {'total': new_total,
           'names': names,
           'surnames': surnames}
    json.dump(new, json_file, indent=4)

print('Succesfully updated total from {} to {}!'.format(old_total, new_total))
