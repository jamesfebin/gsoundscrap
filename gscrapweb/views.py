from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext

# Create your views here.

def home(request):

	soundcloud = False
	if request.user and request.user.is_anonymous() is False and request.user.is_superuser is False:
		
		google = request.user.social_auth.get(provider='google-oauth2')
			print google
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