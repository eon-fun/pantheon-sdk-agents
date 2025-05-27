ARG BASE_IMAGE=python:3.12-bookworm

####### Build Stage ###########
FROM ${BASE_IMAGE} as builder

USER root

RUN pip install poetry poetry-plugin-export && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* /build/
WORKDIR /build

RUN poetry export -f requirements.txt --without-hashes --output requirements.txt

####### Final Stage ###########
FROM ${BASE_IMAGE}

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

ARG PIP_EXTRA_INDEX_URL
ENV PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL}

COPY --from=builder /build/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt && rm ./requirements.txt

ENV PIP_EXTRA_INDEX_URL=

COPY . /relay-service
WORKDIR /relay-service
ENV PYTHONPATH=/relay-service/src

COPY start.sh /relay-service/start.sh
RUN chmod +x /relay-service/start.sh

ENTRYPOINT [ "/relay-service/start.sh" ]
