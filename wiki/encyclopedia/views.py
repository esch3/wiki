from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
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
            "title": "Encyclopedia",
            "form": SearchTitleForm()
        })

    return render(request, "encyclopedia/index.html", {
        "entry": util.get_entry(title),
        "title": title,
        "form": SearchTitleForm()
    })

def search(request):
    form = SearchTitleForm(request.GET)
    if form.is_valid():
        title = form.cleaned_data["title"]
        return entry(request, title)
    else: 
        return render(request, "encyclopedia/index.html", {
            "form": SearchTitleForm()
        })

