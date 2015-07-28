from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from social.apps.django_app.default.models import UserSocialAuth

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


def sync(request):
	if request.user and request.user.is_anonymous() is False and request.user.is_superuser is False:
		user = UserSocialAuth.objects.get(user=request.user,provider="google-oauth2")
		print user.extra_data
		print user.uid
		return render_to_response('sync.html')
		'''
		google = request.user.social_auth.get(provider='google-oauth2')
		if google: 
			access_token = google['access_token']
			response = requests.get(
			    'https://www.googleapis.com/gmail/v1/users/'+email+'/messages',
			    params={'access_token': 'ya29.vgFEY0uezVNr7Zmtusrwr51VZzVLq83xH6D-oEpjC2uI3NnUddDp3XIQbvmWrk2tJX_bjw','q':' boutline after:2010/01/01 before:2015/06/30'}
			)

		
		'''


