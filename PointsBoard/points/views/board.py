from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.models import User
from PointsBoard.points.models import Board
from PointsBoard.points.models import Transaction
from PointsBoard.points.models import Category
from PointsBoard.points.models import Cell

"""
Get string containing HTML representation of all transactions for given board
"""
def getTransStr(request, boardId):
	transactions = Transaction.objects.filter(board=boardId)
	alltrans = []
	for t in transactions:
		alltrans.append(render_to_string('points/transaction.html', {"transaction": t}, RequestContext(request)))
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

def board(request, boardId):
	if request.method == 'GET':
		template = loader.get_template('points/board.html')
		board = Board.objects.get(pk=boardId)
		transactions = getTransStr(request, boardId)
		cats = getCats(boardId)
		cells = getCells(boardId)
		
		context = RequestContext(request, {"board":board, "transactions":transactions, "cats":cats, "cells":cells})
		return HttpResponse(template.render(context))
	elif request.method == 'POST':
		#change description
		if request.POST.has_key("newDescription"):
			if request.user.is_authenticated():
				board = Board.objects.get(pk=boardId)
				#ensure current user is board owner
				if board.owner.id == request.user.id:
					board.description = request.POST["newDescription"]
					#validate board data
					#save board
		#add new category
		elif request.POST.has_key("categoryName"):
			if request.user.is_authenticated():
				board = Board.objects.get(pk=boardId)
				#ensure current user is board owner
				if board.owner.id == request.user.id:
					newcatname = request.POST["categoryName"]
					Category(board=board, name=newcatname)
					#validate category data
					#save category
		#add new user
		elif request.POST.has_key("userName"):
			if request.user.is_authenticated():
				board = Board.objects.get(pk=boardId)
				#ensure current user is board owner
				if board.owner.id == request.user.id:
					userNameToAdd = request.POST["userName"]
					try:
						userToAdd = User.objects.get(username__exact=userNameToAdd)
					except User.DoesNotExist:
						#TODO: error message
						return HttpResponse()
					board.participants.add(userToAdd)
					#validate board data
					#save board
		#new transaction
		elif request.POST.has_key("action"):
			if request.user.is_authenticated():
				board = Board.objects.get(pk=boardId)
				points = int(request.POST["numPts"])
				if request.POST["action"] == "give":
					points = abs(points)
				elif request.POST["action"] == "remove":
					points = abs(points) * -1;
				if points == 0:
					return HttpResponse("Please enter a nonzero number of points.")
				request.POST["category"]
				request.POST["rcvUser"]
		
		return HttpResponse()
