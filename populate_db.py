import datetime
import django
import httplib
import json
import os
import re

import click


def add(name, debug, log):
    if debug == 'y':
        debug = True
    else:
        debug = False

    name = re.sub(u"\s+", "%20", name)
    conn.request("GET", film.format(name), payload)
    res = conn.getresponse()
    data_movie = json.loads(res.read())

    if not data_movie['total_results']:
        print("Could not find ", name)
        log.write(name + '\n')
        log.flush()
    else:
        movie_data = data_movie['results'][0]

        # populating movie database
        if Movie.objects.filter(name=movie_data['title']):
            movie_object = Movie.objects.filter(name=movie_data['title'])[0]
        else:
            if movie_data['poster_path']:
                movie_object = Movie(name=movie_data['title'],
                                     release=movie_data['release_date'],
                                     poster=str(poster_path + movie_data['poster_path']))
            else:
                movie_object = Movie(name=movie_data['title'],
                                     release=movie_data['release_date'])
        movie_id = movie_data['id']

        if debug:
            click.echo(u'Movie name, Release date: {}'.format(movie_object))

        if debug:
            # print genres for debugging
            for j in movie_data['genre_ids']:
                click.echo(u'Genre: {}'.format(genre_dict[str(j)]))

        # getting movie credits to store crew and cast
        conn.request("GET", credit.format(movie_id), payload)
        res = conn.getresponse()
        crew_data = json.loads(res.read())

        # print director for debugging
        if debug:
            for k in crew_data['crew']:
                if k['job'] == "Director":
                    click.echo(u'Director: {}'.format(k["name"]))

        cast_range = min(10, len(crew_data['cast']))  # number of actors to be saved is less than 10

        # print actors for debugging
        if debug:
            for m in range(0, cast_range):
                click.echo(u'Actor: {}'.format(crew_data['cast'][m]['name']))

        # getting keywords for movie
        conn.request("GET", keywords.format(movie_id), payload)
        res = conn.getresponse()
        key_word_data = json.loads(res.read())

        # print keywords for debugging
        if debug:
            for keyword in key_word_data["keywords"]:
                click.echo(u'Keyword: {}'.format(keyword["name"]))

        if debug:
            save = ''
            while save != 'y' and save != 'n':
                save = click.prompt("\nDo you want to save the movie to database? \n(y) for \"yes\" and (n) for \"no\"")
        else:
            save = 'y'

        if save == 'y':
            movie_object.save()

            # populating genre database
            for j in movie_data['genre_ids']:
                if Genre.objects.filter(name=genre_dict[str(j)]):
                    genre_object = Genre.objects.filter(name=genre_dict[str(j)])[0]
                    genre_object.movie_name.add(movie_object)
                else:
                    genre_object = Genre(name=genre_dict[str(j)])
                    genre_object.save()
                    genre_object.movie_name.add(movie_object)

            # populating director database
            for k in crew_data['crew']:
                if k['job'] == "Director":
                    if Director.objects.filter(name=k['name']):
                        director_object = Director.objects.filter(name=k['name'])[0]
                        director_object.movie_name.add(movie_object)
                        break
                    else:
                        director_object = Director(name=k['name'])
                        director_object.save()
                        director_object.movie_name.add(movie_object)

            # populating actor database
            for m in range(0, cast_range):
                if Actor.objects.filter(name=crew_data['cast'][m]['name']):
                    actor_object = Actor.objects.filter(name=crew_data['cast'][m]['name'])[0]
                    actor_object.movie_name.add(movie_object)
                else:
                    actor_object = Actor(name=crew_data['cast'][m]['name'])
                    actor_object.save()
                    actor_object.movie_name.add(movie_object)

            # populating keyword database
            for keyword in key_word_data["keywords"]:
                if Keyword.objects.filter(database_id=keyword["id"]):
                    keyword_object = Keyword.objects.filter(database_id=keyword["id"])[0]
                    keyword_object.movie_name.add(movie_object)
                else:
                    keyword_object = Keyword(database_id=keyword["id"], name=keyword["name"])
                    keyword_object.save()
                    keyword_object.movie_name.add(movie_object)

            print(u"stored: {} {}\n".format(movie_data['title'], movie_data['release_date']))
        else:
            click.echo("Movie not stored in database")


if __name__ == '__main__':
    # set up fixed headers, variables and meta data
    conn = httplib.HTTPSConnection("api.themoviedb.org")
    # w342 determines size of poster that will be loaded, it can be changed according to API specifications
    poster_path = "https://image.tmdb.org/t/p/w342"
    payload = "{}"
    credit = "/3/movie/{}/credits?api_key=a0cda0670d10a1f96ea56ac1d70c5067"
    keywords = "/3/movie/{}/keywords?api_key=a0cda0670d10a1f96ea56ac1d70c5067"
    film = "/3/search/movie?include_adult=false&page=1&query={}&language=en-US&api_key=a0cda0670d10a1f96ea56ac1d70c5067"

    # genres dictionary
    genre_dict = {'37': u'Western', '10402': u'Music', '12': u'Adventure', '14': u'Fantasy',
                  '878': u'Science Fiction', '16': u'Animation', '18': u'Drama', '28': u'Action',
                  '36': u'History', '35': u'Comedy', '99': u'Documentary', '10770': u'TV Movie',
                  '27': u'Horror', '9648': u'Mystery', '10749': u'Romance', '10751': u'Family',
                  '80': u'Crime', '53': u'Thriller', '10752': u'War'}

    # configuring script to understand django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matrix.settings')
    django.setup()
    from movie.models import Movie, Actor, Director, Genre, Keyword

    # ask user for single or file mode
    mode = ''
    while mode != 's' and mode != 'f':
        mode = click.prompt("\nDo you want to use populate in single movie or file mode ?\n"
                            "Please enter (s) for single or (f) for file mode")

    # collect movie names is name list
    name = []
    if mode == 's':
        name.append(click.prompt("\nPlease enter name of movie you want to add to database"))
    else:
        filename = click.prompt("\nPlease enter name of file (leave blank for default)", default="list.txt")
        with open(filename, 'r') as batch:
            name = batch.readlines()

    # file to store names that don't have data
    log = open(r'error_log.txt', 'a')
    log.write("\nScript running at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").__str__() + "\n")

    # check for debug mode
    debug = ''
    while debug != 'y' and debug != 'n':
        debug = click.prompt("\nDo you want to use debug mode ?\n"
                             "Please enter (y) for yes or (n) for no")

    for movie in name:
        add(movie.rstrip(), debug, log)
