# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim


# Install poetry
RUN pip install poetry


# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
	&& poetry install --no-dev --no-interaction --no-ansi


ADD ./piri_web /app
WORKDIR /app


# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 2 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 2 'app:application'
