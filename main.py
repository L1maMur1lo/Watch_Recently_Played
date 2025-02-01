from Database_Scripts.Models import DatabaseModels
from pathlib import Path

import requests
import base64
import os

ROOT_PATH = Path(__file__).parent.__str__()

class RecentlyPlayed:

    def __init__(self):
        self.tokenURL = "https://accounts.spotify.com/api/token"

        self.clientID = os.environ["CLIENT_ID"]
        self.clientSecret = os.environ["CLIENT_SECRET"]
        self.bearerToken = os.environ["BEARER_TOKEN"]
        self.refreshToken = os.environ["REFRESH_TOKEN"]

    def getToken(self):
        auth = (self.clientID + ":" + self.clientSecret).encode("utf-8")
        authB64 = str(base64.b64encode(auth), "utf-8")

        headers = {'Authorization' : 'Basic ' + authB64, 'content-type' : 'application/x-www-form-urlencoded'}
        content = {'grant_type': 'refresh_token', 'refresh_token': self.refreshToken}
        response = requests.post(url=self.tokenURL, headers=headers, data=content)

        if response.status_code == 200:
            response = response.json()
            
            self.bearerToken = response["access_token"]
            print("Token Renovado")
        
        else:
            print(response.status_code)
    
    def execute(self):
        database = DatabaseModels()
        response = requests.get(url="https://api.spotify.com/v1/me/player/recently-played?limit=50", headers={"Authorization": f"Bearer {self.bearerToken}"})

        add_lines = 0
        lines_in_database = 0
        if response.status_code == 200:
            response = response.json()

            for item in response['items']:

                id = item['track']['id']
                title = item ['track']['name'].replace('"', "'")
                artists = ', '.join([artist['name'] for artist in item['track']['artists'] ])
                duration = item['track']['duration_ms']
                albumImgUrl = item['track']['album']['images'][0]['url']
                played_At = item['played_at']
 
                database.addMusic(id=id, title=title, artists=artists, duration=duration, albumImgUrl=albumImgUrl)
                response = database.addExecution(musicId=id, played_At=played_At)

                if response: add_lines += 1
                else: lines_in_database += 1

            print(f"{add_lines:02} Linhas adicionadas ao banco")
            print(f"{lines_in_database:02} Linhas já existentes no banco")
            database.close()

        elif response.status_code == 401:
            self.getToken()

        else:
            raise Exception(f'{response.status_code} - {response.text}')

if __name__ == '__main__':
    recentlyPlayed = RecentlyPlayed()
    recentlyPlayed.getToken()

    recentlyPlayed.execute()