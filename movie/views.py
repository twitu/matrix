# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from . models import Movie
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def index(request):
    all_movies = Movie.objects.all()
    paginator = Paginator(all_movies, 10)

    page = request.GET.get('page', 1)

    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    # movies = paginator.get_page(page)

    return render(
        request,
        'movie/index.html',
        context={'movies': movies}
    )

def detail(request,movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        raise Http404("Movie does not exist")
    return render(request, 'movie/detail.html', {'movie': movie})
