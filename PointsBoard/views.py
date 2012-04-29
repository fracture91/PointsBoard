from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

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
	username = request.POST['username_register']
	password = request.POST['password_register']
	confirm = request.POST['password_confirm']
	if not username:
		return renderHome(request, {"register_feedback": "You cannot use an empty username."})
	try:
		User.objects.get(username__exact=username)
		return renderHome(request, {"register_feedback": "That username is already taken."})
	except User.DoesNotExist:
		pass
	if not password:
		return renderHome(request, {"register_feedback": "You cannot use an empty password."})
	if password != confirm:
		return renderHome(request,
			{"register_feedback": "Passwords do not match, make sure you're typing them in correctly."})
	User.objects.create_user(username, "example@example.com", password)
	user = authenticate(username=username, password=password)
	login(request, user)
	return handleRedirect(request, reverse("userBoards"))

def home(request):
	if request.method == "POST":
		if "login" in request.POST:
			return handleLogin(request)
		elif "register" in request.POST:
			return handleRegistration(request)
		else:
			return HttpResponse(status=400)
	elif request.method == "GET":
		return renderHome(request)
	else:
		return HttpResponse(status=405)
