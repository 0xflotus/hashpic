FROM python:3.12-alpine
LABEL maintainer "0xflotus"

RUN apk add --virtual build-deps --no-cache gcc musl-dev zlib-dev jpeg-dev
RUN apk add zlib jpeg

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

RUN pytest

ENTRYPOINT ["python", "-m", "hashpic"]