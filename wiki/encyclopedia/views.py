from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title.lower() not in [entry.lower() for entry in util.list_entries()]:
        return render(request, "encyclopedia/index.html", {
            "entry": str(f"{title} not found")
        })

    return render(request, "encyclopedia/index.html", {
        "entry": util.get_entry(title)
    })



