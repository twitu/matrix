from . import views
from django.conf.urls import url, include

urlpatterns =[
    #/music/
    url(r'^$',views.index, name='index'),
    #/music/21/
    url(r'^(?P<movie_id>[0-9]+)/$',views.detail, name='detail'),
    #/search/
    url(r'^search/', include('haystack.urls'))
]
