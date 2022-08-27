# Whale
Whale is a "Music Streaming" website developed with Django.

## Overview
Users can share music with others.

The main features that have currently been implemented are:

* Listen songs (no need to login)
* Music player functions(play, pause, next, previous, timestamp)
* Comment the song.
* Add to favourite list.
* Upload songs.
* Edit and Delete own songs.
* Authentication and authorization
* User Profile
* Follow / Unfollow

## Entity–relationship Diagram
![Entity–relationship model](https://github.com/pyaephyokyaw15/Whale/blob/main/ERD.png)
> **Note:** Click and download the image to see details.

## Quick Start

To get this project up and running locally on your computer:
1. Set up the Python development environment.
   > **Note:** I want to recommend using a Python virtual environment.
   
1. Create .env file in the project root directory and create variables used in settings.py.
   > **Note:** >  os.getenv() in settings.py
1. Assuming you have Python setup, run the following commands (if you're on Windows you may use `py` or `py -3` instead of `python` to start Python):
   ```
   pip3 install -r requirements.txt
   python3 manage.py makemigrations
   python3 manage.py migrate
   python3 manage.py collectstatic
   python3 manage.py test # Run the standard tests. These should all pass.
   python3 manage.py createsuperuser # Create a superuser
   python3 manage.py runserver
   ```
1. Open a browser to `http://127.0.0.1:8000.
 
1. Admin Site: `http://127.0.0.1:8000/admin` 
