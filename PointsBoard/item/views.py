from django.template import RequestContext
from models import Item
from django.shortcuts import render_to_response
from datetime import datetime

def index(request):
	if request.method == "POST":
		newItem = Item(creation_date=datetime.now())
		newItem.save()
	
	items = Item.objects.all().order_by('creation_date')
	return render_to_response('item/index.html',
							{'item_list': items},
							context_instance=RequestContext(request));