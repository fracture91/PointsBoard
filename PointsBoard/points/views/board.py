from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from points.models import Board, Transaction, Category, Cell
from points.views.transaction import renderSingleTransaction 
from django.core.exceptions import ValidationError


def getTransStr(request, board):
	"""
	Get string containing HTML representation of all transactions for given board
	"""
	transactions = Transaction.objects.filter(board=board.id)
	alltrans = []
	for t in transactions:
		alltrans.append(renderSingleTransaction(request, t))
	return "\n".join(alltrans)

def getCats(boardId):
	"""
	Returns an array of category names
	"""
	categories = Category.objects.filter(board=boardId)
	catArr = []
	for cat in categories:
		catArr.append(cat.name)
	catArr.sort()
	return catArr

def getCells(boardId):
	"""
	Returns a dictionary (indexed by username) of
		dictionaries (indexed by category name) of cells for given board
	"""
	categories = Category.objects.filter(board=boardId)
	cellDict = {}
	for cat in categories:
		cells = Cell.objects.filter(category=cat.id)
		for cell in cells:
			if not cellDict.has_key(cell.user.username):
				cellDict[cell.user.username] = {}
			cellDict[cell.user.username][cat.name] = cell
	return cellDict

def makeBoardArray(board, cats, cells):
	"""
	Make a 2-dimensional array which represents the cells of the board.
	"""
	boardArray = []
	boardArray.insert(0, cats)
	boardArray[0].insert(0, "") #empty string for top-left corner
	boardIdx = 0
	users = board.participants.all()
	for user in users:
		if user.username in cells:
			userCells = cells[user.username]
		else:
			userCells = {}
		boardIdx += 1
		boardArray.append([user.username])
		for cat in cats:
			if cat != "":
				boardArray[boardIdx].append(userCells[cat].points)
	return boardArray 

@login_required
def board(request, boardId):
	try:
		board = Board.objects.get(pk=boardId)
	except:
		return HttpResponse(content="Board does not exist", status=404)
	if not board.isUserAllowedToView(request.user):
		return HttpResponse(content="You don't have permission to view this board.", status=403)
	if request.method == 'POST':
		#ensure current user is board owner
		if board.owner != request.user:
			return HttpResponse("You do not have permission to modify this board.", status=403)
		else:
			#change description
			if request.POST.has_key("newDescription"):
				board.description = request.POST["newDescription"]
				board.full_clean()
				board.save()
			#add new category
			elif request.POST.has_key("categoryName"):
				remove = "removeCategory" in request.POST
				catname = request.POST["categoryName"]
				if not remove:
					try:
						category = Category(board=board, name=catname)
						category.full_clean()
					except ValidationError as e:
						return HttpResponse(e, status=400)
					category.save()
				else:
					try:
						category = Category.objects.get(name__exact=catname, board=board)
					except Category.DoesNotExist:
						return HttpResponse("That category does not exist.", status=400)
					category.delete()
			#add new user
			elif request.POST.has_key("userName"):
				remove = "removeUser" in request.POST
				username = request.POST["userName"]
				if not remove:
					try:
						user = User.objects.get(username__exact=username)
					except User.DoesNotExist:
						return HttpResponse("That user does not exist.", status=400)
					board.participants.add(user)
				else :
					try:
						user = board.participants.get(username__exact=username)
					except User.DoesNotExist:
						return HttpResponse("That user is not a board participant.", status=400)
					board.participants.remove(user)
				board.full_clean()
				board.save()
			else:
				return HttpResponse(status=400)
	#display board page no matter what type of request we received
	template = loader.get_template('points/board.html')
	transactions = getTransStr(request, board)
	cats = getCats(boardId)
	cells = getCells(boardId)
	boardArray = makeBoardArray(board, cats, cells)
	context = RequestContext(request,
							{"board":board, "transactions":transactions, "cats":cats, "cells":cells, "boardArray":boardArray})
	return HttpResponse(template.render(context))
