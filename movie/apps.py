# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class MovieConfig(AppConfig):
    name = 'movie'
    # To register that we are using signals
    def ready(self):
        import movie.signals
