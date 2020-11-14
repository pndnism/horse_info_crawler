FROM python:3.8.1

# Set timezone to JST
ENV TZ Asia/Tokyo

# Install packages
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    locales && \
    locale-gen ja_JP.UTF-8 && \
    echo "export LANG=ja_JP.UTF-8" >> ~/.bashrc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set Language
ENV LANG ja_JP.UTF-8

ENV APP_ROOT /var/app/
WORKDIR $APP_ROOT

RUN pip install --upgrade pip && pip install pipenv

COPY Pipfile $APP_ROOT
COPY Pipfile.lock $APP_ROOT

RUN pipenv sync --dev

COPY . $APP_ROOT