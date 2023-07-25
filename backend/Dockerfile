# start by pulling the python image
FROM python:3.8-alpine

# install build dependencies for mysqlclient
RUN apk add --no-cache mariadb-connector-c-dev build-base



# install dependencies for the Rust compiler
RUN apk add --no-cache rust cargo

# Install the MySQL client library
RUN apk add --no-cache mariadb-connector-c

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

COPY ./db/create_db.sql /app/create_db.sql
COPY ./db/password.txt /app/password.txt

# switch working directory
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# Install the Flask CLI
RUN pip install Flask

#RUN python create_db.py

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port on which the Flask app will run
EXPOSE 5000

CMD ["-m", "flask", "run"]