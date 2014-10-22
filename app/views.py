from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from app import forms as app_forms
from app import models as app_models
#from app import webkit2png


def index(request):
    args = {
        'tests': app_models.Test.objects.all(),
        'test_form': app_forms.Test()
    }

    return render_to_response('index.html', args, context_instance=RequestContext(request))


def create(request):
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


def delete(request, test_id):
    test = get_object_or_404(app_models.Test, id=test_id)
    test.delete()
    # TODO delete media file
    return redirect('index')
