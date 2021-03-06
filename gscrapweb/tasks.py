from __future__ import absolute_import
from celery import shared_task
from gscrapweb.models import Track
from bs4 import BeautifulSoup
import requests
import json
import base64
import re
import urlparse
import quopri

def remove_tags(text):
	TAG_RE = re.compile(r'<[^>]+>')
	return TAG_RE.sub(' ', text)

def fetch_youtube_video_info(url,user,domain):
	if 'soundcloud' in url or 'youtube' in url or 'youtu.be' in url:
		try:
			track = True
			response = {'status_code':500}
			try:

				response = requests.get(
						'http://www.youtube.com/oembed',
						 params={'url': url,'format': 'json'}
						)
				print json.loads(response.text)
			except Exception, e:
				print e

			if response.status_code == 200:
				youtube_details = json.loads(response.text)
				title = thumbnail = author_url = author_name = html = ''
				if 'title' in youtube_details:
					title =  youtube_details['title'].encode('ascii','ignore') 
					print title
				if 'thumbnail_url' in youtube_details:
					thumbnail = youtube_details['thumbnail_url']
					print thumbnail
				if 'author_name' in youtube_details:
					author_name = youtube_details['author_name']
					print author_name
				if 'author_url' in youtube_details:
					author_url = youtube_details['author_url']
					print author_url
				if 'html' in youtube_details:
					html = youtube_details['html']
				try:
					
					response = requests.get(
								domain+"/save_track_info",
								 params={'title': title,'thumbnail_url': thumbnail,'author':author_name,'author_url':author_url,'embed':html,'user_id':user.id,'link':url,'track_type':'youtube'}
								)
					print response.status_code
					print json.loads(response.text)
					
				except Exception, e:
					print e	

			try:
				response = requests.get(
						'http://soundcloud.com/oembed',
						 params={'url': url,'format': 'json'}
						)

				print json.loads(response.text)
			except Exception, e:
				print e

			if response.status_code == 200:
				soundcloud_details = json.loads(response.text)
				title = thumbnail = author_url = author_name = html = ''
				if 'title' in soundcloud_details:
					title =  soundcloud_details['title'].encode('ascii','ignore') 
					print title
				if 'thumbnail_url' in soundcloud_details:
					thumbnail = soundcloud_details['thumbnail_url']
					print thumbnail
				if 'author_name' in soundcloud_details:
					author_name = soundcloud_details['author_name']
					print author_name
				if 'author_url' in soundcloud_details:
					author_url = soundcloud_details['author_url']
					print author_url
				if 'html' in soundcloud_details:
					html = soundcloud_details['html']

				try:
					response = requests.get(
								domain+"/save_track_info",
								 params={'title': title,'thumbnail_url': thumbnail,'author':author_name,'author_url':author_url,'embed':html,'user_id':user.id,'link':url,'track_type':'soundcloud'}
								)
					print response.status_code
					print json.loads(response.text)
				except Exception, e:
					print e		



		except Exception, e:
			print e
	else:
		pass


				
@shared_task
def fetch_youtube_video_ids(messages_ids,access_token,email,user,domain):
	for message in messages_ids:
		try:
			response = requests.get(
			'https://www.googleapis.com/gmail/v1/users/'+email+'/messages/'+message['id'],
			 params={'access_token': access_token,'format': 'raw'}
			)
			message = json.loads(response.text)
			message = base64.urlsafe_b64decode(message['raw'].encode('latin-1'))
			message = quopri.decodestring(message)
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
			for url in urls:
				print url
				fetch_youtube_video_info(url,user,domain)
		except Exception, e:
			print e
	print 'Completed'
	