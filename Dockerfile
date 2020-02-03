FROM python:3.8.0-alpine
LABEL maintainer="hamid.poursepanj"

COPY requirements.txt .

RUN pip install --upgrade pip \
    && apk add --no-cache \
        bash \
        curl \
        git \
    && curl -Lo /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.1.3/dumb-init_1.1.3_amd64 \
    && chmod +x /usr/local/bin/dumb-init \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install -e git+https://github.com/hamidp555/web-scraper#egg=scraperapp 

COPY app /tmp/app
COPY entrypoint.sh /sbin/

RUN chmod u+x /sbin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]

CMD ["/sbin/entrypoint.sh"]