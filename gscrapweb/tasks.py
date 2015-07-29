from __future__ import absolute_import
from celery import shared_task



@shared_task
def fetch_youtube_video_info(url,user):
	print url
	response = requests.get(
			'http://www.youtube.com/oembed',
			 params={'url': url,'format': 'json'}
			)
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
			track = Track.objects.get(link=url,user_id=user)
		except Track.DoesNotExist:
			Track.objects.create(title=title,thumbnail=thumbnail,author_link=author_url,author=author_name,track_type='youtube',link=url,user_id=user,embed=html)

	response = requests.get(
			'http://soundcloud.com/oembed',
			 params={'url': url,'format': 'json'}
			)
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
			track = Track.objects.get(link=url,user_id=user)
		except Track.DoesNotExist:
			Track.objects.create(title=title,thumbnail=thumbnail,author_link=author_url,author=author_name,track_type='soundcloud',link=url,user_id=user,embed=html)

@shared_task
def fetch_youtube_video_ids(messages_ids,access_token,email,user):
	print 'worker here'
	for message in messages_ids:
		response = requests.get(
			'https://www.googleapis.com/gmail/v1/users/'+email+'/messages/'+message['id'],
			 params={'access_token': access_token,'format': 'raw'}
			)
		message = json.loads(response.text)
		message = base64.urlsafe_b64decode(message['raw'].encode('UTF-8'))
		message = remove_tags(message)
		message = message.replace('\n',' ')
		message = message.replace('\r',' ')
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
		for url in urls:
			fetch_youtube_video_info(url,user)
	return 'done'