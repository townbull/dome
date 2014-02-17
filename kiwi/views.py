from django.shortcuts import render, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from models import FileInfo
import json, datetime

# Create your views here.

def Selector(request):
    return render_to_response('kiwi/selector.html')


def GooglePicker(request):
    return


def DropboxChooser(request):
    return

def SaveInfoGoogle(request):
    print 'jquery post received from google'
    print request.POST.get('files')
    files = json.loads(request.POST.get('files'))
    src = request.POST.get('source')
    for f in files:
        #print f["link"], f["bytes"], f["link"], f["icon"]
        print datetime.datetime.fromtimestamp(int(f["lastEditedUtc"])/1000.0)
        file = FileInfo(name=f["name"], link=f["url"], size=int(f["sizeBytes"]), icon=f["iconUrl"],source = src,lastEditTime=datetime.datetime.fromtimestamp(int(f["lastEditedUtc"])/1000.0))

        print 'google file set done'
        file.save()
        print 'google record save success'

    return render_to_response('kiwi/selector.html')


#@csrf_exempt
def SaveInfoDropbox(request):
    # save information of dropbox item in db, return all existing items
    print 'jquery post received from dropbox'
    print request.POST.get('files')
    files = json.loads(request.POST.get('files'))
    src = request.POST.get('source')

    for f in files:
        #print f["link"], f["bytes"], f["link"], f["icon"]
        file = FileInfo(name=f["name"], link=f["link"], size=int(f["bytes"]), icon=f["icon"],source = src )
        # icon=f["icon"], thumbnail=f["thumbnail"])
        print 'dropbox file set done'
        file.save()
        print 'dropbox record save success'

    return render_to_response('kiwi/selector.html')
        #json.loads(FileInfo.objects.all())

def Showlist(request):
    files = FileInfo.objects.all()
    data = serializers.serialize('json', files)
    data = '{"files":'+ data + '}'
    return HttpResponse(data, content_type='application/json')
