import smtplib
import requests
import bs4
import os
import re
import json
from email.mime.text import MIMEText

# adapter
with open('./watchAuthors.json', 'r') as f:
    args = json.loads(f.read())
    old_total = args['total']
    names = args['names']
    surnames = args['surnames']

receivers = ['EMAIL_ADDRESS_TO_NOTIFY', 'ANOTHER_ADDRESS_TO_NOTIFY']

link = "https://arxiv.org/search/advanced?advanced="
for idx, (name, surname) in enumerate(zip(names, surnames)):
    link += "&terms-"+str(idx)+"-operator=OR&terms-"+str(idx)+"-term="+name+"%2C+"+surname+"&terms-"+str(idx)+"-field=author"

link += "&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=2021&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=100&order=-announced_date_first"


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

res = requests.get(link, headers=headers)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, features="html.parser")
results = soup.select('li.arxiv-result')
new_total = soup.select('h1.title')[0].getText()
new_total = re.findall(r'\s\d+\s', new_total)[0].strip()
new_total = int(new_total)


with open('./watchAuthors.json', 'w') as json_file:
    new = {'total': new_total, 'names': names, 'surnames': surnames}
    json.dump(new, json_file, indent=4)


diff = new_total - old_total
i = 0


lead_authors = [] 
if diff > 0:
    while diff > 0:

        title = results[i].select('p.title')
        latest_title = title[0].getText().strip()
        
        authors = results[i].select('p.authors')
        authors = authors[0].getText()
        authors = re.findall(r'\w+\s\w+', authors)

        authors_lower = []
        for j in range(len(authors)):
            authors_lower.append(authors[j].lower())    

        for surname, name in zip(surnames, names):
            full_name = surname+' '+name
            full_name = full_name.lower()
            if full_name in authors_lower:
                lead_authors.append(name)

        authors = ', '.join(authors)
        
        latest = results[i].select('p > a')
        latest_link = latest[0].attrs['href']

        res2 = requests.get(latest_link, headers=headers)
        res2.raise_for_status()
        soup2 = bs4.BeautifulSoup(res2.text, features="html.parser")

        abstract = soup2.select('blockquote.abstract')
        abstract = abstract[0].getText().strip()

        if i==0:
            mail = 'Hi Team,\n\n' + \
                   'A new article was just uploaded on arxiv!\n\nTitle : ' + latest_title + '\n\nAuthors : ' + \
                    authors + '\n\n' + abstract + '\n\nLink : ' + latest_link 
        else:
            mail = mail + \
                '\n\nAnd also this one :\n\nTitle : ' + latest_title + '\n\nAuthors : ' + \
                    authors + '\n\n' + abstract + '\n\nLink : ' + latest_link 
        
        diff -= 1
        i += 1
    
    mail = mail + '\n\nCordially,\nBOT NAME'
    msg = MIMEText(mail)
    lead_authors = ', and also from '.join(lead_authors)
    msg['Subject'] = 'New article from '+lead_authors+'!' 
    msg['From'] = 'BOT NAME'
    msg['To'] = ','.join(receivers)
    
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('BOT_MAIL_ADDRESS', 'PASSWORD')
    smtpObj.sendmail('BOT_MAIL_ADDRESS',
                     receivers, msg.as_string())
    smtpObj.quit()
