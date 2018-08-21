# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from movie.models import Movie, Actor, Director, Genre, Keyword

admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Genre)
admin.site.register(Keyword)
