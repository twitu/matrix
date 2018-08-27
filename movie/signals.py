from .models import Movie
from django.db.models.signals import post_save
from django.dispatch import receiver
# adding a signal that fires .indexing() saved after every new post
@receiver(post_save, sender = Movie)
def index_post(sender, instance, **kwargs):
    instance.indexing()


# The post_save signal will ensure that the saved instance will
# get indexed with the .indexing() method after it is saved
