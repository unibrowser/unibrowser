#!/bin/sh
# This file is meant to be run from inside a docker container based on the Alpine Linux image. The location of the 
# scraping script files is '/src'
cd /src
echo "Running"
log=/var/scrape.log
python scraping/faqscraper.py >> $log
python scraping/profinfoscraping.py >> $log
python scraping/tweetexractor.py >> $log
