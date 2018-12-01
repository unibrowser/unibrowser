import urllib.request
import json
import sys
# sys.path.append('../')
from api.school import School


def loadJsonFromUrl(url):
    contents = urllib.request.urlopen(url).read()
    jsonData = json.loads(contents)
    return jsonData


def getListFromJsonArrayWIthKey(key, jsonArray):
    listObject = []
    for j in jsonArray:
        if j[key] is not None:
            listObject.append(j[key])
    return listObject 


def getSchool(collegeName, id, jsonSchools):
    for school in jsonSchools["schools"]:
        if (collegeName is not None and school["name"].lower() == collegeName.lower()) or (id is not -1 and int(school["id"]) == id):
            # print("Found college : ", school)
            return school


def cleanSportsIdArray(sportIdList, sportsInfoJson):
    sportsNameList = []
    sportsTitleList = []
    for i in range(len(sportIdList) - 1, -1, -1):
        sportId = sportIdList[i]
        sportName = None
        for sport in sportsInfoJson["sports"]:
            if sport["id"] == sportId:
                if sport["is_visible"] == True:
                    sportName = sport["menu_label"]
                    sportTitle = sport["name"]
        if sportName is not None:
            sportsNameList.append(sportName)
            sportsTitleList.append(sportTitle)
        else:
            del sportIdList[i]
    
    return sportsNameList[::-1], sportsTitleList[::-1]


def getEventsQueryLink(eventsIdsLis):
    eventsApiLink = "https://api.pac-12.com/v3/events/"
    link = eventsApiLink + ";".join(eventsIdsLis)
    link = link + "/context"
    return link

    
def getSchoolPOPO(school, sportsNameList, sportsIdList):
    sch = School(school["id"], school["name"], school["abbr"], school["images"]["tiny"], sportsNameList, sportsIdList)
    return sch