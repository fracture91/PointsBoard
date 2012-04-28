from django.template import RequestContext, loader
from django.http import HttpResponse
from PointsBoard.points.models import Transaction

def transaction(request, boardId, transactionId):
	if request.method == 'GET':
		template = loader.get_template('points/transaction_page.html')
		transaction = Transaction.objects.get(pk=transactionId)
		context = RequestContext(request, {"transaction": transaction})
		return HttpResponse(template.render(context))
	elif request.method == 'POST':
		return HttpResponse()
