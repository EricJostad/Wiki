from django import forms
from django.shortcuts import redirect, render
from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)


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
            return redirect("encyclopedia:title", user_query)
        else:
            matches = []
            entries = util.list_entries()
            for entry in entries:
                if user_query.lower() in entry.lower():
                    matches.append(entry)
            return render(request, "encyclopedia/search.html", {
                "query": user_query,
                "results": matches
            })
    else:
        return None


def new(request):
    return render(request, "encyclopedia/new.html")
