# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from . models import Movie
from django.shortcuts import render

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
