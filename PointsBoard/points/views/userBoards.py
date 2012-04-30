from django.shortcuts import redirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from points.models import Board
from datetime import datetime

@login_required
def userBoards(request):
	feedback = ""
	if request.method == "POST":
		if "create" in request.POST and "board_name" in request.POST:
			try:
				board = Board(name=request.POST["board_name"], owner=request.user,
							creation_date=datetime.now())
				board.full_clean()
				board.save()
				return redirect(reverse("board", args=[board.id]))
			except ValidationError, e:
				feedback = "Error creating board: " + str(e.message_dict)
		else:
			return HttpResponse(status=400)
	elif request.method != "GET":
		return HttpResponse(status=405)
	template = loader.get_template('points/user_boards.html')
	userBoards = request.user.participating_boards.all()
	ownedBoards = request.user.owned_boards.all()
	context = RequestContext(request, {"boards": userBoards,
				"ownedBoards": ownedBoards, "feedback": feedback})
	return HttpResponse(template.render(context))
