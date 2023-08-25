'''
This class handles all the functionality from the SpotifyUi.py file
'''
import os
import pprint
from PyQt5 import QtWidgets, QtGui
from ui.output_files.spotifyUi import Ui_SpotifyWidget
from bartender.spotify import Spotify
from bartender.thread_manager import SpotifyPlayerThread
from utils import constants

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
class SpotifyWidget(QtWidgets.QWidget):

    def __init__(self, nospotify) -> None:
        super().__init__()
        self.view = Ui_SpotifyWidget()
        self.view.setupUi(self)
        self.spotifyPlayer = Spotify("Everywhere", nospotify)
        if not nospotify:
            self.spotifyQueueThread = SpotifyPlayerThread(self.spotifyPlayer.spotify)
            self.spotifyQueueThread.songChanged.connect(self.updateCurrentPlayback)
        self.setupDjBooth()
        return None

    def setupDjBooth(self) -> None:
        '''
        Setup the DJ Booth aka Spotify Player
        '''
        if self.spotifyPlayer.getDeviceId() != -1:
            self.view.currentlyPlayingLabel.setText("None")
            self.view.spotifySearchButton.clicked.connect(self.searchSpotify)
            self.view.spotifySearchResultsField.itemDoubleClicked.connect(self.selectedSearch)
            self.view.spotifyPlayPauseButton.clicked.connect(self.playPauseButtonClicked)
            self.view.spotifyNextButton.clicked.connect(self.nextTrack)
            self.view.spotifyPreviousButton.clicked.connect(self.previousTrack)
            self.view.spotifyTabWidget.setStyleSheet(constants.SPOTIFY_TAB_STYLE)
            self.localPlaybackState = False

            '''
            Get the initial playback status from spotify to show the correct state of the play/pause button
            '''
            if  self.getInitialPlayback() == True:
                self.view.spotifyPlayPauseButton.setStyleSheet(constants.SPOTIFY_PLAY_STATE_STYLE)
            else:
                self.view.spotifyPlayPauseButton.setStyleSheet(constants.SPOTIFY_PAUSED_STATE_STYLE)

            self.spotifyQueueThread.start()
            self.updateQueueField()
        else:
            self.view.currentlyPlayingLabel.setText("!!!!! Device is not connected !!!!!")
            print("No device found! Spotify player not started!")

        return None

    def getInitialPlayback(self) -> bool:
        '''
        Get the initial playback from spotify.
        '''
        temp = self.spotifyPlayer.getCurrentPlayback()
        self.setLocalPlaybackState(True if temp != None else False)
        return self.getLocalPlaybackState()


    def setLocalPlaybackState(self, state:bool) -> None:
        '''
        Spotify does not return a simple True/False is a user is actively playing
        so we have to keep a local playback state. 

        NOTE! THIS WILL BREAK IF A USER CHANGES THE STATE OF SPOTIFY OUTSIDE THE BARTENDER
        ie. Mobile App, Broswer, TV, etc...
        '''
        self.localPlaybackState = state
        return None
        
    def getLocalPlaybackState(self) -> bool:
        '''
        Return the local state
        '''
        return self.localPlaybackState 


    def updateCurrentPlayback(self, track, artist, uri) -> None:
        '''
        Update the label with the currently playing song
        '''
        self.view.currentlyPlayingLabel.setText("{} by {}".format(track, artist))
        self.attemptToRemoveFromQueue(uri)


    def playPauseButtonClicked(self) -> None:
        '''
        Control the state of spotify. Playing or Pause

        NOTE! THIS WILL BREAK IF A USER CHANGES THE STATE OF SPOTIFY OUTSIDE THE BARTENDER
        ie. Mobile App, Broswer, TV, etc...
        '''
        if  self.getLocalPlaybackState() == False:
            self.view.spotifyPlayPauseButton.setStyleSheet(constants.SPOTIFY_PLAY_STATE_STYLE)
            self.spotifyPlayer.play()
            self.setLocalPlaybackState(True)
        else:
            self.view.spotifyPlayPauseButton.setStyleSheet(constants.SPOTIFY_PAUSED_STATE_STYLE)
            self.spotifyPlayer.pause()
            self.setLocalPlaybackState(False)
        return None

    def nextTrack(self) -> None:
        '''
        Advance to the next track
        '''
        self.spotifyPlayer.next()
        return None

    def previousTrack(self) -> None:
        '''
        Restart track or go to the previous track
        '''
        self.spotifyPlayer.previous()
        return None

    def attemptToRemoveFromQueue(self, uri) -> None:
        '''
        A new song has started playing check and see if it was queue'd up by the Bartender
        if it was, remove it from our local queue because it is playing
        '''
        self.spotifyPlayer.checkAndRemoveFromQueue(uri)
        self.updateQueueField()

    def updateQueueField(self) -> None:
        '''
        Update the queue field when new selection is added
        '''
        self.view.spotifyQueueField.clear()
        currentQueue = self.spotifyPlayer.getQueue()
        if len(currentQueue) > 0:
            for item in currentQueue:
                track = f"TRACK: {item[0]}\n" + \
                        f"ARTIST: {item[1]}\n"
                self.view.spotifyQueueField.addItem(QtWidgets.QListWidgetItem(track))
        else:
            self.view.spotifyQueueField.addItem(QtWidgets.QListWidgetItem("No songs currently in Bartender queue."))

        return None

    def searchSpotify(self) -> None:
        '''
        Display the items returned from the spotify query
        '''
        self.view.spotifySearchResultsField.clear()
        self.spotifyPlayer.search(self.view.spotifySearchInputField.text())
        for key, value in self.spotifyPlayer.getRecentQuery().items():
            data = f"ID: {key}\n" + \
                   f"TRACK: {value[0]}\n" + \
                   f"ARTIST: {value[1]}\n"
            
            self.view.spotifySearchResultsField.addItem(QtWidgets.QListWidgetItem(data))
        return None

    def selectedSearch(self,item) -> None:
        '''
        Prompt the user to if they want to add the track to the queue
        '''
        itemDetails = item.text()
        userInput = QtWidgets.QMessageBox.question(self, "Request Track", f"Would you like to add the following track to the queue?\n\n{itemDetails}", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if userInput == QtWidgets.QMessageBox.Yes:
            data = itemDetails.split("\n")
            id = data[0].split("ID:")
            id = id[1].strip()
            self.spotifyPlayer.requestTrack(int(id))
            self.updateQueueField()
        return None