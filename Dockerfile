FROM python:3.9-alpine
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN apk add --virtual build-deps --no-cache gcc python3-dev musl-dev zlib-dev jpeg-dev
RUN apk add zlib jpeg
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade argparse
RUN python3 -m pip install --upgrade Pillow 
ENTRYPOINT ["python", "-m", "hashpic"]