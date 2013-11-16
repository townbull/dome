from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from skymesh_dashboard import settings
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class IndexView(generic.ListView):
    template_name = 'dome/index.html'
    context_object_name = 'obj_list'

    def get_queryset(self):
        """Return the last five object files."""
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        # Auto-iterate through all files that matches this query
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        return file_list
