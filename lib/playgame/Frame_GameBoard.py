import tkinter as tk
from tkinter import ttk
from lib.AppObject import *
from lib.playgame.Frame_Scoreboard import *
from lib.playgame.Frame_GameAction import *
from lib.playgame.Frame_GameTimer import *

class Frame_GameBoard(AppObject):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)

        self.createSelf()
        
    def createSelf(self):
        strBorderColor = "#FFFFFF"
    
        self["bg"] = strBorderColor
        
        self.frameScoreboard = Frame_Scoreboard(self)
        self.propagateWidget(self.frameScoreboard)
        self.frameGameAction = Frame_GameAction(self)
        self.propagateWidget(self.frameGameAction)
        self.frameGameTimer = Frame_GameTimer(self)
        self.propagateWidget(self.frameGameTimer)
        
    def setPlayersUsingList(self, listPlayers):
        self.frameScoreboard.setPlayersUsingList(listPlayers)
        
    def gridify(self):
        intBackgroundCols = 10
        intBackgroundRows = 10
        
        for i in range(intBackgroundCols):
            self.columnconfigure(i,weight=1, uniform="gridUniform")
        for i in range(intBackgroundRows):
            self.rowconfigure(i,weight=1, uniform="gridUniform")
            
        self.frameGameAction.grid(column=0, row=0, columnspan=10, rowspan=3, padx=2, pady=2, sticky="NSEW")
        self.frameGameAction.gridify()
        self.frameScoreboard.grid(column=0, row=3, columnspan=10, rowspan=6, padx=2, pady=2, sticky="NSEW")
        self.frameScoreboard.gridify()
        self.frameGameTimer.grid(column=0, row=9, columnspan=10, rowspan=1, padx=2, pady=2, sticky="NSEW")
        self.frameGameTimer.gridify()