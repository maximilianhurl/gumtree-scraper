FROM python:3.6

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y curl git libpq-dev

# Set the working directory to /app
RUN mkdir /opt/app
WORKDIR /opt/app

# Copy the current directory contents into the container at /app
ADD . /opt/app

RUN python3 -m venv env && env/bin/pip install -r requirements.txt

ENV PYTHONPATH=/opt/app/
ENV AIRFLOW_HOME=/opt/app/

EXPOSE 8080

ENTRYPOINT ["/bin/bash", "-c"]