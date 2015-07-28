from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from social.apps.django_app.default.models import UserSocialAuth
import requests
import json
# Create your views here.

def home(request):

	soundcloud = False
	if request.user and request.user.is_anonymous() is False and request.user.is_superuser is False:
		try:
			soundcloud = request.user.social_auth.get(provider='soundcloud')
			if soundcloud:
				backend = soundcloud.get_backend_instance()
				soundcloud = True
		except Exception, e:
			#Nothing to worry , Sound cloud isn't connected
			print e


	context = RequestContext(request,
                           {'user': request.user,'soundcloud':soundcloud})
	return render_to_response('home.html',context_instance=context)


def fetch_from_gmail(access_token,email,query,start,end):
	response = requests.get(
			'https://www.googleapis.com/gmail/v1/users/'+email+'/messages',
			 params={'access_token': access_token,'q': query + ' after:'+start +' before:'+end}
			)
	return response

def fetch_and_parse_url_from_messages(messages_ids,access_token):
	for message in messages:
		response = requests.get(
			'https://www.googleapis.com/gmail/v1/users/'+email+'/messages/'+message['id'],
			 params={'access_token': access_token,'q': query + ' after:'+start +' before:'+end}
			)
		print json.loads(response.text)
		break

def sync(request):
	if request.user and request.user.is_anonymous() is False and request.user.is_superuser is False:
		google = UserSocialAuth.objects.get(user=request.user,provider="google-oauth2")
		if google:
		
			start = '2010/01/01'
			end = '2015/06/30'
			query = 'youtube.com'

			response = fetch_from_gmail(google.extra_data['access_token'],google.uid,query,start,end)
			if response.status_code == 200:
				youtube_emails = json.loads(response.text)
				if 'messages' in youtube_emails:
					fetch_and_parse_url_from_messages(youtube_emails['messages'],google.extra_data['access_token'])
			else:
				print json.loads(response.text)
	return render_to_response('sync.html')

	

'''

			query = 'youtu.be'
			response = fetch_from_gmail(google.extra_data['access_token'],google.uid,query,start,end)
			if response.status_code == 200:
				youtube_emails = json.loads(response.text)
				if 'messages' in youtube_emails:
					fetch_and_parse_url_from_messages(youtube_emails['messages'],google.extra_data['access_token'])
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


