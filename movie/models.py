from __future__ import unicode_literals
from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User
from .search import MovieIndex
from django.db.models.signals import post_save
from django.dispatch import receiver



class Movie(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    release = models.CharField(max_length=20, default="N/A")
    poster = models.URLField(max_length=100, null=True)

    def __unicode__(self):
        return "".join([self.name, " ", self.release])

    # Add indexing method
    def indexing(self):
        obj = MovieIndex(
            # meta = {'id : self.id'}, need not use that.
            name = self.name,
            release = self.release
        )
        obj.save(index='movie-index')
        return obj.to_dict(include_meta=True)

    class Meta:
        ordering = ("name",)


@receiver(post_save, sender = Movie)
def index_post(sender, instance, **kwargs):
    instance.indexing()



class Actor(models.Model):
    name = models.CharField(max_length=50)
    movie_name = models.ManyToManyField(Movie)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Director(models.Model):
    name = models.CharField(max_length=50)
    movie_name = models.ManyToManyField(Movie)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Genre(models.Model):
    name = models.CharField(max_length=100)
    movie_name = models.ManyToManyField(Movie)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Keyword(models.Model):
    database_id = models.IntegerField()
    name = models.CharField(max_length=100)
    movie_name = models.ManyToManyField(Movie)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ("name",)
