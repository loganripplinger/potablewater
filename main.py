import praw
import sqlite3
from datetime import datetime 
import time
import sys
import secrets

#db will be creating if it does not exist
conn = sqlite3.connect("memer.db", timeout=11)
cursor = conn.cursor()

#Create the posts table if we don't have it
table_name = "posts"
cursor.execute('SELECT count(*) FROM sqlite_master WHERE type=? AND name=?;',('table', table_name))

if cursor.fetchone()[0] == 0:
	print('Database does not contain submissions table, creating.')
	create_posts_table = """
		CREATE TABLE posts (
			id text PRIMARY KEY,
			url text, 
			created_utc integer, 
			discovered integer, 
			lastseen integer
		);"""

	cursor.execute(create_posts_table)


def is_an_image(url):
	if url[-3:] in ['jpg', 'png'] or url[-4:] in ['jpeg']:
		return True
	return False


def id_in_db(sub):
	cursor.execute('SELECT EXISTS(SELECT 1 FROM posts WHERE id=?)', (sub.id,))
	return bool(cursor.fetchone()[0])
	
def add_sub_to_db(sub):
	cursor.execute(
		'INSERT INTO posts (id, url, created_utc, discovered) VALUES (?, ?, ?, ?)',
		(sub.id, sub.url, int(sub.created_utc), int(time.time()))
	)
	conn.commit()

def update_lastseen(sub):
	cursor.execute(
		'UPDATE posts SET lastseen=? WHERE id=?',
		(int(time.time()), sub.id)
	)
	conn.commit()

while True:
 
	try:
		r = praw.Reddit(
				client_id = secrets.client_id,
				client_secret = secrets.client_secret,
				password = secrets.password,
				user_agent = secrets.user_agent,
				username = secrets.username
				)

		print('logged in')
		submissions = r.subreddit('all').hot(limit=100);
		
		total_sub_count = 0
		new_sub_count = 0

		for submission in submissions:
			total_sub_count += 1

			if submission.is_self or not is_an_image(submission.url):
				continue

			if not id_in_db(submission): #if id is not in db then add data
				add_sub_to_db(submission)
				new_sub_count += 1
			else:
				update_lastseen(submission)

		print('{}: Found {}/{} new posts, sleeping'.format(str(datetime.now()), new_sub_count, total_sub_count))
		
	except:
		print('{}: Unexpected error: {}'.format(str(datetime.now()), sys.exc_info()[-1]))
		
	time.sleep(600)