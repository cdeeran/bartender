import json
import os
from typing import Any
import spotipy
from spotipy.oauth2 import SpotifyOAuth

try:
  CLIENT_ID           = os.environ["SPOTIPY_CLIENT_ID"]
  CLIENT_SECRET       = os.environ["SPOTIPY_CLIENT_SECRET"]
  CLIENT_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]
except Exception as e:
  print("An Environment Variable for Spotify is incorrrect. Please verify you have the follow correct:\n")
  print("CLIENT_ID\nCLIENT_SECRET\nREDIRECT_URI\n")

redirect = "http://localhost:3000"
class Spotify:
  def __init__(self, deviceName:str, nospotify):
    self._scope       = "user-read-playback-state,user-modify-playback-state"
    if not nospotify:
      self._credentials = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=redirect, scope=self._scope, open_browser=True)
      self.spotify      = spotipy.Spotify(client_credentials_manager=self._credentials)
    else:
      self._credentials = None
      self.spotify      = None
    self._deviceName  = deviceName
    self._deviceId    = -1 if nospotify else self.establishConnection()
    self._recentQuery = {}
    self._queue       = set()

  def _findDeviceId(self) -> Any:
    id = -1
    devices = self.getDevices()
    for device in devices["devices"]:
      if device['name'] == self.getDeviceName():
        id = device['id']
    return id

  def _setDeviceId(self, id) -> None:
    self._deviceId = id
    return None

  def _addToLocalQueue(self, id) -> None:
    knownQuery = self.getRecentQuery()
    self._queue.add(knownQuery[id])
    return None

  def checkAndRemoveFromQueue(self, uri) -> None:
    for item in self._queue:
      if item[2] == uri:
        self._queue.remove(item)
        break
    return None

  def getCurrentPlayback(self):
    return self.spotify.currently_playing()

  def establishConnection(self, maxAttempts=3) -> None:
    currentRetries = 1
    deviceId = self._findDeviceId()

    while deviceId == -1 and currentRetries <= maxAttempts:
        print("Attempting to establish spotify device connection...")
        print(f"Retries remaining: {(maxAttempts - currentRetries)}")   
        deviceId = self._findDeviceId

    if deviceId != -1:
      self._setDeviceId(deviceId)
      print(f"Established connection to device id: {self.getDeviceId()}")
    else:
      print(f"Error! Could not establish connection to device named: {self.getDeviceName()}")

    return None

  def getDevices(self) -> json:
    return self.spotify.devices()

  def getDeviceId(self) -> Any:
    return self._deviceId

  def getDeviceName(self) -> str:
    return self._deviceName

  def getRecentQuery(self) -> dict:
    return self._recentQuery

  def getQueue(self) -> set:
    return self._queue

  def setRecentQuery(self, results:dict) -> None:
    self._recentQuery = results
    return None

  def printSearchResults(self, results:dict) -> None:
      for key, value in results.items():
          print(f"    ID: {key}")
          print(f" TRACK: {value[0]}")
          print(f"ARTIST: {value[1]}")
          print(f"   URI: {value[2]}")
          print()
      return None

  def search(self, query) -> None:
      formattedResults = {}
      results = self.spotify.search(q=query)
      id = 1
      for item in results['tracks']['items']:
        for artist in item['artists']:
          formattedResults[id] = (item['name'], artist['name'], item['uri'])
          id += 1
      self.setRecentQuery(formattedResults)
      return None

  def play(self) -> None:
      self.spotify.start_playback(device_id=self.getDeviceId())
      return None
  
  def pause(self) -> None:
      self.spotify.pause_playback(device_id=self.getDeviceId())
      return None

  def next(self) -> None:
      self.spotify.next_track(device_id=self.getDeviceId())
      return None
    
  def previous(self) -> None:
      self.spotify.previous_track(device_id=self.getDeviceId())
      return None

  def requestTrack(self, id) -> None:
    uri = self.getTrackUri(id, self.getRecentQuery())
    if self.spotify.current_playback():
      self.spotify.add_to_queue(uri=uri, device_id=self.getDeviceId())
    else:
      self.spotify.start_playback(uris=[uri], device_id=self.getDeviceId())
    self._addToLocalQueue(id)
    return None

  def getTrackUri(self, trackId, recentQuery:dict) -> Any:
    return recentQuery[trackId][2] #uri position in tuple