# How To Set Up Flask with MongoDB and Docker

https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker

## NOTES:

- build, package, and run to-do web app w/ Flask, Nginx, and MongoDB inside of Docker containers

- Flask requires a web server to serve HTTP requests => use Gunicorn => a Python WSGI HTTP Server => serve the app 

- Nginx => reverse proxy server => forwards requests to Gunicorn for processing

## Step 1 — Writing the Stack Configuration in Docker Compose

 ` touch docker-compose.yml `

- NOTE:

	-  Volumes are stored in a part of the host filesystem managed by Docker (/var/lib/docker/volumes/ on Linux)

- using the `unless-stopped` property in compose.yml file => containers will start automatically once the Docker Engine is restarted or any error occurs

- the `volume appdata` is mounted inside the container at the `/var/www` directory

- `depends_on` => only run Flask service if the mongodb service is running

- `networks` => specifies frontend and backend as the networks the flask service will have access to

- `mongod --auth` => disables logging into the MongoDB shell without credentials

- env vars `MONGO_INITDB_ROOT_USERNAME` and `MONGO_INITDB_ROOT_PASSWORD` create a root user w/ the given credentials => replace the placeholder with a strong password

- `MongoDB` stores data in `/data/db` => data in the /data/db folder will be written to the named volume `mongodbdata` for persistence

- `nginx`:

  - defined the context of the build, which is the nginx folder containing the Dockerfile

- `Nginx Dockerfile` => `alpine` base image => a tiny Linux distribution with a `minimal attack surface built for security`

- NOTE:

  - `Publishing errors to standard error and output is a best practice` since `containers are ephemeral`, doing this the logs are shipped to docker logs and from there you can forward your logs to a logging service like the Elastic stack for persistance


## Step 2 — Writing the Flask and Web Server Dockerfiles

  ` mkdir app `

  ` vim app/Dockerfile `

  - creating an image on top of the `3.6.8-alpine3.9` image => based on Alpine 3.9 w/ Python 3.6.8 pre-installed

  - `ENV` directive => defines the environment variables for our group and user ID

      - `Linux Standard Base (LSB)` => http://refspecs.linux-foundation.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/usernames.html => specifies that:
      
      
          -  `UIDs and GIDs 0-99` are `statically allocated` by the system. UIDs 100-999 are supposed to be allocated dynamically for system users and groups
          
          - `UIDs 1000-59999` are supposed to be `dynamically allocated for user accounts` => can safely assign a UID and GID of 1000 + can change the UID/GID by updating the GROUP_ID and USER_ID to match your requirements

# Step 3 — Configuring the Nginx Reverse Proxy

  - configure Nginx as a reverse proxy to `forward requests to Gunicorn on :5000` => direct client requests to the appropriate back-end server

    ` mkdir nginx/conf.d ` 

    ` vim nginx/conf.d/app.conf `

    - `upstream server` => specify a web or app server for routing or load balancing

        -  upstream server, `app_server`, defines the `server address` w/ the server directive => identified by the container name `flask:5000`

    - config for the Nginx web server is defined in the `server block` => `proxy_pass` directive => set the upstream server for `forwarding the requests to http://app_server`


## Step 4 — Creating the Flask To-do API


- write a to-do API application that will save and display to-do notes sent in from a POST request

  ` vim app/requirements.txt `

  ` vim app/app.py `

  ` vim app/wsgi.py `

      - for each request => the server uses this app object to `run the app’s request handlers upon parsing the URL`

      - imports app object from app.py + creates an `app object for the Gunicorn server`


# Step 5 — Building and Running the Containers

 ` docker-compose up -d `

 ` docker ps `


## Step 6 — Creating a User for Your MongoDB Database


- `secure DB` => create a dedicated user w/ access to DB

- ie.,.. configure a dedicated DB + user account for Flask app

    - need `root username + password` set in docker-compose.yml

        - ie., `MONGO_INITDB_ROOT_USERNAME` + `MONGO_INITDB_ROOT_PASSWORD`

    - `avoid using root user`:

        - create new DB user for Flask app + new DB that allows Flask app access to that particular DB


    ` docker exec -it 9eb90bfb bash `//or current container ID

    - Once inside container, `log in to the MongoDB root administrative account`:

      ` mongo -u mongodbuser -p `//enter password from yml

      ` show dbs `

      ` use flaskdb `

      ` db.createUser({user: 'flaskuser', pwd: 'your_mongodb_password', roles: [{role: 'readWrite', db: 'flaskdb'}]}) `//user and pwd => values defined in docker-compose.yml under `env variables section for the flask service` => change password later...

    - Log in to the authenticated DB:

      ` mongo -u flaskuser -p your_mongodb_password --authenticationDatabase flaskdb `

    - exit Mongo

      ` exit `

    - exit container

      ` exit `


## Step 7 — Running the Flask To-do App


  ` http://your_server_ip `


- get server ip:

  ` docker inspect <container_id> `

- see the JSON response from Flask:

  ` curl -i http://your_server_ip `

  - or just ` curl -i http://localhost:80 `

- test POST:

  ` curl -i -H "Content-Type: application/json" -X POST -d '{"todo": "Dockerize Flask application with MongoDB backend"}' http://your_server_ip/todo `

  ...ie.,...

  ` curl -i -H "Content-Type: application/json" -X POST -d '{"todo": "Dockerize Flask application with MongoDB backend"}' http://localhost:80/todo `

- GET todos:

  ` curl -i http://your_server_ip/todo `

  ..ie.,...

  ` curl -i http://localhost:80/todo `


- now have a Dockerized Flask API running a MongoDB backend w/ Nginx as a reverse proxy deployed to your servers

- NOTE:

    - for a `prod environment` => use `sudo systemctl enable docker` => ensures Docker service automatically starts at runtime


## Conclusion

- Created a stateless API application that can be scaled
