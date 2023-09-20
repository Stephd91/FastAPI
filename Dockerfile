# Start from the official Python base image.
FROM python:3.10

# Metadata for Docker image
LABEL org.opencontainers.image.source=https://github.com/Stephd91/FastAPI
LABEL org.opencontainers.image.description="Fastapi container image"

# Set the current working directory to /code.
# This is where we'll put the requirements.txt file and the app directory.
WORKDIR /code

# Copy the file with the requirements to the /code directory.
# As this file doesn't change often, Docker will detect it and use the cache
# for this step, enabling the cache for the next step too.
COPY ./requirements.txt /code/requirements.txt

# Install the package dependencies in the requirements file.
# The --no-cache-dir option tells pip to not save the downloaded packages locally
# The --upgrade option tells pip to upgrade the packages if they are already installed.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the ./app directory inside the /code directory.
# it's important to put this near the end of the Dockerfile, 
# to optimize the container image build times (bacause the Docker cache won't
# be used for this or any following steps easily.)
COPY ./app /code/app
COPY ./bootstrap.sh ./import_data.py ./Anki_cards.csv /code/
CMD ["bash", "./bootstrap.sh"]

# The CMD directive specifies the default command to run when starting a container (docker run) from this image.
# Set the command to run the uvicorn server.
# This command will be run from the current working directory,
# the same /code directory you set above with WORKDIR /code.
# Because the program will be started at /code and inside of it is the
# directory ./app with your code, Uvicorn will be able to see and import app from app.main

# Uncomment the below line if you want the webapp to be launched with uvicorn automatically
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]