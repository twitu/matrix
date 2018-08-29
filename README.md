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
    * Using another terminal, activate the virtualenv and go into the Django shell for bulk indexing of data.
    ```bash
    python manage.py shell
   
    >from movie.search import *
    >bulk_indexing()
    ```

7. Start the application.
    ```bash
    python manage.py runserver
    ```
    
