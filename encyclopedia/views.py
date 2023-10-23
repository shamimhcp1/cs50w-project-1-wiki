from django.shortcuts import render, redirect
from django.http import HttpResponse
from markdown2 import Markdown # convert Markdown to HTML.
import random
from django.urls import reverse
from django.http import HttpResponseRedirect
import re


from . import util
markdowner = Markdown()

def index(request):

    # Check if method is POST
    if request.method == "POST":
        # Search for an encyclopedia entry
        query = request.POST['q'].lower()
        entries = util.list_entries()
        lowered_entries = []
        for entry in entries:
            lowered_entries.append(entry.lower())
        if query in lowered_entries:
            return HttpResponseRedirect(f"wiki/{query}")
        else:
            matched_query = []
            for entry in entries:
                match = re.search(f"{query}", entry, re.IGNORECASE)
                if match:
                    matched_query.append(entry)
            
            return render(request, "encyclopedia/search-wiki.html", {
                "matched_query": matched_query,
                "query" : query
            })


    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, title):
    # calling 'util' function.
    content = util.get_entry(title)

    # render contents of that encyclopedia entry.
    if content:
        return render(request, "encyclopedia/content.html", {
            "title" : title,
            "content": markdowner.convert(content)
        })
    
    # entry does not exist
    else:
        return render(request, "encyclopedia/content.html", {
            "title" : title,
            "content": None
        })
    
def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    return HttpResponseRedirect(f"wiki/{random_title}")

# edit a entry
def edit(request, title):
    content = util.get_entry(title)

    if request.method == 'POST':
        # remove extra line with replace
        markdown_content = request.POST['content'].replace('\r\n', '\n')
        # save edited entry
        util.save_entry(title, markdown_content)
        # return entry page
        return redirect('get_entry', title=title)

    return render(request, "encyclopedia/edit.html", {
        "title" : title,
        "content" : content
    })

# create new page
def create_page(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content'].replace('\r\n', '\n')
        entries = util.list_entries()
        lowered_entries = []
        for entry in entries:
            lowered_entries.append(entry.lower())
        # check if entry already exist
        if title.lower() in lowered_entries:
            return render(request, "encyclopedia/create.html", {
                "title" : title,
                "content" : content,
                "status" : "failed"
            })
        # if entry not exist create new page
        else:
            util.save_entry(title, content)
            return redirect('get_entry', title=title)
    
    return render(request, "encyclopedia/create.html", {
        "title" : "",
        "content" : "",
        "status" : ""
    })