# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from . models import Movie
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator, InvalidPage

def index(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        movies = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        movies = paginator.page(paginator.num_pages)

    # Get the index of the current page
    index = movies.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 2 if index <= max_index - 2 else max_index

    page_range = list(paginator.page_range)[start_index:end_index-1]
    return render(request, 'movie/index.html', {
        'movies': movies, 'page_range':page_range, 'page': page,

    })


def detail(request,movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        raise Http404("Movie does not exist")
    return render(request, 'movie/detail.html', {'movie': movie})
