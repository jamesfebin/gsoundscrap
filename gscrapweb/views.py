from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from social.apps.django_app.default.models import UserSocialAuth
import requests
import json
import base64
import re
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

def parse_video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return ''

def remove_tags(text):
	TAG_RE = re.compile(r'<[^>]+>')
	return TAG_RE.sub('', text)

def fetch_and_parse_url_from_messages(messages_ids,access_token,email):
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
			video_id = parse_video_id(url) 
			if video_id != '':
				print video_id
				print url
			else:
				print url

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
					fetch_and_parse_url_from_messages(youtube_emails['messages'],google.extra_data['access_token'],google.uid)
			else:
				print json.loads(response.text)
	return render_to_response('sync.html')



'''

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


