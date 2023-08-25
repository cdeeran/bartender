import sys
import time
import spotipy
from PyQt5.QtCore import QThread, pyqtSignal


class ProgressThread(QThread):
    '''
    Thread dedicated to updating the progress bar
    '''
    count = pyqtSignal(int)

    def __init__(self, waitTime = 0, parent = None) -> None:
        super(ProgressThread, self).__init__(parent)
        self.waitTime = waitTime 

    def run(self):
        count = 0.0
        interval = 100.0/self.waitTime
        while count < 100:
            count += interval
            time.sleep(1)
            self.count.emit(count)

class PourDrinkThread(QThread):
    '''
    Thread dedicated to the pouring the drink
    '''
    gpioStart = pyqtSignal(int)
    gpioFinished = pyqtSignal(int)

    def __init__(self, pin, waitTime = 0, parent = None) -> None:
        super(PourDrinkThread, self).__init__(parent)
        self.pin = pin
        self.waitTime = waitTime

    def run(self):
        self.gpioStart.emit(self.pin)
        time.sleep(self.waitTime)
        self.gpioFinished.emit(self.pin)
        
class SpotifyPlayerThread(QThread):
    '''
    Thread dedicated to polling the current user's spotify playback for the queue

    When a song is updated the emit the signal
    '''
    songChanged = pyqtSignal(str, str, str)

    def __init__(self, spotifyApi:spotipy.Spotify, parent = None) -> None:
        super(SpotifyPlayerThread, self).__init__(parent=parent)
        self.spotifyApi = spotifyApi

    def run(self):
        currentTrack = self.spotifyApi.current_playback()
        prevTrack = None
        while True:
            try:
                if prevTrack != currentTrack['item']['name']:
                    trackName   = currentTrack['item']['name']
                    trackArtist = currentTrack['item']['artists'][0]['name']
                    trackUri    = currentTrack['item']['uri']
                    self.songChanged.emit(trackName,trackArtist, trackUri)
                    prevTrack = currentTrack['item']['name']
            except:
                '''
                Spotify could be running on multiple devices or user switched to a different device
                or Alexa interrupted the playback. All of those could cause for a None return type for current
                track.
                '''
                pass  
            '''
            Spotify will kick us out if we spam the server too many times
            once. So the thread needs to sleep for about 10 seconds every loop.
            This has the potiental to cause some lag in updating the now playing label.
            But it's better than getting kicked out and needing to restart the application to reconnect.
            '''
            time.sleep(10)
            currentTrack = self.spotifyApi.current_playback()