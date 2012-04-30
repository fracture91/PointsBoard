from django.template import RequestContext, loader
from django.http import HttpResponse
from points.models import Board, Category, Transaction
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
from points.views.comment import getAllComments

def renderSingleTransaction(request, transaction):
	board = transaction.board
	template = loader.get_template('points/transaction.html')
	context = RequestContext(request, {"transaction": transaction, "board": board, "comments":getAllComments(transaction)})
	return template.render(context)

@login_required
def transaction(request, boardId, transactionId=-1):
	board = Board.objects.get(pk=boardId)
	if not board.isUserAllowedToView(request.user):
		return HttpResponse(content="You don't have permission to view or add transactions on this board.",
						status=403)
	if request.method == 'GET':
		if transactionId != -1:
			template = loader.get_template('points/transaction_page.html')
			try:
				transaction = Transaction.objects.get(pk=transactionId)
			except Transaction.DoesNotExist:
				return HttpResponse(status=404)
			context = RequestContext(request, {"transaction": transaction, "board": board, "comments":getAllComments(transaction)})
			return HttpResponse(template.render(context))
		return HttpResponse(status=405)
	elif request.method == 'POST':
		#new transaction
		if request.POST.has_key("action"):
			try:
				points = int(request.POST["numPts"])
			except ValueError: #it looks like the default value is 1 on the form, so treat no value as a 1
				points = 1
			if request.POST["action"] == "give":
				points = abs(points)
			elif request.POST["action"] == "remove":
				points = abs(points) * -1;
			if points == 0:
				return HttpResponse("Please enter a nonzero number of points.", status=400)
			cat = Category.objects.get(board=board, name=request.POST["category"])
			rcvUser = User.objects.get(username__exact=request.POST["rcvUser"])
			trans = Transaction(board=board, category=cat, points=points, reason=request.POST["reason"],
					recipient=rcvUser, giver=request.user, creation_date=datetime.datetime.now())
			trans.full_clean()
			trans.save()
		elif request.POST.has_key("delete"):
			if request.user != board.owner:
				return HttpResponse(content="You don't have permission to delete transactions on this board.",
								status=403)
			try:
				todel = Transaction.objects.get(pk=transactionId)
			except Transaction.DoesNotExist:
				return HttpResponse(status=404)
			todel.delete()
		response = HttpResponse()
		response['Refresh'] = "0; url=/boards/"+str(boardId)
		return response