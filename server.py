import requests
import json
import cherrypy
import base64
import time

#app auth
clientID="CLIENT_ID"
clientSecret="CLIENT_SEC"
red_uri="http://127.0.0.1/callback"
scope="user-modify-playback-state"

#query html for initial auth
start_auth=f"<html><body><a href=https://accounts.spotify.com/authorize?client_id={clientID}&response_type=code&redirect_uri={red_uri}&scope={scope}>auth</a></body></html>"

#for Auth in header
auth_bytes=f"{clientID}:{clientSecret}".encode("ascii")
auth_base64=base64.urlsafe_b64encode(auth_bytes).decode()


class spotify_auth(object):
    favicon_ico=None

    #client auth
    @cherrypy.expose
    def auth(self):
        return start_auth
        
    @cherrypy.expose
    def callback(self, error=None, code=None, state=None):
        #now getting acces token and refresh token
        query="https://accounts.spotify.com/api/token"

        body={
            "grant_type":"authorization_code",
            "code":code,
            "redirect_uri":red_uri,
        }

        header={"Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {auth_base64}",
                }

        access_res=requests.post(query, params=body, headers=header)
        print(access_res)
        res_json=access_res.json()

        #saving access and refresh token in local json file
        creds_dict={
            "access_token":res_json["access_token"],
            "refresh_token":res_json["refresh_token"],
            "valid_until":time.time()+3596.0,
        }
        #having a four second buffer

        with open("user_creds.json", "w") as creds:
            json.dump(creds_dict, creds)

        #auth completed
        return "auth-process completed"

    def refresh(self):
        #selfexplanatory
        with open("user_creds.json") as creds:
            old_creds=json.load(creds)

        query="https://accounts.spotify.com/api/token"

        body={
            "grant_type":"refresh_token",
            "refresh_token":old_creds["refresh_token"]
        }
        header={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth_base64}"
            }

        refresh_res=requests.post(query, headers=header, params=body)
        refresh_json=refresh_res.json()

        creds_dict={
            "access_token":refresh_json["access_token"],
            "refresh_token":old_creds["refresh_token"],
            "valid_until":time.time()+3596.0,
        }

        with open("user_creds.json", "w") as creds:
            json.dump(creds_dict, creds)
        
        print("refreshed Token")
        return "refreshed"
    
    def getToken(self):
        #check if accessToken is still valid
        with open("user_creds.json") as creds:
            creds_json=json.load(creds)
            access_token=creds_json["access_token"]
            valid_until=creds_json["valid_until"]
        #if not valid
        if not float(valid_until) > (time.time()+3):
            self.refresh()
            time.sleep(10)
            with open("user_creds.json") as creds:
                creds_json=json.load(creds)
                access_token=creds_json["access_token"]
        
        return str(access_token)

    @cherrypy.expose
    def addtoqueue(self, track=None):
        access_token=self.getToken()
        header={"Authorization": f"Bearer {str(access_token)}"}
        query="https://api.spotify.com/v1/me/player/queue?uri=spotify:track:"+str(track)
        r=requests.post(query, headers=header)
        print(f"added {track}")
        return "song added"

    @cherrypy.expose
    def nexttrack(self):
        access_token=self.getToken()
        header={"Authorization": f"Bearer {str(access_token)}"}
        query="https://api.spotify.com/v1/me/player/next"
        r=requests.post(query, headers=header)
        print("switched to next track")
        return "switched to next track"
        
    @cherrypy.expose
    def pause(self):
        access_token=self.getToken()
        header={"Authorization": f"Bearer {str(access_token)}"}
        query="https://api.spotify.com/v1/me/player/pause"
        r=requests.put(query, headers=header)
        print("paused playback")
        return "paused playback"

    @cherrypy.expose
    def play(self):
        access_token=self.getToken()
        header={"Authorization": f"Bearer {str(access_token)}"}
        query="https://api.spotify.com/v1/me/player/play"
        r=requests.put(query, headers=header)
        print("playback started")
        return "playback started"


if __name__ == "__main__":
    cherrypy.server.socket_host="127.0.0.1"
    cherrypy.server.socket_port=80
    cherrypy.quickstart(spotify_auth())