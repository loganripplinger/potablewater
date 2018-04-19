# reddit data miner
Simple bot that scrapes and records unqiue submissions that are jpgs from top 100 posts from reddit.com/r/all every 10 minutes.

Uses reddit's API (via PRAW) and stores that information to a sqlite3 database.

Currently setup to only record unique submissions whose URL points to a jpg file.

This is a good base to work from if you are interested in datamining reddit.