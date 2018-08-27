from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search
# The DocType works as a wrapper to enable you to write an index like a model
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
import models # using from . not working


# global connection with elasticsearch set up
connections.create_connection()

# define what to index here



class MovieIndex(DocType):
    name = Text()
    release = Text()

    class Meta:
        index = 'movie-index'

# bulk indexing, run in terminal
def bulk_indexing():
    MovieIndex.init(index='movie-index')
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.Movie.objects.all().iterator()))

def search(name):
    s = Search().filter('term', name=name)
    response = s.execute()
    return response
