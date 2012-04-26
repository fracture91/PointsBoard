from django.template import Context, loader
from django.http import HttpResponse

def board(request, boardId):
	template = loader.get_template('points/board.html')
	context = Context()
	return HttpResponse(template.render(context))
