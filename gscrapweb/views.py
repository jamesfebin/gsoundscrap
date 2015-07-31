from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from social.apps.django_app.default.models import UserSocialAuth
from django.conf import settings
from models import Track
import tasks
import requests
import json
import soundcloud
import base64
import re
import urlparse
# Create your views here.


def home(request):
	tracks = []
	soundcloud = False
	if request.user and request.user.is_anonymous() is False and request.user.is_superuser is False:
		try:
			soundcloud = UserSocialAuth.objects.get(user=request.user,provider="soundcloud")
			if soundcloud:
				soundcloud = True
		except Exception, e:
			#Nothing to worry , Sound cloud isn't connected
			print e

		tracks = Track.objects.filter(user_id=request.user.id)

	context = RequestContext(request,
                           {'user': request.user,'soundcloud':soundcloud,'tracks':tracks})

	return render_to_response('home.html',context_instance=context)


def fetch_from_gmail(access_token,email,query,start,end):
	response = requests.get(
			'https://www.googleapis.com/gmail/v1/users/'+email+'/messages',
			 params={'access_token': access_token,'q': query + ' after:'+start +' before:'+end}
			)
	print 'query 2 is here '
	print query + ' after:'+start +' before:'+end
	return response

def parse_video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse.urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = urlparse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return ''




'''
video_id = parse_video_id(url) 
if video_id != '':
	print video_id
	print url
else:
	print url
'''

def sync(request):
	domain = request.META['HTTP_HOST']
	print domain
	print 'is secure'
	print request.is_secure()
	if request.is_secure():
		domain = 'http://'+domain
	else:
		domain = 'https://'+domain


	if request.user and request.user.is_anonymous() is False and request.user.is_superuser is False:
		google = UserSocialAuth.objects.get(user=request.user,provider="google-oauth2")
		if google:
			
			start = request.GET.get('from')
			print start
			end = request.GET.get('end')
			print end

			query = 'youtube.com'
			response = fetch_from_gmail(google.extra_data['access_token'],google.uid,query,start,end)
			if response.status_code == 200:
				youtube_emails = json.loads(response.text)
				if 'messages' in youtube_emails:
					tasks.fetch_youtube_video_ids.delay(youtube_emails['messages'],google.extra_data['access_token'],google.uid,request.user,domain)
			else:
				print json.loads(response.text)

			query = 'soundcloud.com'

			response = fetch_from_gmail(google.extra_data['access_token'],google.uid,query,start,end)
			if response.status_code == 200:
				youtube_emails = json.loads(response.text)
				if 'messages' in youtube_emails:
					tasks.fetch_youtube_video_ids.delay(youtube_emails['messages'],google.extra_data['access_token'],google.uid,request.user,domain)
			else:
				print json.loads(response.text)

			query = 'youtu.be'

			response = fetch_from_gmail(google.extra_data['access_token'],google.uid,query,start,end)
			if response.status_code == 200:
				youtube_emails = json.loads(response.text)
				if 'messages' in youtube_emails:
					tasks.fetch_youtube_video_ids.delay(youtube_emails['messages'],google.extra_data['access_token'],google.uid,request.user,domain)
			else:
				print json.loads(response.text)
		else:
			print 'Doesnt exist'

	return render_to_response('sync.html')

def save_track_info(request):

	thumbnail = request.GET.get('thumbnail_url')
	title = request.GET.get('title')
	author = request.GET.get('author')
	author_url = request.GET.get('author_url')
	embed = request.GET.get('embed')
	user_id = request.GET.get('user_id')
	link = request.GET.get('link')
	track_type = request.GET.get('track_type')
	print 'Trying to add'
	try:
		track = Track.objects.get(link=link,user_id=user_id)
	except Track.DoesNotExist:
		try:
			Track.objects.create(title=title,thumbnail=thumbnail,author_link=author_url,author=author,track_type=track_type,link=link,user_id=user_id,embed=embed)
			print 'added'
		except Exception, e:
			print e
	except Exception, e:
		print e


def follow_user(request):
	try:
		url = request.GET.get('url')
		SOUNDCLOUD_KEY = settings.SOCIAL_AUTH_SOUNDCLOUD_KEY
		client = soundcloud.Client(client_id=SOUNDCLOUD_KEY)
		soundcloud_user = client.get('/resolve', url=url)
		if request.user and request.user.is_anonymous() is False and request.user.is_superuser is False:
			soundcloud_data = UserSocialAuth.objects.get(user=request.user,provider="soundcloud")	
			if soundcloud_data:
				client = soundcloud.Client(access_token=soundcloud_data.extra_data['access_token'])
				response = client.put('/me/followings/'+soundcloud_user.id)
				print json.loads(response.text)
	except Exception, e:
		print e

	return render_to_response('sync.html')

	


def like_track(request):
	try:
		url = request.GET.get('url')
		SOUNDCLOUD_KEY = settings.SOCIAL_AUTH_SOUNDCLOUD_KEY
		client = soundcloud.Client(client_id=SOUNDCLOUD_KEY)
		track = client.get('/resolve', url=url)
		if request.user and request.user.is_anonymous() is False and request.user.is_superuser is False:
			soundcloud_data = UserSocialAuth.objects.get(user=request.user,provider="soundcloud")	
			if soundcloud_data:
				client = soundcloud.Client(access_token=soundcloud_data.extra_data['access_token'])
				response = client.put('/me/favorites/'+track.id)
				print json.loads(response.text)
	except Exception, e:
		print e

	return render_to_response('sync.html')

'''

def save_track_info(request):
	thumbnail_url = request.GET.get('thumbnail_url')
	title = request.GET.get('title')
	author = request.GET.get('author')
	author_url = request.GET.get('author_url')
	embed = request.GET.get('embed')
	user_id = request.GET.get('user_id')
	link = request.GET.get('link')
	track_type = request.GET.get('track_type')


						 


	response = requests.get(
			'https://www.googleapis.com/gmail/v1/users/jamesfebin%40gmail.com/messages/14c6735174c40b02',
			 params={'access_token': 'ya29.vgFgiO_EJBS7MD12iKu7894OxZ8I3nVouT6PIEr5lFK1bSQejCNQw6TME_oTbSuzpZJC2g','format': 'raw'}
			)




			query = 'youtu.be'
			response = fetch_from_gmail(google.extra_data['access_token'],google.uid,query,start,end)
			if response.status_code == 200:
				youtube_emails = json.loads(response.text)
				if 'messages' in youtube_emails:
					fetch_and_parse_url_from_messages(youtube_emails['messages'],google.extra_data['access_token'],google.uid)
			else:
				print json.loads(response.text)


			query = 'soundcloud.com'
			response = fetch_from_gmail(google.extra_data['access_token'],google.uid,query,start,end)
			if response.status_code == 200:
				soundcloud_emails = json.loads(response.text)
				print soundcloud_emails
			else:
				print json.loads(response.text)

		google = request.user.social_auth.get(provider='google-oauth2')
		if google: 
			access_token = google['access_token']
			response = requests.get(
			    'https://www.googleapis.com/gmail/v1/users/'+email+'/messages',
			    params={'access_token': 'ya29.vgFEY0uezVNr7Zmtusrwr51VZzVLq83xH6D-oEpjC2uI3NnUddDp3XIQbvmWrk2tJX_bjw','q':' boutline after:2010/01/01 before:2015/06/30'}
			)
		access_token = google.extra_data['access_token']
			response = requests.get(
			    'https://www.googleapis.com/gmail/v1/users/'+email+'/messages',
			    params={'access_token': 'ya29.vgFEY0uezVNr7Zmtusrwr51VZzVLq83xH6D-oEpjC2uI3NnUddDp3XIQbvmWrk2tJX_bjw','q':' boutline after:2010/01/01 before:2015/06/30'}
			)
		
		'''


