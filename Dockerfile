FROM python:3.14-alpine@sha256:5862d971d1f0ae26b258cefa4e893556b1d3aba81bd2ff30888704ad378bab67
LABEL maintainer="0xflotus"

RUN apk add --virtual build-deps --no-cache gcc musl-dev zlib-dev jpeg-dev
RUN apk add zlib jpeg

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

RUN pytest

ENTRYPOINT ["python", "-m", "hashpic"]