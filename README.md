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
    
6. Start the application.
    ```bash
    python manage.py runserver
    ```