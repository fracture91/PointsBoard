from datetime import datetime
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from points.models import MinComment, Transaction, Board

def singleComment(comment):
	template = loader.get_template('points/comment.html')
	context = Context({"comment":comment})
	return template.render(context)

def getAllComments(trans):
	comments = trans.comments.all()
	responseText = ""
	for comment in comments:
		responseText = responseText + singleComment(comment)
	return responseText

@login_required
def comment(request, boardId, transactionId, commentId=None):
	try:
		board = Board.objects.get(pk=boardId)
		trans = Transaction.objects.get(pk=transactionId)
	except:
		return HttpResponse(status=404)
	
	if not board.isUserAllowedToView(request.user):
		return HttpResponse(status=403)
	
	if trans.board != board:
		return HttpResponse(status=418)
	
	if request.method == 'POST':
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
		response = HttpResponse("singleComment(comment)")
		if 'HTTP_REFERER' in request.META:
			response['Refresh'] = "0; "+request.META['HTTP_REFERER']
		return response
	elif request.method == 'GET':
		if commentId == None:
			return HttpResponse(getAllComments(trans))
		else:
			try:
				comment = MinComment.objects.get(pk=commentId)
			except:
				return HttpResponse(status=404)
			return HttpResponse(singleComment(comment))