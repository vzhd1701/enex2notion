FROM python:3.10.6-slim

# Map host volume here from where you can read the *.enex files
VOLUME data

# Lock version
ENV POETRY_VERSION=1.3.2

# Install poetry build and dependency management system for python
RUN pip3 install "poetry==$POETRY_VERSION"

# Cache the dependencies, they are less volatile.
COPY poetry.lock pyproject.toml /code/

WORKDIR /code

# Disabling creation of virtual environment since docker container is isolated by design.
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy rest of the files (code) which are more likely to change.
COPY . ./

# Setting entry point that cannot be overriden, we will just need to prepend the CLI args when using docker run
ENTRYPOINT [ "poetry", "run", "enex2notion" ]
