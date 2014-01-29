from django.shortcuts import render, render_to_response, redirect
# Create your views here.

def Selector(request):
    return render_to_response('kiwi/selector.html')

def GooglePicker(request):
    return

def DropboxChooser(request):
    return