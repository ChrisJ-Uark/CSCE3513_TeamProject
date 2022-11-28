import time
import tkinter as tk
from tkinter import ttk
from lib.AppObject import *
from lib.Frame_FKeys import *
from lib.playgame.Frame_GameBoard import *

class Screen_PlayGame(AppObject):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)

        self.createScreen()
        self.gridify()
        self.showSelf()
        self.hideSelf()

    def createScreen(self):
        self["bg"] = "#000000" #set black background
        self.createGameboardFrame()
        self.createFKeys()

    def createLabelScoreboard(self):
        TextColor = "#5b5bc3" # Light Blue
        BGColor = "#000000" # Black
        Font = self.strDefaultFont
        TextSize = 30

        self.labelScoreboard = tk.Label(self,
                                        text="Scoreboard",
                                        fg=TextColor, bg=BGColor, font=(Font, TextSize))

    def createGameboardFrame(self):
        self.frameGameboard = Frame_GameBoard(self)
        self.propagateWidget(self.frameGameboard)

    def createFKeys(self):
        self.frameFKeys = Frame_FKeys(self)
        self.frameFKeys.clearAllKeyText()
        #Assign F Keys
        self.frameFKeys.setKeyText(5, "F5 \nMove to \nEdit Game", 12)
        self.frameFKeys.setKeyText(4, "F4 \n(Debug)\nSimulator", 12)

    def getFrameFKeys(self):
        return self.frameFKeys

    def getFrameGameboard(self):
        return self.frameGameboard

    def gridify(self):
        MainFrameCols = 24
        MainFrameRows = 40
        # Position F Key - Row
        PosFKeyRow   = 35
        FKeyRowSpan = 5
        FKeyColSpan = 2

        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.grid(column=0,row=0,sticky="NSEW")
        for i in range(MainFrameCols):
            self.columnconfigure(i,weight=1, uniform="gridUniform")
        for i in range(MainFrameRows):
            self.rowconfigure(i,weight=1, uniform="gridUniform")

        self.frameGameboard.grid(column=2, row=1, columnspan=20, rowspan=32, padx=2,pady=2,sticky="NSEW")
        self.frameGameboard.gridify()

        self.frameFKeys.grid(column=0, row=PosFKeyRow, rowspan=FKeyRowSpan, columnspan=MainFrameCols, sticky="NSEW")
        self.frameFKeys.gridify()

    def setPlayersUsingList(self, listPlayers, listIDs):
        print(listPlayers)
        print(listIntID)
        print(listIDs)
        self.frameGameboard.setPlayersUsingList(listPlayers, listIDs)
        self.listOfListIntPlayerIDs = self.frameGameboard.getValidListIntID()
        print(self.listOfListIntPlayerIDs)
        self.trafficGenerator.setIDList(self.listOfListIntPlayerIDs[0],
                                        self.listOfListIntPlayerIDs[1])

    def updateScreen(self):
        if self.frameGameboard.frameGameTimer.isTimerActive() and not self.frameGameboard.frameGameTimer.isTimerPaused():
            self.frameGameboard.frameGameTimer.updateTimer()
            if abs(time.time() - self.floatHighScoreFlashLastTime) >= 0.25:
                self.flashTeamScore()
                self.floatHighScoreFlashLastTime = time.time()
            self.intIDAfter = self.root.after(1, self.updateScreen)
        elif self.frameWaitUntilPlay.isCountActive() and not self.frameWaitUntilPlay.isPaused():
            self.frameWaitUntilPlay.updateCount()
            self.intIDAfter = self.root.after(1, self.updateScreen)

    def flashTeamScore(self):
        charHighestTeam = self.frameGameboard.frameScoreboard.getListHighestTeamScore()[0]
        self.frameGameboard.frameScoreboard.flashTeamScore(charHighestTeam)
