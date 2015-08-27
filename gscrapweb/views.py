from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from social.apps.django_app.default.models import UserSocialAuth
from social.apps.django_app.utils import load_strategy
from django.core.paginator import Paginator
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
	soundcloud_auth = False
	pnos=0
	next_page = 0
	prev_page = 0
	current_page = request.GET.get('current_page',1)
	current_page = int(current_page)
	print 'current_page is'
	print current_page

	if request.user and request.user.is_anonymous() is False and request.user.is_superuser is False:
		try:
			soundcloud_auth = UserSocialAuth.objects.get(user=request.user,provider="soundcloud")

			if soundcloud_auth:
				soundcloud_auth = True
		except Exception, e:
			#Nothing to worry , Sound cloud isn't connected
			print e

		#Try refreshing the token	
		try: 
			if soundcloud_auth:
				strategy = load_strategy(backend='soundcloud')
				UserSocialAuth.refresh_token(strategy)
		except Exception, e:
			print 'refresh token error'
			print e 

		tracks = Track.objects.filter(user_id=request.user.id)
		p = Paginator(tracks,10)
		pnos = p.num_pages
		if current_page > p.num_pages:
			current_page = p.num_pages
		page1 = p.page(current_page) 
		tracks = page1.object_list
		next_page = current_page + 1
		if next_page > p.num_pages:
			next_page = 0

		prev_page = current_page - 1
		if prev_page < 0 :
			prev_page = 0

	context = RequestContext(request,
                           {'user': request.user,'soundcloud':soundcloud_auth,'tracks':tracks,'pnos':pnos,'current_page':current_page,'next_page':next_page,'prev_page':prev_page})

	return render_to_response('home.html',context_instance=context)

def get_page(request):
	tracks = []
	page_no = request.GET.get('page')
	if request.user and request.user.is_anonymous() is False and request.user.is_superuser is False:
		try:
			tracks = Track.objects.filter(user_id=request.user.id)
			p = Paginator(tracks,10)
			pnos = p.num_pages
			page1 = p.page(page_no)
			tracks = page1.object_list
		except Exception, e:
			print e		
	return tracks



def fetch_from_gmail(access_token,email,query,start,end):
	response = requests.get(
			'https://www.googleapis.com/gmail/v1/users/'+email+'/messages',
			 params={'access_token': access_token,'q': query + ' after:'+start +' before:'+end}
			)
	print 'query 2 is here '
	print query + ' after:'+start +' before:'+end
	return response

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
				response = client.put('/me/followings/'+str(soundcloud_user.id))
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
				response = client.put('/me/favorites/'+str(track.id))
				print json.loads(response.text)
	except Exception, e:
		print e

	return render_to_response('sync.html')




