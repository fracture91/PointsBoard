from django.template import RequestContext, loader
from django.http import HttpResponse
from points.models import Board, Category, Transaction
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def transaction(request, boardId, transactionId=-1):
	if request.method == 'GET':
		if transactionId != -1:
			template = loader.get_template('points/transaction_page.html')
			transaction = Transaction.objects.get(pk=transactionId)
			context = RequestContext(request, {"transaction": transaction})
			return HttpResponse(template.render(context))
		response = HttpResponse()
		response.status_code = 404
		return response
	elif request.method == 'POST':
		#new transaction
		if request.POST.has_key("action"):
			board = Board.objects.get(pk=boardId)
			points = int(request.POST["numPts"])
			if request.POST["action"] == "give":
				points = abs(points)
			elif request.POST["action"] == "remove":
				points = abs(points) * -1;
			if points == 0:
				return HttpResponse("Please enter a nonzero number of points.")
			cat = Category.objects.get(board=board, name=request.POST["category"])
			rcvUser = User.objects.get(username__exact=request.POST["rcvUser"])
			trans = Transaction(board=board, category=cat, points=points, reason=request.POST["reason"],
					recipient=rcvUser, giver=request.user, creation_date=datetime.datetime.now())
			trans.full_clean()
			trans.save()
		response = HttpResponse()
		response['Refresh'] = "0; url=/boards/"+str(boardId)
		return response