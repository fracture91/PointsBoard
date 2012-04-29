from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from points.models import Board, Transaction, Category, Cell

"""
Get string containing HTML representation of all transactions for given board
"""
def getTransStr(request, boardId):
	transactions = Transaction.objects.filter(board=boardId)
	alltrans = []
	for t in transactions:
		alltrans.append(
					render_to_string('points/transaction.html', {"transaction": t, "boardid": boardId}, RequestContext(request)))
	return "\n".join(alltrans)

"""
Returns an array of category names
"""
def getCats(boardId):
	categories = Category.objects.filter(board=boardId)
	catArr = []
	for cat in categories:
		catArr.append(cat.name)
	return catArr

"""
Returns a dictionary (indexed by username) of
	dictionaries (indexed by category name) of cells for given board
"""
def getCells(boardId):
	categories = Category.objects.filter(board=boardId)
	cellDict = {}
	for cat in categories:
		cells = Cell.objects.filter(category=cat.id)
		for cell in cells:
			if not cellDict.has_key(cell.user.username):
				cellDict[cell.user.username] = {}
			cellDict[cell.user.username][cat.name] = cell
	return cellDict

@login_required
def board(request, boardId):
	board = Board.objects.get(pk=boardId)
	if not board.isUserAllowedToView(request.user):
		return HttpResponse(content="You don't have permission to view this board.", status=403)
	if request.method == 'POST':
		#ensure current user is board owner
		if board.owner.id == request.user.id:
			#change description
			if request.POST.has_key("newDescription"):
				board.description = request.POST["newDescription"]
				board.full_clean()
				board.save()
			#add new category
			elif request.POST.has_key("categoryName"):
				newcatname = request.POST["categoryName"]
				newcat = Category(board=board, name=newcatname)
				newcat.full_clean()
				newcat.save()
			#add new user
			elif request.POST.has_key("userName"):
				userNameToAdd = request.POST["userName"]
				try:
					userToAdd = User.objects.get(username__exact=userNameToAdd)
				except User.DoesNotExist:
					return HttpResponse("That user does not exist.")
				board.participants.add(userToAdd)
				board.full_clean()
				board.save()
			else:
				return HttpResponse(status=400)
	template = loader.get_template('points/board.html')
	transactions = getTransStr(request, boardId)
	cats = getCats(boardId)
	cells = getCells(boardId)
	
	context = RequestContext(request,
							{"board":board, "transactions":transactions, "cats":cats, "cells":cells})
	return HttpResponse(template.render(context))
