from datetime import datetime
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from points.models import MinComment, Transaction

def singleComment(request, comment):
	template = loader.get_template('points/comment.html')
	context = RequestContext(request, {"comment":comment})
	return template.render(context)

def getAllComments(request, trans):
	comments = trans.comments.all()
	responseText = ""
	for comment in comments:
		responseText = responseText + singleComment(request, comment)
	return responseText

@login_required
def comment(request, boardId, transactionId, commentId=None):
	if request.method == 'POST':
		try:
			trans = Transaction.objects.get(pk=transactionId)
		except:
			return HttpResponse(status=404)
		try:
			text = request.POST["comment"]
		except:
			return HttpResponse(status=400)
		try:
			comment = MinComment(user=request.user, transaction = trans, submit_date = datetime.now(), comment=text)
		except:
			return HttpResponse(status=500)
		comment.full_clean()
		comment.save()
	elif request.method == 'GET':
		if commentId == None:
			try:
				trans = Transaction.objects.get(pk=transactionId)
			except:
				return HttpResponse(status=404)
			return HttpResponse(getAllComments(request, trans))
		else:
			try:
				comment = MinComment.objects.get(pk=commentId)
			except:
				return HttpResponse(status=404)
			return HttpResponse(singleComment(request, comment))