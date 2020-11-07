from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from . import util

class SearchTitleForm(forms.Form):
    title = forms.CharField(label="Search")

class CreateNewForm(forms.Form):
    new_title = forms.CharField(label="Title: ")
    content = forms.CharField(label="Content: ", widget=forms.Textarea)
    
def match_title(title):
    # Returns True if a complete match
    if title.lower() in [entry.lower() for entry in util.list_entries()]:
        return True
    return False

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title": "Encyclopedia",
        "form": SearchTitleForm()
    })

def entry(request, title):
    if not match_title(title):
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
        matched_entries = [entry for entry in util.list_entries() if title.lower() in entry.lower()]
        # If query string returns partial matches
        if not match_title(title) and matched_entries: 
            return render(request, "encyclopedia/index.html", {
                "entries": matched_entries,
                "title": "Encyclopedia",
                "form": SearchTitleForm()
            })
        else:
            return entry(request, title)
    else: 
        return render(request, "encyclopedia/index.html", {
            "form": SearchTitleForm(),
            "entry": str(f"invalid input"),
            "title": "Encyclopedia"
        })

def new(request):
    new_entry= CreateNewForm()
    return render(request, "encyclopedia/index.html", {
        "title": "Encyclopedia",
        "form": SearchTitleForm(),
        "new_entry_form": new_entry
    })
