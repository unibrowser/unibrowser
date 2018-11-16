from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.options import Options
from scraping.faqscraperutil import saveToMongo
from config import SPORTS_CONFIG

PROGRESS = "progress"
DETAILS = "details"
TICKETS = "tickets"
SPORT = "sport"
SPORT_ID = "s_id"

DATE = 'date'
AIRING = "airing"

ALT_TILE = "alt_title"

TEAM_LOGO = "logo_url"
SCORE = "score"
NAME = "name"
NAME_ABBR = "name_abbr"
TIME = "time"
LOCATION = "location"
HOME = "home"
AWAY = "away"


def getMatchDetails(div, data):
    teamDetails = div.find("div", {"class": "team-detail"})
# For Case 3
    if teamDetails is not None:
        teamDetailsTitle = teamDetails.find(
            "div", {"class": "team-detail title"})
        if teamDetailsTitle is not None:
            print("teamDetailsTitle : ", teamDetailsTitle.getText())
            data[ALT_TILE] = teamDetailsTitle.getText()
        else:
            away = {}
            home = {}
            getMatchPlayers(teamDetails, away, home)
            awayScore = teamDetails.find("span", {"class": "detail tl"})
            if awayScore is not None:
                print("awayScore : ", awayScore.getText())
                away[SCORE] = awayScore.getText()
                homeScore = teamDetails.find("span", {"class": "detail tr"})
                print("homeScore : ", homeScore.getText())
                home[SCORE] = homeScore.getText()
            else:
                futureGameTime = teamDetails.find(
                    "span", {"class": "DateTimeDisplay"})
                print("futureGameTime : ", futureGameTime.getText())
                data[TIME] = futureGameTime.getText()  # Future Event no Score
            abbrTitles = div.findAll("span", {"class": "Abbr"})
            awayAbbrTitle = abbrTitles[0].getText()
            away[NAME_ABBR] = awayAbbrTitle
            homeAbbrTitle = abbrTitles[1].getText()
            home[NAME_ABBR] = homeAbbrTitle
            print("awayAbbrTitle : ", awayAbbrTitle,
                  " homeAbbrTitle : ", homeAbbrTitle)
            data[AWAY] = away
            data[HOME] = home


def getMatchPlayers(teamDetails, away, home):
    awayTeamLogo, awayTeamTitle = getLogoDetails(
        teamDetails.find("span", {"class": "ScheduleEventDetail away"}))
    print("awayTeamTitle : ", awayTeamTitle, " awayTeamLogo: ", awayTeamLogo)
    away[TEAM_LOGO] = awayTeamLogo
    away[NAME] = awayTeamTitle
    homeTeamLogo, homeTeamTitle = getLogoDetails(
        teamDetails.find("span", {"class": "ScheduleEventDetail home"}))
    print("homeTeamTitle : ", homeTeamTitle, " homeTeamLogo: ", homeTeamLogo)
    home[TEAM_LOGO] = homeTeamLogo
    home[NAME] = homeTeamTitle


def getMatchMeta(div, data):
    progressSpan = div.find("span", {"class": "progress"})
    if progressSpan is not None:
        data[PROGRESS] = progressSpan.getText()
        print("Progress: ", progressSpan.getText())
    eventDetails = div.find(
        "a", {"class": "Link events-link-details Link-events-link-details"})
    if eventDetails is not None:
        eventDetailsLink = eventDetails['href']
        print("EventDetails: ", eventDetailsLink)
        data[DETAILS] = eventDetailsLink
    eventTickts = div.find(
        "a", {"class": "Link events-link-tickets Link-events-link-tickets"})
    if eventTickts is not None:
        eventTicktsLink = eventTickts['href']
        print("TicketDetails: ", eventTicktsLink)
        data[TICKETS] = eventTicktsLink
    sportName = div.find("span", {"class": "ScheduleEventSportName"})
    print("SportName: ", sportName.getText())
    data[SPORT] = sportName.getText()
    networkNameSpan = div.find("span", {"class": "Network-name"})
    if networkNameSpan is not None:
        print("networkName: ", networkNameSpan.getText())
        data[AIRING] = networkNameSpan.getText()
    address = div.find("div", {"class": "ScheduleEventInfo"})
    print(address.getText())
    data[LOCATION] = address.getText()


def getDivs(link):
    soup = getLink(link)
    class_value = "ScheduleRow-container"
    mydivs = soup.findAll("div", {"class": class_value})
    return mydivs


def getLink(link):
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(link)
    sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    return soup


def getLogoDetails(span):
    logo = span.find("img", {"class": "Logo"})
    return logo['src'], logo['title']


def readSportsList():
    with open(SPORTS_CONFIG['links'], 'r') as myfile:
        sports = myfile.read().split('\n')
        return sports


sportsLinks = readSportsList()

jsonList = []
for i in range(0, len(sportsLinks)):
    link = sportsLinks[i]
    divs = getDivs(link)
    print(len(divs))
    for div in divs:
        dt = div.find("span", {"class": "DateTimeDisplay"})
        if dt is None:
            continue
        print("Date: ", dt.getText())
        data = {}
        data[SPORT_ID] = i
        data[DATE] = dt.getText()

        getMatchMeta(div, data)

        getMatchDetails(div, data)
        jsonList.append(data)
        print("\n")
        print(data)
        print("\n\n")

saveToMongo(jsonList, SPORT)
