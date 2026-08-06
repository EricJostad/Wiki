from django.shortcuts import render
from flask import request

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, entry):
    return render(request, "encyclopedia/title.html", {
        "entry": util.get_entry(entry)
    })


def search(request):
    user_query = request.GET.get("q", "")
    if user_query:
        entry = util.get_entry(user_query)
        if entry:
            return render(request, "encyclopedia/title.html", {
                "entry": entry
            })
        else:
            pass


def new(request):
    return render(request, "encyclopedia/new.html")
