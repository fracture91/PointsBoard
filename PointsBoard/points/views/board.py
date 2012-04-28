from django.template import Context, RequestContext, loader
from django.template.loader import render_to_string
from django.http import HttpResponse
from PointsBoard.points.models import Board
from PointsBoard.points.models import Transaction
from PointsBoard.points.models import Category
from PointsBoard.points.models import Cell

"""
Get string containing HTML representation of all transactions for given board
"""
def getTransStr(boardId):
	transactions = Transaction.objects.filter(board=boardId)
	alltrans = []
	for t in transactions:
		alltrans.append(render_to_string('points/transaction.html', {"transaction": t}))
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
	template = loader.get_template('points/board.html')
	board = Board.objects.get(pk=boardId)
	transactions = getTransStr(boardId)
	cats = getCats(boardId)
	cells = getCells(boardId)
	
	context = RequestContext(request, {"board":board, "transactions":transactions, "cats":cats, "cells":cells})
	return HttpResponse(template.render(context))
