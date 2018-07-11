import click
import json, re, datetime, httplib, sys
import os,django
from populate_db import get_info_and_store
import populate_db

#add option 'name' to take input through cli
@click.command()
@click.option('--name',prompt='Name of movie',help='Adds movie to the database.')

def add(name):
		global conn
		global movie_id
				
		name = re.sub(r"\s+", "%20",name)
    		conn.request("GET", film.format(name), payload)
    		res = conn.getresponse()
    		data = json.loads(res.read())

		if not data['total_results']:
        		print("Could not find", name)
        		f.write(name+'\n')
        		f.flush()
    		else:
        		data_1 = data['results'][0]

     			# populating movie database
       			if Movie.objects.filter(name=data_1['title']):
            			object1 = Movie.objects.filter(name=data_1['title'])[0]
       			else:
           			if data_1['poster_path']:
                			object1 = Movie(name=data_1['title'],
                                	release=data_1['release_date'],
                                	poster=str(poster_path+data_1['poster_path']))
            			else:
                			object1 = Movie(name=data_1['title'],
                                	release=data_1['release_date'])
			movie_id = data_1['id']
				
			click.echo('Movie name,Release date:%s' %object1)
		
			# populating genre database
       	 		for j in data_1['genre_ids']:
            			if Genre.objects.filter(name=genre_dict[str(j)]):
                			object4 = Genre.objects.filter(name=genre_dict[str(j)])[0]
               			else:
                			object4 = Genre(name=genre_dict[str(j)])
								
				click.echo('Genre:%s' %object4)
				

			# getting movie credits to store actors and cast
        		conn.request("GET", credit.format(movie_id), payload)
        		res = conn.getresponse()
        		data = json.loads(res.read())
			 
			# populating director database
        		for k in data['crew']:
            			if k['job'] == "Director":
                			if Director.objects.filter(name=k['name']):
                    				object2 = Director.objects.filter(name=k['name'])[0]
                    				object2.movie_name.add(object1)
                    				break
                			else:
                    				object2 = Director(name=k['name'])
					
					
			click.echo('Director:%s' %object2)
				
			
			# populating actors database with only first seven or less actors
        		if len(data['cast']) < 7:
            			cast_range = len(data['cast'])
        		else:
            			cast_range = 7

        		for m in range(0,cast_range):
            			if Actor.objects.filter(name=data['cast'][m]['name']):
                			object3 = Actor.objects.filter(name=data['cast'][m]['name'])[0]
                			object3.movie_name.add(object1)
            			else:
                			object3 = Actor(name=data['cast'][m]['name'])
								
				click.echo('Actor:%s' %object3)

			debug = click.prompt('Do you want to save the movie to database? \n(y) for "yes" and (n) for "no"')
			if debug=='y':
				object1.save()
				
				print("stored:", data_1['title'])
				movie_id = data_1['id']
				# populating genre database
       	 			for j in data_1['genre_ids']:
            				if Genre.objects.filter(name=genre_dict[str(j)]):
                				object4 = Genre.objects.filter(name=genre_dict[str(j)])[0]
                				object4.movie_name.add(object1)
            				else:
                				object4 = Genre(name=genre_dict[str(j)])
						object4.save()	
						object4.movie_name.add(object1)

				# populating director database
        			for k in data['crew']:
            				if k['job'] == "Director":
                				if Director.objects.filter(name=k['name']):
                    					object2 = Director.objects.filter(name=k['name'])[0]
                    					object2.movie_name.add(object1)
                    					break
                				else:
                    					object2 = Director(name=k['name'])
							object2.save()
							object2.movie_name.add(object1)

				for m in range(0,cast_range):
            				if Actor.objects.filter(name=data['cast'][m]['name']):
                				object3 = Actor.objects.filter(name=data['cast'][m]['name'])[0]
                				object3.movie_name.add(object1)
            				else:
                				object3 = Actor(name=data['cast'][m]['name'])
						object3.save()
						object3.movie_name.add(object1)        			
               
			else:
				click.echo("Movie not stored in database")
					
if __name__=='__main__':
    # set up fixed headers, varicables and meta data
    conn = httplib.HTTPSConnection("api.themoviedb.org")
    poster_path = "https://image.tmdb.org/t/p/w640"
    payload = "{}"
    credit = "/3/movie/{}/credits?api_key=a0cda0670d10a1f96ea56ac1d70c5067"
    film = "/3/search/movie?include_adult=false&page=1&query={}&language=en-US&api_key=a0cda0670d10a1f96ea56ac1d70c5067"

    # genres dictionary
    genre_dict = {'37': u'Western', '10402': u'Music', '12': u'Adventure', '14': u'Fantasy',
                  '878': u'Science Fiction', '16': u'Animation', '18': u'Drama', '28': u'Action',
                  '36': u'History', '35': u'Comedy', '99': u'Documentary', '10770': u'TV Movie',
                  '27': u'Horror', '9648': u'Mystery', '10749': u'Romance', '10751': u'Family',
                  '80': u'Crime', '53': u'Thriller', '10752': u'War'}

    # configuring script to understance django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matrix.settings')
    django.setup()
    from movie.models import Movie, Actor, Director, Genre

    # collect movie names in a list
    text = open(r'list.txt', 'r').readlines()
   
    # file to store names that don't have data
    log = open(r'error_log.txt', 'a')
    log.write("\nScript running at" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").__str__() + "\n")
    
    print('Type "f" for file and "t" for cli')
    method=raw_input('Method for populating database(f or t):')
	
    if method== 't':
    	add()
    elif method=='f':
	 for name in text:
         	get_info_and_store(name.rstrip())
