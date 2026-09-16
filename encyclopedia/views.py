from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render
from . import util
from random import choice
from markdown2 import Markdown


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="Content", widget=forms.Textarea(
        attrs={"class": "content-textarea"}))


class EditEntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="Content", widget=forms.Textarea(
        attrs={"class": "content-textarea"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    content = util.get_entry(entry)
    markdowner = Markdown()
    converted_content = markdowner.convert(content)
    return render(request, "encyclopedia/title.html", {
        "entry": entry,
        "content": content,
        "converted_content": converted_content
    })


def search(request):
    user_query = request.GET.get("q", "")
    if user_query:
        entry = util.get_entry(user_query)
        if entry:
            return redirect("encyclopedia:entry", user_query)
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
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) == None:
                filename = util.title_to_filename(title)
                util.save_entry(filename, content)
                return redirect("encyclopedia:entry", filename)
            else:
                messages.error(
                    request, "An entry with this title already exists.")
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm()
    })


def edit(request, entry):
    if request.method == "GET":
        title = entry
        content = util.get_entry(entry)
        form = EditEntryForm(initial={"title": title, "content": content})
        return render(request, "encyclopedia/edit.html", {
            "entry": entry,
            "form": form
        })
    elif request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            filename = util.title_to_filename(title)
            util.save_entry(filename, content)
            return redirect("encyclopedia:entry", filename)
        else:
            return render(request, "encyclopedia/edit.html", {
                "entry": entry,
                "form": form
            })


def random(request):
    entries = util.list_entries()
    random_entry = choice(entries)
    return redirect("encyclopedia:entry", random_entry)
