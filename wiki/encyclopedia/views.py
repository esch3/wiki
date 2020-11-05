from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from . import util

class SearchTitleForm(forms.Form):
    title = forms.CharField(label="Search")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title": "Encyclopedia",
        "form": SearchTitleForm()
    })

def entry(request, title):
    if title.lower() not in [entry.lower() for entry in util.list_entries()]:
        return render(request, "encyclopedia/index.html", {
            "entry": str(f"{title} not found"),
            "title": "Encyclopedia"
        })

    return render(request, "encyclopedia/index.html", {
        "entry": util.get_entry(title),
        "title": title
    })

def search(request):
    return HttpResponse("hello there")
