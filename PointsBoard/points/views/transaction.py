from django.template import RequestContext, loader
from django.http import HttpResponse
from points.models import Board, Category, Transaction
from django.contrib.auth.models import User
import datetime


def transaction(request, boardId, transactionId=-1):
	if request.method == 'GET':
		if transactionId != -1:
			template = loader.get_template('points/transaction_page.html')
			transaction = Transaction.objects.get(pk=transactionId)
			context = RequestContext(request, {"transaction": transaction})
			return HttpResponse(template.render(context))
	elif request.method == 'POST':
		#new transaction
		if request.POST.has_key("action"):
			if request.user.is_authenticated():
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
		return HttpResponse("Transaction added.")
