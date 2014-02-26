from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from models import FileInfo
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.conf import settings


def Selector(request):
    #print "request user:", request.user
    if not request.user.is_authenticated():
        login_url = getattr(settings, 'LOGIN_URL', None)
        return redirect('%s?next=%s' % (login_url, request.path))
    return render(request, 'dome/selector.html')


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

    return render(request, 'dome/selector.html')


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

    return render(request, 'dome/selector.html')
        #json.loads(FileInfo.objects.all())


def Showlist(request):
    files = FileInfo.objects.all()
    data = serializers.serialize('json', files)
    data = '{"files":'+ data + '}'
    return HttpResponse(data, content_type='application/json')


"""
@login_required
def authredirect(request):
    gauth = GoogleAuth()
    gauth.GetFlow()
    oauth_callback = request.build_absolute_uri() + "gdrive"
    gauth.flow.redirect_uri = oauth_callback
    auth_url = gauth.GetAuthUrl()
    return HttpResponseRedirect(auth_url)

class IndexView(generic.ListView):
    template_name = 'dome/index.html'
    context_object_name = 'obj_list'
    code = ""

    def get_queryset(self):
        #Return the last five object files.

        drive = self.get_gdrive()

        # Auto-iterate through all files that matches this query
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        return file_list

    def get_gdrive(self):
        #Return google drive handler

        # recreate auth flow handling code exchange
        # require flow.redirect_uri matching the code generation flow
        gauth = GoogleAuth()
        gauth.GetFlow()
        oauth_callback = self.request.build_absolute_uri()
        oauth_callback = oauth_callback.split('?', 1)[0].rsplit('/', 1)[0]

        gauth.flow.redirect_uri = oauth_callback
        code = self.request.GET.get('code')
        print "TB: code = ", code

        # Authenticate and authorize the code
        gauth.Auth(code)
        print "gauth credentials: ", gauth.credentials.to_json()
        drive = GoogleDrive(gauth)
        return drive
"""
