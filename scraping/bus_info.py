# Sets the execution path
import sys
import os
import json
from datetime import datetime
from database.mongoclientclass import MongoClientClass
from scraping.scrape_utils import get_html
from config import BUS_CONFIG


WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
WEEKENDS = ['Saturday']
HOLIDAYS = ['Sunday']

LAT = 'lat'
LONG = 'long'
IMAGE = 'image'
DESC = 'desc'
ADDRESS = 'address'


def scrape_row_data(soup, cur_bus_name, location_info, lat_lng_config):
    route_tables = soup.select('table')
    lat_lngs = []
    headers = route_tables[0].select('thead tr th')
    for header in headers:
        lat_lng_name = header.getText().strip()
        if lat_lng_name in lat_lng_config:
            lat_lng = lat_lng_config[lat_lng_name]
        else:
            lat_lng = lat_lng_name
        lat_lngs.append(lat_lng)
        if lat_lng not in location_info:
            location_info[lat_lng] = {}
        for week_day in WEEK_DAYS:
            if week_day not in location_info[lat_lng]:
                location_info[lat_lng][week_day] = {}
            location_info[lat_lng][week_day][cur_bus_name] = []
    # print(lat_lngs)
    time_data_list = route_tables[0].select('tbody tr')
    for time_data in time_data_list:
        times = time_data.select('td')
        for i in range(len(lat_lngs)):
            for week_day in WEEK_DAYS:
                try:
                    # print(i, lat_lngs[i], week_day, cur_location_info[lat_lngs[i]])
                    cur_time = times[i].getText().strip()
                    if times[i].select('strong'):
                        cur_time = cur_time + ' PM'
                    else:
                        cur_time = cur_time + ' AM'
                    cur_time = datetime.strptime(cur_time, '%I:%M %p')
                    location_info[lat_lngs[i]][week_day][cur_bus_name].append(
                        cur_time.strftime('%H:%M'))
                except Exception as e:
                    print("Unable to parse time:", cur_time)


def save_loc_data(locations):
    try:
        mongo_client_instance = MongoClientClass()
        mongo_client_instance.insert(
            collection=BUS_CONFIG['db_collection'], documents=locations)
    except Exception as e:
        print(e)
        # print("inside save_prof_data: 0 (exception)")
        return 0
    # print("inside save_prof_data: 1 (success)")
    return 1


if __name__ == '__main__':
    bus_config = BUS_CONFIG['config_file']
    lat_lng = BUS_CONFIG['lat_lng_info_file']
    with open(bus_config, 'r') as f:
        json_config = json.load(f)
    with open(lat_lng, 'r') as f:
        lat_lng_config = json.load(f)

    location_info = {}
    for bus_name, bus_url in json_config['bus_information'].items():
        cur_soup = get_html(bus_url)
        scrape_row_data(cur_soup, bus_name, location_info, lat_lng_config)
    loc_info = []
    for loc_lat_lng, details in location_info.items():
        loc_info.append({
            'lat_lng': loc_lat_lng,
            'details': details
        })
    print(json.dumps(loc_info, indent=4))
    save_loc_data(loc_info)
