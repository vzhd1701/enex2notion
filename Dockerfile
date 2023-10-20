FROM debian:12-slim AS build

ENV BUILD_POETRY_VERSION=1.6.1

RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv python3-pip && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip

RUN pip3 install --break-system-packages poetry==$BUILD_POETRY_VERSION

FROM build AS build-venv

COPY . /app
WORKDIR /app

RUN poetry build --no-interaction -f wheel
RUN /venv/bin/pip install --disable-pip-version-check dist/*.whl

FROM gcr.io/distroless/python3-debian12

ENV INSIDE_DOCKER_CONTAINER=1

LABEL   maintainer="vzhd1701 <vzhd1701@gmail.com>" \
        org.opencontainers.image.title="enex2notion" \
        org.opencontainers.image.description="Import Evernote ENEX files to Notion " \
        org.opencontainers.image.authors="vzhd1701 <vzhd1701@gmail.com>" \
        org.opencontainers.image.licenses="MIT" \
        org.opencontainers.image.documentation="https://github.com/vzhd1701/enex2notion" \
        org.opencontainers.image.url="https://github.com/vzhd1701/enex2notion" \
        org.opencontainers.image.source="https://github.com/vzhd1701/enex2notion.git"

COPY --from=build-venv /venv /venv

WORKDIR /input

ENTRYPOINT ["/venv/bin/enex2notion"]
