from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from app import forms as app_forms
from app import models as app_models
from app import utils as app_utils


def index(request):
    args = {
        'tests': app_models.Test.objects.all(),
    }
    return render_to_response('index.html', args, context_instance=RequestContext(request))


def tests(request):
    return redirect('index')


def test(request, test_id):
    args = {
        'test': get_object_or_404(app_models.Test, id=test_id)
    }
    return render_to_response('test.html', args, context_instance=RequestContext(request))


def create(request):
    if request.method == 'POST':
        test_form = app_forms.Test(request.POST, request.FILES)
        if test_form.is_valid():
            test = test_form.save()
            app_utils.request_screenshots(test)
            return redirect('test', test_id=test.id)
    else:
        test_form = app_forms.Test()

    return render_to_response('create.html', {'test_form': test_form}, context_instance=RequestContext(request))


def delete(request, test_id):
    test = get_object_or_404(app_models.Test, id=test_id)
    test.delete()
    # TODO delete media file
    return redirect('index')


def callback(request):
    # TODO
    print(request)


"""
def sync_all(request):
    for test in app_models.Test.objects.all():
        app_utils.get_screenshots(test)
    return redirect('index')
"""


def sync(request, test_id):
    app_utils.get_screenshots(get_object_or_404(app_models.Test, id=test_id))
    return redirect('test', test_id=test_id)
