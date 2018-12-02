#!/bin/sh
# This file is meant to be run from inside a docker container based on the Alpine Linux image. The location of the 
# scraping script files is '/src'
#cd /src
echo "Running"
#log=/var/scrape.log
python scraping/faqscraper.py #>> $log
python scraping/profinfoscraping.py #>> $log
python scraping/tweetextractor.py #>> $log
python scraping/sportscraper_new.py #>> $log
python scraping/events.py #>> $log
python scraping/bus_info.py #>> $log
