# Image will be based on a version of Debian with Python3.8 preinstalled
FROM python:3.8-slim-buster

# Copy all the files necessary for the code to run
COPY src/*.py /app/
# Copy all the assets (e.g., images)
COPY assets /assets
# Copy the file specifying our dependencies
COPY requirements.txt /

# Install our dependencies
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Open port 2522 to the outside world
EXPOSE 2522

# Environment variable will be visible from within the Python program
ENV IP_TO_LISTEN_ON="0.0.0.0"

ARG NUM_WORKERS=3
ARG NUM_THREADS_PER_WORKER=1

ENV NUM_WORKERS ${NUM_WORKERS}
ENV NUM_THREADS_PER_WORKER ${NUM_THREADS_PER_WORKER}

# Command to run when the Docker image starts, this command launches our server (gunicorn) allowing it to serve clients
CMD gunicorn -b "0.0.0.0:2522" -w ${NUM_WORKERS} --threads ${NUM_THREADS_PER_WORKER} --chdir "app" "app:server"
