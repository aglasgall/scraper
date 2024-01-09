1. Install `poetry`
2. `poetry install` to install the app and its deps to a virtualenv
3. `poetry run playwright install` to install a browser `playwright` can use
4. `poetry run gunicorn -b 0.0.0.0:8000 -w 4 scraper.app:application` or similar

There are several environment variables the app expects to be set:
- `HUNT_LOGIN_URL`: URL of the login page for the Hunt site
- `PUZZLES_URL`: URL of the page with the textual list of all puzzles
- `HUNT_USERNAME`: Team username for the Hunt site
- `HUNT_PASSWORD`: Team password for the Hunt site

The app uses HTTP Basic authentication using the team username and
password because it's the internet and unauthenticated webapps are not
a great idea. You 100% want to put a reverse proxy with TLS in front
of this (to protect the password in flight) or run it under mod_wsgi
or the like or something instead of gunicorn. If you do that, you're
probably going to have the easiest time if you `poetry build` to get a
wheel file and then install `dist/scraper-0.1.0-py3-none-any.whl` in
that virtualenv instead of relying on poetry's virtualenv management.

Good luck!
