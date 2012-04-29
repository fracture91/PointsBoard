from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from points.models import Board

@login_required
def userBoards(request):
	template = loader.get_template('points/boards.html')
	userBoards = request.user.participating_boards.all()
	ownedBoards = request.user.owned_boards.all()
	context = RequestContext(request, {"boards":userBoards, "ownedBoards":ownedBoards})
	return HttpResponse(template.render(context))
