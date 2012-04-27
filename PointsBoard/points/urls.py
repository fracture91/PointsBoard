from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('points.views',
	url(r'^$', 'userBoards', name='userBoards'),
	url(r'^(?P<boardId>\d+)$', 'board', name='board'),
	url(r'^(?P<boardId>\d+)/transactions/(?P<transactionId>\d+)$', 'transaction', name='transaction'),
)