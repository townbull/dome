from django.http import HttpRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
#from dome.auth import BaseDriveHandler, DriveState
from skymesh_dashboard import settings
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError


def authredirect(request):
    gauth = GoogleAuth()
    gauth.GetFlow()
    oauth_callback = request.build_absolute_uri() + "gdrive"
    gauth.flow.redirect_uri = oauth_callback
    auth_url = gauth.GetAuthUrl()
    return HttpResponseRedirect(auth_url)


class IndexView(generic.ListView):
    template_name = 'dome/home.html'
    context_object_name = 'obj_list'
    code = ""

    def get_queryset(self):
        """Return the last five object files."""

        drive = self.get_gdrive()

        # Auto-iterate through all files that matches this query
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        return file_list

    def get_gdrive(self):
        """Return google drive handler"""

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
        drive = GoogleDrive(gauth)
        return drive
