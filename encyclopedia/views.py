from django.shortcuts import render

from . import util
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
import random

class AddPageForm(forms.Form):
    title = forms.CharField(label='Title',max_length=100)
    markdown_content = forms.CharField(
    label='Entry Content:',
    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 25})
)
class EditPageForm(forms.Form):
    markdown_content = forms.CharField(
    label='Entry Content:',
    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 25})
)


def index(request):
    if 'q' in request.GET:
        search_query = request.GET['q']
        return HttpResponseRedirect(reverse("entry",args=(search_query,)))

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def entry(request,title):
    html_content = util.convert_md_to_html(title)

    # If HTML content is available, render the entry page
    if html_content:
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "content": html_content
        })

    # If exact entry not found, get a list of all entries and search for similar entries
    entries = util.list_entries()
    similar_entries = []
    lowered_title = title.lower()
    similar_entries = [entry for entry in entries if title in entry.lower()]
    if similar_entries:        
        return render(request,"encyclopedia/subtitle.html",{'similar_entries':similar_entries})

    # If no content or similar entries found, display a "not found" message
    return HttpResponse(f"The requested page for \"{title}\" was not found.")


def addpage(request):
    if request.method == 'POST':
        form = AddPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['markdown_content']
            if title not in util.list_entries():
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry",args=(title,)))
            else:
                return HttpResponse(f"Entry page for \"{title}\" already exist!")

    return render(request,"encyclopedia/addpage.html",{
        "form": AddPageForm()
    })


def editpage(request,title):
    content = util.get_entry(title)
    if request.method == 'POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            updated_content = form.cleaned_data['markdown_content']
            if content != updated_content:
                util.save_entry(title,updated_content)
            return HttpResponseRedirect(reverse("entry",args=(title,)))

    return render(request,"encyclopedia/editpage.html",{
        "form": EditPageForm(initial= {'markdown_content': content})
    })    


def randompage(request):
    random_page = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry",args=(random_page,)))