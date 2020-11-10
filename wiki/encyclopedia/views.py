from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from . import util

class SearchTitleForm(forms.Form):
    title = forms.CharField(label="Search")

class CreateNewForm(forms.Form):
    new_title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id' : 'new-title',
                'class': 'form-control'
                }))
    content = forms.CharField(
        label="Content: ",
        widget=forms.Textarea(
            attrs={
                'id': 'new-content',
                'class': 'form-control'
                }))

# TODO: move this function into utils.py
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
    new_entry = CreateNewForm()
    return render(request, "encyclopedia/new.html", {
        "title": "Encyclopedia",
        "form": SearchTitleForm(),
        "new_entry_form": new_entry
    })

def save(request):
    if request.method == "POST":
        form = CreateNewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["new_title"]
            if match_title(title):
                return render(request, "encyclopedia/error.html", {
                    "message": str(f"Error: Entry for {title} already exists. Please give another title."),
                    "form": SearchTitleForm()
                })
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entry', args=[title]))
        else:
            return HttpResponse('invalid request')
            
