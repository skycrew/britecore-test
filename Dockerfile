FROM ubuntu:18.04
RUN apt-get -qq update && \
    apt-get -qqy install python-pip python-dev mariadb-server libmysqlclient-dev npm && \
    npm install -g sass
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["./run.sh"]
