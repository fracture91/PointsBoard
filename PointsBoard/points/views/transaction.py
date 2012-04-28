from django.template import Context, loader
from django.http import HttpResponse
from PointsBoard.points.models import Transaction
from django.contrib.auth.models import User

def transaction(request, boardId, transactionId):
	template = loader.get_template('points/transaction_page.html')
	transaction = Transaction.objects.get(pk=transactionId)
	context = Context({"transaction": transaction})
	return HttpResponse(template.render(context))
