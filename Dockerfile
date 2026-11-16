FROM python:3.15-alpine@sha256:0f9552bb28711333da16915ec146f5e6bb44a7fdac9ced15dc17c2e0206346dd
COPY --from=ghcr.io/astral-sh/uv:0.13.8 /uv /uvx /bin/
LABEL maintainer="0xflotus"

RUN apk add --virtual build-deps --no-cache gcc musl-dev zlib-dev jpeg-dev
RUN apk add zlib jpeg

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --extra test --no-install-project
COPY . .
RUN uv sync --locked --extra test

RUN uv run pytest

ENTRYPOINT ["uv", "run", "--no-sync", "python", "-m", "hashpic"]