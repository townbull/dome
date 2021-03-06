from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from models import FileInfo
from allauth.socialaccount.models import SocialToken
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.conf import settings


def Selector(request):
    #print "request user:", request.user
    if not request.user.is_authenticated():
        login_url = getattr(settings, 'LOGIN_URL', None)
        return redirect('%s?next=%s' % (login_url, request.path))
    return render(request, 'kiwi/selector_bak.html')


def GooglePicker(request):
    pass


def DropboxChooser(request):
    pass


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

    return render(request, 'kiwi/selector_bak.html')


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

    return render('kiwi/selector_bak.html')
        #json.loads(FileInfo.objects.all())

def Showlist(request):
    files = FileInfo.objects.all()
    data = serializers.serialize('json', files)
    data = '{"files":'+ data + '}'
    return HttpResponse(data, content_type='application/json')

def GetToken(request):
    accountId = request.POST.get('accountId')
    record = SocialToken.objects.get(account=accountId)
    token = record.token
    print token
    data = '{"token":"'+ token + '"}'
    print data
    return HttpResponse(data, content_type='application/json')
