FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

RUN apt-get update \
    && apt-get -y install --no-install-recommends bundler

COPY ./startup.sh /tmp/scripts/startup.sh
COPY ./.bash_aliases /tmp/scripts/.bash_aliases
RUN apt-get update && bash /tmp/scripts/startup.sh