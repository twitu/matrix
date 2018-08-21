from __future__ import unicode_literals

from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    release = models.CharField(max_length=20, default="N/A")
    poster = models.URLField(max_length=100, null=True)

    def __unicode__(self):
        return "".join([self.name, " ", self.release])

    class Meta:
        ordering = ("name",)


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
