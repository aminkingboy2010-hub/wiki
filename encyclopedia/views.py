from django.shortcuts import render, redirect
import markdown2
import random
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {"message": "Page not found."})
    else:
        html_content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    query = request.GET.get("q", "").strip()
    entries = util.list_entries()

    if query in entries:
        return redirect("entry", title=query)
    
    results = []
    for entry in entries:
        if query.lower() in entry.lower():
            results.append(entry)
            
    return render(request, "encyclopedia/search.html", {
        "query": query, 
        "results": results
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect("entry", title=title)
    else:
        return render(request, "encyclopedia/new.html")

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect("entry", title=title)
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title, 
            "content": content
        })

def random_page(request):
    entries = util.list_entries()
    if not entries:
        return redirect("index")
    
    random_title = random.choice(entries)
    return redirect("entry", title=random_title)