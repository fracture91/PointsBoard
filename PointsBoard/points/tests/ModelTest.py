from django.test import TestCase
from points.models import Board, Category, Cell, Transaction
from django.contrib.auth.admin import User
from datetime import datetime

class ModelTest(TestCase):
	def setUp(self):
		self.testman = User.objects.create_user("testman", "example@example.com", "password")
		self.testboy = User.objects.create_user("testboy", "example@example.com", "password")
		self.board = Board(name="test board", description="This is a test board", owner=self.testman,
						creation_date=datetime.now())
		self.board.save()
		self.board.participants.add(self.testman, self.testboy)
		self.paragon = Category.objects.create(name="Paragon", board=self.board)
		self.renegade = Category.objects.create(name="Renegade", board=self.board)
	
	def tearDown(self):
		self.board.participants.clear()
		toDelete = [Board, User, Category, Cell, Transaction]
		for model in toDelete:
			model.objects.all().delete()
			
	def testBoardDefinition(self):
		self.assertEqual(self.board.name, "test board")
		self.assertEqual(self.board.description, "This is a test board")
		self.assertEqual(self.board.owner, self.testman)
		self.assertIsInstance(self.board.creation_date, datetime)
		
		self.assertEqual(self.testman.username, "testman")
		self.assertEqual(self.testboy.username, "testboy")
		
		# will raise exceptions if they don't exist
		self.assertEqual(self.board.participants.get(username="testman"), self.testman)
		self.assertEqual(self.board.participants.get(username="testboy"), self.testboy)
		
		self.assertEqual(self.paragon.name, "Paragon")
		self.assertEqual(self.renegade.name, "Renegade")
		
		self.assertEqual(self.board.category_set.get(name="Paragon"), self.paragon)
		self.assertEqual(self.board.category_set.get(name="Renegade"), self.renegade)
		
	def testBoardCells(self):
		# cells should have been created automatically
		self.assertEqual(self.paragon.cell_set.get(user=self.testman).points, 0)
		self.assertEqual(self.paragon.cell_set.get(user=self.testboy).points, 0)
		self.assertEqual(self.renegade.cell_set.get(user=self.testman).points, 0)
		self.assertEqual(self.renegade.cell_set.get(user=self.testboy).points, 0)
		
	def testAddUserCells(self):
		user = User.objects.create_user("newuser", "example@example.com", "password")
		self.board.participants.add(user)
		self.assertEqual(self.board.participants.get(username="newuser"), user)
		self.assertEqual(self.paragon.cell_set.get(user=user).points, 0)
		self.assertEqual(self.renegade.cell_set.get(user=user).points, 0)
		self.assertEqual(self.paragon.cell_set.count(), 3)
		self.assertEqual(self.renegade.cell_set.count(), 3)
