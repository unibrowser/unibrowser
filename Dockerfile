FROM python:3.6-alpine

# This helps our scraper script know where the python files it needs to run are
ENV APP_HOME /src

# Add our scapers and required configuration
ADD scraping/ /src/scraping/
ADD database/ /src/database/
ADD config/ /src/config/

# Include our cronjob
ADD scrape.sh /etc/periodic/daily/scrape.sh

# Install all of our dependencies
ADD requirements.txt /requirements.txt
ADD setup.py /setup.py
RUN apk add --upgrade \
        python-dev \
        python3-dev \
        libxslt-dev \
        build-base \
        libxml2-dev \
    && pip install -r requirements.txt \
    && python setup.py \
    && apk del \
        build-base \
        python3-dev \
        python-dev \
        libxml2-dev \
        libxslt-dev \
    && rm -rf /var/cache/apk/*

# Start the cron daemon in forground mode to keep the container alive when started
CMD ["crond", "-f"]
