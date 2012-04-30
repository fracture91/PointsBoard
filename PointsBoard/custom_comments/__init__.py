from custom_comments.models import MinComment
from custom_comments.forms import MinCommentForm

def get_model():
	return MinComment
 
def get_form():
	return MinCommentForm