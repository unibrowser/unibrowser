import urllib.request
import sys
import re
import json
import datetime
from bson import json_util
from bson.json_util import loads

sys.path.append('../')
from api.school import School, insert
from api.sportevents import Team, SportEvent, ComplexHandler, insert_many
from sportscraperutils import loadJsonFromUrl, getSchool, cleanSportsIdArray, getEventsQueryLink, getListFromJsonArrayWIthKey, getSchoolPOPO

schoolsLink = "https://api.pac-12.com/v3/schools"
networksQuery = "https://api.pac-12.com/v3/networks/"
sportsInfoLink = "http://api.pac-12.com/v2/sports"
# eventsQuery = "https://api.pac-12.com/v3/events?pagesize=100&sports=26&start=2018-08-01T00%3A00%3A00-07%3A00&end=2019-07-31T23%3A59%3A59-07%3A00&school=18"


def getLinksToSports(school):
    sportsInfoJson = loadJsonFromUrl(sportsInfoLink)
    schoolId = school["id"]
    # print(school["sports"])
    # print(sportsInfoJson)
    sportsIdListString = getListFromJsonArrayWIthKey("id", school["sports"])
    sportsIdList = [ int(x) for x in sportsIdListString ]
    
    sportsNameList, sportTitleList = cleanSportsIdArray(sportsIdList, sportsInfoJson)
    # for i in range(len(sportsIdList)):
    #     print("ID : ", sportsIdList[i], " Name : ", sportsNameList[i], " Title : ", sportTitleList[i])
    sportsLinkList = []
    for id in sportsIdList:
        link = "https://api.pac-12.com/v3/events?pagesize=100&sports=" + str(id) + "&start=2018-08-01T00%3A00%3A00-07%3A00&end=2019-07-31T23%3A59%3A59-07%3A00&school=" + str(schoolId)
        sportsLinkList.append(link)
    return sportsNameList, sportsLinkList, sportsIdList, sportTitleList


def getTeamsInfo(teams, jsonSchools):
    if teams[0]["home_team"]:
        homeTeamId = teams[0]["id"]
        awayTeamId = teams[1]["id"]
    else:
        awayTeamId = teams[0]["id"]
        homeTeamId = teams[1]["id"]
    home = {}
    away = {}
    for school in jsonSchools["schools"]:
        if school["id"] == homeTeamId:
            home["name"] = school["abbr"]
            home["logo_url"] = school["images"]["tiny"]

        if school["id"] == awayTeamId:
            away["name"] = school["abbr"]
            away["logo_url"] = school["images"]["tiny"]

        if home.get("name", None) is not None and away.get("name", None) is not None:
            break



    return home, away

def getAddress(venueJson):
    address = None
    if venueJson.get("name", None) is not None:
        if address is None:
            address = ""
        address += venueJson["name"] + ", "
    if venueJson.get("address_1", None) is not None:
        if address is None:
            address = ""
        address += venueJson["address_1"] + ", "
    if venueJson.get("city", None) is not None:
        if address is None:
            address = ""
        address += venueJson["city"] + ", "
    if venueJson.get("state", None) is not None:
        if address is None:
            address = ""
        address += venueJson["state"]
    return address


def checkForScore(sportEventsJson, home, away, id):
    for event in sportEventsJson["data"]:
        if event["_id"] == id:
            if event.get("awayScore", None) is not None:
                home["score"] = event["homeScore"]
                away["score"] = event["awayScore"]
            return
            

def saveSportsEventsForSport(sportEventsJson, sportPageJson, jsonSchools, sport_tags, sportsName):
    sportEventList = []
    for event in sportPageJson:
        sportEvent = {}
        # sportEvent = SportEvent()
        sportEvent["event_id"] = event["id"]
        sportEvent["sport"] = sportsName
        # sportEvent["sport_tags"] = sport_tags
        sportEvent["details"] = event["url"]
        sportEvent["sport_id"] = event["sport_id"]

        eventDate = event["event_date"]["start_time"]     
        dateFormatted = datetime.datetime.strptime(eventDate, '%Y-%m-%dT%H:%M:%SZ')
        sportEvent["date"] = dateFormatted
        sportEvent["location"] = getAddress(event["venue"])
        if event.get("link", None) is not None and event["link"].get("url", None) is not None:
            sportEvent["tickets"] = event["link"]["url"]
        # print(sportEvent.__dict__)
        teams = event.get("schools", None)

        if event.get("event_name", None) is not None:
            sportEvent["alt_title"] = event["event_name"] 
        else:
            if teams is not None and len(teams) > 1:
                home, away = getTeamsInfo(teams, jsonSchools)
                checkForScore(sportEventsJson, home, away, event["id"])
                sportEvent["away"] = away
                sportEvent["home"] = home

        sportEventList.append(sportEvent)
    
    insert_many(loads(json.dumps(sportEventList, default=json_util.default)))

    
def startSportsScrapper(collegeName):
    school = getSchool(collegeName, -1, jsonSchools)
    sportsNameList, sportsLinkLists, sportIdList, sportTitleList = getLinksToSports(school)
    print(len(sportsLinkLists), " ", len(sportIdList), " ", len(sportsNameList))
    #Iterate Through Xports
    # print("len : ", len(sportsLinkLists))
    for i in range(len(sportsLinkLists) - 1, -1, -1):
        link = sportsLinkLists[i]
        sportPageJson = loadJsonFromUrl(link)
        # print(sportPageJson)
        eventIdsList = getListFromJsonArrayWIthKey("id", sportPageJson["events"])
        if len(eventIdsList) > 0:
            eventsApiLink = getEventsQueryLink(eventIdsList)
            # print(eventsApiLink)
            sportEventsJson = loadJsonFromUrl(eventsApiLink)
            # print(sportEventsJson)
            sportName = sportsNameList[i]
            sportTitle = sportTitleList[i]
            sport_tags = re.sub(r'[^\w\s]', '', sportTitle).split(" ")
            # print(sportName)
            # print(link)
    
            saveSportsEventsForSport(sportEventsJson, sportPageJson["events"], jsonSchools, sport_tags, sportName)
            # break
        else:
            # print("Remove : ", len(sportsLinkLists), " i : ", i)
            del sportsNameList[i]
            del sportIdList[i]
            del sportTitleList[i]

    # print(school)
    mainSchoolPOPO = getSchoolPOPO(school, sportsNameList, sportIdList)
    insert(mainSchoolPOPO)

# def generateSportsData(collegeName):
    # jsonSchools = loadJsonFromUrl(schoolsLink)
    # startSportsScrapper(collegeName)

if __name__ == '__main__':
    jsonSchools = loadJsonFromUrl(schoolsLink)
    startSportsScrapper("Oregon State")
