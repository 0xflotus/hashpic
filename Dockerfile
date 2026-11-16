FROM python:3.15-alpine@sha256:0f9552bb28711333da16915ec146f5e6bb44a7fdac9ced15dc17c2e0206346dd
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