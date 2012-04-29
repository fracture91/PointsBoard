from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

def renderHome(*args, **kwargs):
	return render_to_response('home.html', context_instance=RequestContext(*args, **kwargs))

# go to "next" param if it exists, otherwise the given url
def handleRedirect(request, url):
	if request.GET.has_key("next"):
		return redirect(request.GET["next"])
	else:
		return redirect(url)

# log in the user based on the given request, return a HttpResponse
def handleLogin(request):
	username = request.POST['username_login']
	password = request.POST['password_login']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return handleRedirect(request, reverse("userBoards"))
		else:
			return renderHome(request, {"login_feedback": "That account is disabled."})
	else:
		return renderHome(request, {"login_feedback": "Invalid login credentials provided."})

def handleRegistration(request):
	# todo
	return renderHome(request)

def home(request):
	if request.method == "POST":
		if "login" in request.POST:
			return handleLogin(request)
		elif "register" in request.POST:
			return handleRegistration(request)
		else:
			response = HttpResponse()
			response.status_code = 400
			return response
	return renderHome(request)
