# Reddit Front Page Scraper
Simple bot that scrapes and records unqiue submissions that are jpg's or png's from the top 100 posts of reddit.com/r/all every 10 minutes.

Uses reddit's API (via PRAW) and stores that information to a sqlite3 database.

**Currently this will only record unique submissions whose URL's point to a jpg or png file.**

This is a good base to work from if you are interested in datamining/scraping reddit.

# Setup

Because this script is scraping /r/all, it requires that you be logged into an account to see all content. Therefore you must setup OAuth with a reddit account, see PRAW's documentation for more information.

Setup your clients secrets in the secrets_rename.py file. Then rename it to secrets.py and you're good to go!

# Export the submissions data to csv

Via the command line, `cd` to the location of the database (the project directory). Then, use the following command:
```bash
sqlite3 -header -csv memer.db "select * from posts;" > out.csv
```
