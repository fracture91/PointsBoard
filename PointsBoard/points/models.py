from django.db import models
from django.contrib.auth.models import User

"""
Django doesn't support primary keys with multiple columns :(
https://code.djangoproject.com/ticket/373

Django magically adds an integer primary key for you, unless you tell it not to

blank=False and null=False for all fields by default (all are required and non-null)

Django has a built-in User model and comments framework, so we don't need to worry about those
https://docs.djangoproject.com/en/dev/topics/auth/
https://docs.djangoproject.com/en/1.3/ref/contrib/comments/

To check out the code Django generates:
python PointsBoard\manage.py sqlall points

To get rid of everything in the database related to this app:
python PointsBoard\manage.py sqlclear points | python PointsBoard\manage.py dbshell
(make sure psql is on your PATH)

To sync everything back up in the database (create all the tables and whatnot):
python PointsBoard\manage.py syncdb
"""

class Board(models.Model):
	"""
	A points board with a name, optional description, and owner.
	participants does not necessarily include the owner.
	An owner cannot own two boards with the same name.
	"""
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=512, blank=True)
	owner = models.ForeignKey(User, related_name="owned_boards")
	# the join table created here makes sure User and Board are unique_together
	participants = models.ManyToManyField(User, related_name="participating_boards",
										blank=True, db_table="points_participates_in")
	creation_date = models.DateTimeField()
	def __unicode__(self):
		return self.owner.username + "/" + self.name + "." + unicode(self.id)
	class Meta:
		unique_together = ("name", "owner") # just for the owner's sanity

class Category(models.Model):
	"""A unique category of points on a board, e.g. "Hipster" or "Paragon"."""
	board = models.ForeignKey(Board)
	name = models.CharField(max_length=32)
	def __unicode__(self):
		return unicode(self.board) + "/" + self.name + "." + unicode(self.id)
	class Meta:
		unique_together = ("board", "name")

class Cell(models.Model):
	"""
	A cell in a board.
	Holds the number of points the user has in the given category.
	"""
	category = models.ForeignKey(Category)
	user = models.ForeignKey(User)
	points = models.IntegerField(default=0)
	def __unicode__(self):
		return unicode(self.category) + "/" + self.user.username + ":" +\
			unicode(self.points) + "." + unicode(self.id)
	class Meta:
		unique_together = ("category", "user")

class Transaction(models.Model):
	"""
	A transaction of points between two users on a board (not necessarily unique).
	The giver can supply a reason for the transaction, e.g. "for liking Josef K".
	"""
	board = models.ForeignKey(Board)
	category = models.ForeignKey(Category)
	points = models.IntegerField()
	reason = models.CharField(max_length=256)
	recipient = models.ForeignKey(User, related_name="received_transactions")
	giver = models.ForeignKey(User, related_name="given_transactions")
	creation_date = models.DateTimeField()
	def __unicode__(self):
		return unicode(self.board) + " " + unicode(self.giver) + " " +\
			unicode(self.points) + " " + self.category.name + " -> " + unicode(self.recipient)
