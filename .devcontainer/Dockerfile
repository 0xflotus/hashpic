FROM mcr.microsoft.com/devcontainers/python:3.15-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.13.8 /uv /uvx /usr/local/bin/

ENV UV_LINK_MODE=copy
