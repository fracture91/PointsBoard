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
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=512, blank=True)
	owner = models.ForeignKey(User, related_name="owned_boards")
	# the join table created here makes sure User and Board are unique_together
	participants = models.ManyToManyField(User, related_name="participating_boards",
										blank=True, db_table="participates_in")
	creation_date = models.DateTimeField()
	class Meta:
		unique_together = ("name", "owner") # just for the owner's sanity

class Category(models.Model):
	board = models.ForeignKey(Board)
	name = models.CharField(max_length=32)
	class Meta:
		unique_together = ("board", "name")

class Cell(models.Model):
	category = models.ForeignKey(Category)
	user = models.ForeignKey(User)
	class Meta:
		unique_together = ("category", "user")

class Transaction(models.Model):
	board = models.ForeignKey(Board)
	category = models.ForeignKey(Category)
	value = models.IntegerField()
	reason = models.CharField(max_length=256)
	recipient = models.ForeignKey(User, related_name="received_transactions")
	giver = models.ForeignKey(User, related_name="given_transactions")
	creation_date = models.DateTimeField()
