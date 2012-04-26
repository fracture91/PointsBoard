from django.template import Context, loader
from django.http import HttpResponse

def userBoards(request):
	template = loader.get_template('points/user_boards.html')
	context = Context()
	return HttpResponse(template.render(context))
