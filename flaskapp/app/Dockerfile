FROM python:3.6.8-alpine3.9

LABEL MAINTAINER="Juliette Tworsey"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

ADD . /var/www/
RUN pip install -r requirements.txt
RUN pip install gunicorn

# add a new user & group + initialize the app
# create a new group named www
RUN addgroup -g $GROUP_ID www

# create a www user with a user ID of 1000
# `-s` => create user's home directory if !exist + default login shell => /bin/sh
# `-g` => set user's login group to `www`
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

# programs run in the container will use the www user
USER www

EXPOSE 5000

# start the Gunicorn server with four workers listening on port 5000
CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi"]
