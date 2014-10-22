from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from .models import Greeting

# Create your views here.
def index(request):
    
    return render_to_response('index.html', {}, context_instance=RequestContext(request))
