from django.shortcuts import redirect, render
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
            return redirect("encyclopedia:title", user_query)
        else:
            pass


def new(request):
    return render(request, "encyclopedia/new.html")
