# Run as non-root user

- `default` => Docker containers run as the `root user` w/access to everything in the system => a security breach can be disastrous

    - Solution:

      - create a `new user` and `group` that will only have access to the ``/var/www` directory


  ` RUN addgroup -g $GROUP_ID www
    RUN adduser -D -u $USER_ID -G www www -s /bin/sh

    USER www `

    
