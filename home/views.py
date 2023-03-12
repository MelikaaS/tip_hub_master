from django.db.models import Q
from django.shortcuts import render

from post_details.models import Post


def home(request):
    context={}
    post=Post.objects.all()
    context['post'] = post
    return render(request,'home/home.html',context)

def search(request):
    context={}
    search_query= request.GET.get('search_query')
    blog=Post.objects.filter(Q(text__icontains=search_query) | Q(headline__icontains=search_query))
    context['post']=blog    #the value of context should be the same as the cintext send to home.htmlin other function. here home function
    return render(request, 'home/home.html', context)
