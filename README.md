Running the app in dev mode
---------------------------

On debian install poetry:

```
apt install python3-poetry
```

Run this command in clonned directory (here: /app/fadin/):

```
git clone ...
cd fadin
poetry install
```

Activate the environment (in /app/fadin/ dir) is done by:

```
poetry shell
```

Inside the shell run `uvicorn` this way:

```
uvicorn app.asgi:application --reload
```

You should get something similar:

```
(fadin-py3.11) user@linux:/app/fadin/fadin$ uvicorn app.asgi:application --reload
INFO:     Will watch for changes in these directories: ['/app/fadin/fadin']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [39134] using StatReload
INFO:     Started server process [39136]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Environment
-----------

This project uses `django-environ` package.

You can create `.env` file to store your environment varialbles.

Example `.env` file contents:

```
DATABASE_URL=postgres://fadin:fadin@localhost:5432/fadin
DEBUG=True
DJANGO_SETTINGS_MODULE=app.settings
```