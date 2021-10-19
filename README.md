# watchArxiv

## Basic idea

Using python to automatically scrape arXiv everyday and be notified by email 
whenever a specific author upload a paper. 
The repository is not usable as is and has to be adapted to your specfic case. 
You should create a specific gmail account and go to the security settings to 
allow programs to login.
The script works as follows: a list of authors is kept in `watchAuthors.json`
 as well as the total of articles uploaded on arxiv by them so far.
The script does a request to an advanced search on arxiv for all those authors
and look at the total of articles. 
If it is greater than the stored total, then the difference corresponds to 
newly updated papers and can be extracted from the search and sent by email.
The total is then updated.

## Setting the environment

The script requires `requests` for getting the html document from arxiv
 and `beautifulsoup4` to parse the html and manipulate it.

```
python3 -m venv myenv
source myenv/bin/activate
pip install --upgrade pip setuptools
pip install requests
pip install beautifulsoup4
```

## Adding authors to follow

The followed authors are kept into `watchAuthors.json`, as well as the current
total of articles uploaded on arxiv by them.
To start adding authors (one at a time), run:
```
python addAuthor.py First_name Last_name
```
It should output the new total of articles uploaded by the followed authors 
on arixv. 

## Adapt to your case

In `watchAuthors.py`, replace the uppercase placeholders by your data.

## Adapt the shell script

Adapt `watchArxiv.sh` with your paths.

## Set the cron job

Now you just have to make the shell script execute automatically at the frequency
of your choice. 
Run `crontab -e` in the terminal and put something like:

```
0 9 * * * /absolute/path/to/watchArxiv.sh
```

This will launch the script everyday at 9:00am.
