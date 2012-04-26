from django.template import Context, loader
from django.http import HttpResponse

def transaction(request, boardId, transactionId):
	template = loader.get_template('points/transaction_page.html')
	context = Context()
	return HttpResponse(template.render(context))
