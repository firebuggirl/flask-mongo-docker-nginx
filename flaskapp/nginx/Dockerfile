#FROM digitalocean.com/alpine:latest
FROM alpine:3.10.3

LABEL MAINTAINER="Juliette Tworsey"


# install nginx + publish the error and access logs to the standard error (/dev/stderr) and output (/dev/stdout)
# remove tdefault.conf & /var/cache/apk/* to reduce the size of the image
# one connected run command => smaller image + fewer layers
RUN apk --update add nginx && \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log && \
    mkdir /etc/nginx/sites-enabled/ && \
    mkdir -p /run/nginx && \
    rm -rf /etc/nginx/conf.d/default.conf && \
    rm -rf /var/cache/apk/*

COPY conf.d/app.conf /etc/nginx/conf.d/app.conf

# run app on :80 w/ :443 as the secure port
EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
