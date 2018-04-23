import praw
import sqlite3
from datetime import datetime 
import time
import sys
import secrets

###############################################################################

#May get an error from this...
def print_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

###############################################################################

def is_an_image(url):
	if url[-3:] in ['jpg', 'png'] or url[-4:] in ['jpeg']:
		return True
	return False

###############################################################################

def human_time(time):
	hours = int(time)
	minutes = (time*60) % 60
	seconds = (time*3600) % 60
	return "%d hr %02d mins %02d sec" % (hours, minutes, seconds)

def get_avg_created_to_front():
	cursor.execute('select AVG(discovered - created_utc)/60/60.0 from posts;')
	return cursor.fetchone()[0]


def get_avg_front_life():
	cursor.execute('select AVG(lastseen - discovered)/60/60.0 from posts;')
	return cursor.fetchone()[0]

###############################################################################

def is_id_in_db(sub):
	cursor.execute('SELECT EXISTS(SELECT 1 FROM posts WHERE id=?)', (sub.id,))
	return bool(cursor.fetchone()[0])
	
def add_sub_to_db(sub):
	cursor.execute(
		'INSERT INTO posts (id, title, url, subreddit, subreddit_id, created_utc, discovered) VALUES (?, ?, ?, ?, ?, ?, ?)',
		(
			sub.id,
			sub.title,
			sub.url,
		   	str(sub.subreddit),
		    sub.subreddit_id,
		    int(sub.created_utc),
			int(time.time())
		)
	)
	conn.commit()

def update_lastseen(sub):
	cursor.execute(
		'UPDATE posts SET lastseen=? WHERE id=?',
		(int(time.time()), sub.id)
	)
	conn.commit()

###############################################################################


#db will be creating if it does not exist
conn = sqlite3.connect("memer.db", timeout=11)
cursor = conn.cursor()

#to export the sqlite3 database/table to csv,
#via the command line use the following command
#sqlite3 -header -csv memer.db "select * from posts;" > out.csv

#Creates the posts table if we don't have it
#NOTE: Does not check for changes to table schema
cursor.execute('SELECT count(*) FROM sqlite_master WHERE type=? AND name=?;',('table', 'posts'))

if cursor.fetchone()[0] == 0:
	print('Database does not contain submissions table, creating.')
	create_posts_table = """
		CREATE TABLE posts (
			id text PRIMARY KEY,
			title text,
			url text, 
			subreddit text,
			subreddit_id text,
			created_utc integer, 
			discovered integer, 
			lastseen integer
		);"""

	cursor.execute(create_posts_table)

while True:
 
	try:
		r = praw.Reddit(
				client_id = secrets.client_id,
				client_secret = secrets.client_secret,
				password = secrets.password,
				user_agent = 'PotableWater front page scrapper',
				username = secrets.username
				)

		submissions = r.subreddit('all').hot(limit=100);
		
		total_sub_count = 0
		new_sub_count = 0

		print('')

		for submission in submissions:
			total_sub_count += 1

			if submission.is_self or not is_an_image(submission.url):
				continue

			if not is_id_in_db(submission): #if id is not in db then add data
				add_sub_to_db(submission)
				new_sub_count += 1
			else:
				update_lastseen(submission)

		print('{}: Found {} of {} new posts, sleeping after report;'.format(str(datetime.now()), new_sub_count, total_sub_count))
		print('Avg time to get to front page: {}'.format(human_time(get_avg_created_to_front())))
		print('Avg life span on front page: {}'.format(human_time(get_avg_front_life())))
		
	except:
		print_exception()
	
	time.sleep(600)