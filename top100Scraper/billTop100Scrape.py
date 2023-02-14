from bs4 import BeautifulSoup
import requests
import re
import openpyxl
import json
import datetime
from scrapeID import spotifyID, spotifyToken

def __init__(self):
    self.spotifyID = spotifyID
    self.spotifyToken = spotifyToken

def scrape(self):
    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = 'Billboard Top 100'
    sheet.append(['Rank','Song','Artist'])

    try:
        source = requests.get("https://www.billboard.com/charts/hot-100/")
        source.raise_for_status()
        mySoup = BeautifulSoup(source.text, 'html.parser')
        songs = mySoup.find('div', class_="chart-results-list // lrv-u-padding-t-150 lrv-u-padding-t-050@mobile-max").find_all(class_=re.compile("o-chart-results-list-row-container"))
        songRank = 1
        for song in songs:
            songName = song.find('h3', "c-title").get_text(strip=True)
            songArtist = song.find('span',class_=re.compile("c-label a-no-trucate")).get_text(strip=True)        
            sheet.append([songRank, songName, songArtist])
            songRank = songRank + 1

        
    except Exception as e:
        print("The link is not valid!")
    excel.save("Billboard Top 100.xlsx")

def makePlaylist(self):
            currentTime = datetime.datetime.now()
            request_body = json.dumps({
            "name": "Billboard Top 100: {}, {}".format(currentTime.month, currentTime.year),
            "description": "The Billboard Top 100 for the specified time range!",
            "public": True})

            query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotifyID)
            response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotifyToken)
            }
            )
            response_json = response.json()
            return response_json["id"]

def getSongs(self, songName, artist):
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            songName,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotifyToken)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        # only use the first song
        uri = songs[0]["uri"]

        return uri