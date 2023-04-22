# pull official base image
FROM python:3.11.2-slim-buster

# set working directory
WORKDIR /src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# new
# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc  \
  && apt-get clean

# add and install requirements
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# add app
COPY . .

# new
# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x entrypoint.sh
