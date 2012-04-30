import datetime
from django import forms
from django.contrib.comments.forms import CommentSecurityForm
from custom_comments.models import MinComment
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy
from django.conf import settings


COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH',3000)

class MinCommentForm(CommentSecurityForm):
	comment       = forms.CharField(label=ugettext_lazy('Comment'), widget=forms.Textarea({}),
                                    max_length=COMMENT_MAX_LENGTH)
	
	def get_comment_model(self):
		return MinComment
	
	def get_comment_create_data(self):
		"""
		Returns the dict of data to be used to create a comment.
		"""
		return dict(
			object_pk    = force_unicode(self.target_object._get_pk_val()),
			comment      = self.cleaned_data["comment"],
			submit_date  = datetime.datetime.now(),
			site_id      = settings.SITE_ID,
			is_public    = True,
			is_removed   = False,
		)