# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from . models import Movie
from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages
from django.http import *
from . models import *


def index(request):
    all_movies = Movie.objects.all()

    return render(
        request,
        'movie/index.html',
        context={'all_movies': all_movies,}
    )

def detail(request,movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        raise Http404("Movie does not exist")
    return render(request, 'movie/detail.html', {'movie': movie})

def search(request):
    if request.method == "POST":
        srch = request.POST['srh']

        if srch:
            match= Movie.objects.filter(Q(name__icontains=srch)|Q(release__icontains=srch))
            if match:
                return render(request,'search.html', {'sr':match})
            else:
                messages.error(request,'no result found')
        else:
            return HttpResponseRedirect('/search/')
    return render(request, 'search.html')
