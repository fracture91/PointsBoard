from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('points.views',
	url(r'^$', 'userBoards', name='userBoards'),
	url(r'^(?P<boardId>\d+)$', 'board', name='board'),
	url(r'^(?P<boardId>\d+)/transactions/(?P<transactionId>\d+)$', 'transaction', name='transaction'),
	url(r'^(?P<boardId>\d+)/transactions$', 'transaction', name='boardTransactions'),
	url(r'^(?P<boardId>\d+)/transactions/(?P<transactionId>\d+)/comments/(?P<commentId>\d+)$', 'comment', name='comment'),
	url(r'^(?P<boardId>\d+)/transactions/(?P<transactionId>\d+)/comments$', 'comment', name='transactionComments'),
)
