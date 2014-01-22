from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from skymesh_dashboard.settings import LOGIN_URL


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    c = {}
    c.update(csrf(request))
    state = "OK"
    # username = ''
    # password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #state = "You're successfully logged in!"
                return redirect(request.POST.get('next'))
            else:
                state = "N/A"
        else:
            state = "AGAIN"

    return render_to_response('acorn/login.html',
                              dict({'state':state,
                                    'next':'/'}, **c))