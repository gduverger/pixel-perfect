from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from app import forms as app_forms
from app import models as app_models


def index(request):
    args = {
        'tests': app_models.Test.objects.all(),
        'test_form': app_forms.Test()
    }

    return render_to_response('index.html', args, context_instance=RequestContext(request))


def upload(request):
    if request.method == 'POST':
        test_form = app_forms.Test(request.POST, request.FILES)
        if test_form.is_valid():
            test_form.save()
            return redirect('index')
    else:
        test_form = app_forms.Test()

    args = {
        'tests': app_models.Test.objects.all(),
        'test_form': test_form
    }

    return render_to_response('index.html', args, context_instance=RequestContext(request))
