#!/usr/bin/python

import csv
import time
import json
import click
import datetime
import requests

DRIBBBLE_SHOTS_URL = 'https://api.dribbble.com/v1/shots'

@click.command()
@click.option('--verbose/--no-verbose', default=False, help='Verbosity (False by default).')
@click.option('--follow/--no-follow', default=False, help='Fetch next page results or not (False by default).')
@click.option('--shots-per-page', '-p', default=10, help='The number of shots returned per page (10 by default).')
@click.option('--likes-per-page', '-q', default=100, help='The number of likes returned per page (100 by default).')
@click.option('--timeframe', '-t', default=None, help='A period of time to limit the results to (False by default).')
@click.option('--date', '-d', default=None, help='Limit the timeframe to a specific date (False by default).')
@click.option('--sort', '-s', default=None, type=click.Choice(['comments', 'recent', 'views', None]), help='The sort field ("popular" by default).')
def likkkes(timeframe, shots_per_page, likes_per_page, follow, sort, date, verbose):

	if verbose:
		print('\ntimeframe: %s\nshots_per_page: %s\nlikes_per_page: %s\nfollow: %s\nsort: %s\ndate: %s\nverbose: %s\n' 
			% (timeframe, 
				shots_per_page, 
				likes_per_page, 
				follow, 
				sort, 
				date, 
				verbose))

	shots_list = []
	users_set = set()
	shots_url = DRIBBBLE_SHOTS_URL
	headers = {'Authorization': 'Bearer %s' % open('likkkes.conf', 'r').read()}

	############################## RETRIEVE ##############################

	while shots_url:

		time.sleep(1) # Dribbble rate limit (up to 60 requests per minute)
		shots_response = requests.get(shots_url, headers=headers, params={'date': date, 'timeframe': timeframe, 'sort': sort, 'per_page': shots_per_page})
		shots_url = shots_response.links.get('next', {}).get('url', False) if follow else False
		if verbose: print('Retrieving shots from %s' % shots_response.url)

		if shots_response.status_code == 200:
			for s in shots_response.json():
				likes_count = s['likes_count']
				shot_dict = {
					'shot_id': s['id'],
					'views_count': s['views_count'], 
					'likes_count': likes_count, 
					'comments_count': s['comments_count'], 
					'attachments_count': s['attachments_count'], 
					'rebounds_count': s['rebounds_count'], 
					'buckets_count': s['buckets_count'], 
					'created_at': s['created_at'], 
					'user_id': s['user']['id'], 
					'user_location': s['user']['location'], 
					'user_followers_count': s['user']['followers_count'], 
					'user_followings_coount': s['user']['followings_count'], 
					'user_shots_count': s['user']['shots_count']
				}

				users_list = []
				likes_url = s.get('likes_url', False)

				while likes_url and likes_count:

					time.sleep(1) # Dribbble rate limit (up to 60 requests per minute)
					likes_response = requests.get(likes_url, headers=headers, params={'per_page': likes_per_page})
					likes_url = likes_response.links.get('next', {}).get('url', False)
					if verbose: print('Retrieving likes from %s' % likes_response.url)

					if likes_response.status_code == 200:
						for l in likes_response.json():
							user_id = l['user']['id']
							users_set.add(user_id)
							users_list.append(user_id)

				shot_dict.update({'likes': users_list})
				shots_list.append(shot_dict)

	############################## CSV ##############################

	file_name = ('date_%s-timeframe_%s-sort_%s-shots_len_%s.%s' 
		% (date.replace('-', ''), 
			timeframe, 
			sort, 
			len(shots_list), 
			datetime.datetime.now().strftime("%Y%m%d-%H%M%S")))

	users_file = open('csv/users.%s.csv' % file_name.lower(), 'w')
	shots_file = open('csv/shots.%s.csv' % file_name.lower(), 'w')
	likes_file = open('csv/likes.%s.csv' % file_name.lower(), 'w')

	delimiter = ''
	for u in users_set:
		users_file.write('%s%s' % (delimiter, u))
		delimiter = ','

	shots_file.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,"%s",%s,%s,%s\n' % 
		('shot_id',  
			'views_count', 
			'likes_count', 
			'comments_count', 
			'attachments_count',
			'rebounds_count',
			'buckets_count',
			'created_at',
			'user_id',
			'user_location',
			'user_followers_count',
			'user_followings_count',
			'user_shots_count'))

	for s in shots_list:
		shots_file.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,"%s",%s,%s,%s\n' % 
			(s['shot_id'],  
				s['views_count'], 
				s['likes_count'], 
				s['comments_count'], 
				s['attachments_count'],
				s['rebounds_count'],
				s['buckets_count'],
				s['created_at'],
				s['user_id'],
				s['user_location'],
				s['user_followers_count'],
				s['user_followings_count'],
				s['user_shots_count']))

		delimiter = ''
		for u in users_set:
			if u in s.get('likes', []):
				likes_file.write('%s1' % delimiter)
			else:
				likes_file.write('%s0' % delimiter)
			delimiter = ','
		likes_file.write('\n')

if __name__ == '__main__':
	likkkes()
