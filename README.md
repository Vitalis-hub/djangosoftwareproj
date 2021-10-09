# UCO Wheelchair Direction App

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/FendyPierre/UCOMap.git
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```
(env)$ python manage.py runserver
```

You can update Locations, Campus and Entrances in admin
```
http://127.0.0.1:8000/admin/
```

You can login with user `testuser` password `password` or create a user:
```
(env)$ python manage.py createsuperuser
```