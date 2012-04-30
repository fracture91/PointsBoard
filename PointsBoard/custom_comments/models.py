import datetime
from django.db import models
from django.utils.translation import ugettext_lazy
from django.contrib.auth.models import User
from django.contrib.comments.models import BaseCommentAbstractModel
from django.conf import settings

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH',3000)


class MinComment(BaseCommentAbstractModel):
	user        = models.ForeignKey(User, verbose_name=ugettext_lazy('user'),
								blank=True, null=True, related_name="%(class)s_comments")
	comment     = models.TextField(ugettext_lazy('comment'), max_length=COMMENT_MAX_LENGTH)
	submit_date = models.DateTimeField(ugettext_lazy('date/time submitted'), default=None)
	is_public   = models.BooleanField(ugettext_lazy('is public'), default=True,
									help_text=ugettext_lazy('Uncheck this box to make the comment effectively ' \
											'disappear from the site.'))
	is_removed  = models.BooleanField(ugettext_lazy('is removed'), default=False,
									help_text=ugettext_lazy('Check this box if the comment is inappropriate. ' \
											'A "This comment has been removed" message will ' \
											'be displayed instead.'))
	
	class Meta:
		db_table = "django_comments"
		ordering = ('submit_date',)
		permissions = [("can_moderate", "Can moderate comments")]
		verbose_name = ugettext_lazy('comment')
		verbose_name_plural = ugettext_lazy('comments')
	
	def __unicode__(self):
		return "%s: %s..." % (self.user.username, self.comment[:50])
	
	def save(self, *args, **kwargs):
		if self.submit_date is None:
			self.submit_date = datetime.datetime.now()
		super(MinComment, self).save(*args, **kwargs)