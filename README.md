# matrix
Code base for MATRIX website

## Installation
1. Clone or download the repository. 
2. Create a new virtual environment for the project.
    ```bash
    virtualenv venv
    source venv/bin/activate
    ```
3. Install required python libraries giving in the requirements.txt file.
    ```bash
    pip install -r requirements.txt
    ```
4. Run Django migrations.
    
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5. Populate database with names from list.txt   
    ```bash
    python populate_db.py
    ```
    
6. Perform bulk indexing of data.
    
    * Download elasticsearch and activate it. 
    ```bash
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.1.1.tar.gz
    tar -xzf elasticsearch-5.1.1.tar.gz
    ./elasticsearch-5.1.1/bin/elasticsearch
    ```
    * Using another terminal (let elasticsearch run in the background), activate the virtualenv and go into the Django shell for bulk indexing of data.
    ```bash
    python manage.py shell
   
    from movie.search import *
    bulk_indexing()
    ``` 
    * To confirm bulk indexing of data quit the shell and run the following curl command.
    ```bash
    curl -XGET 'localhost:9200/movie-index?pretty' 
    ```
    * In case of Invoke-WebRequest error, run this command and try again.
    ```bash
    remove-item alias:\curl
    ```
7. To test out the search functionality run the following commands in the shell.
     ```bash
    python manage.py shell
    
    from movie.search import *
    print(search(name="<movie name>")) # use 'thor', for example.  
    ```
    * The response should be something like this. 
     ```bash
     <Response: [<Hit(movie-index/doc/AWXKb2DCkOlAI_7rRErW): {u'release': u'thor', u'name': u'thor'}>, <Hit(movie-index/doc/AWXKb2DVkOlAI_7rRErX): {u'release': u'thor', u'name': u'thor'}>]>   
     ```

8. Start the application.
    ```bash
    python manage.py runserver
    ```
    

