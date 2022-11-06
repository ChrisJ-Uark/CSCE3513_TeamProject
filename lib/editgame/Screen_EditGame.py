import tkinter as tk
from tkinter import ttk
from lib.Database import *
from lib.Frame_FKeys import *
from lib.AppObject import *
from lib.editgame.Frame_TeamBoxes import *
from lib.editgame.MenuManager_EditGame import *

class Screen_EditGame(AppObject):
    INDEX_PINFO_ID = 0
    INDEX_PINFO_FNAME = 1
    INDEX_PINFO_LNAME = 2
    INDEX_PINFO_CODE = 3
    PLAYERSELECT = 0
    PLAYERNAME = 1
    ASKUSEPREVCODE = 2
    PLAYERCODENAME = 3
    DELETEDBCONFIRM = 4
    MOVETOPLAYCONFIRM = 5

    def __init__(self, tkRoot):
        super().__init__(tkRoot)
        
        self.database = Database()
        self.database.openConnection()
        
        self.createScreen()
        self.gridify()
        self.switchToMainMenu()
        self.hideSelf()
            
    def createScreen(self):
        self["bg"] = "#000000"
        self.createPageHeader()
        self.createTeamBoxes()
        self.createFKeys()
        self.createLabelFooter()
        self.createMenuManager()
        
    def createPageHeader(self):
        strTextColor = "#5b5bc3" # Light, purplish blue
        strBGColor = "#000000" # Black
        strFontStyle = self.strDefaultFont
        intFontSize = 25
        
        self.labelEditGame = tk.Label(self, text="Edit Current Game", fg=strTextColor, bg=strBGColor, font=(strFontStyle,intFontSize))
        self.propagateWidget(self.labelEditGame)
        
    def createTeamBoxes(self):
        self.frameTeamBoxes = Frame_TeamBoxes(self)
        self.propagateWidget(self.frameTeamBoxes)
        
    def createFKeys(self):
        self.frameFKeys = Frame_FKeys(self)
        self.frameFKeys.clearAllKeyText()
        self.frameFKeys.setKeyText(4,"F4 \n(Debug) \nFill Players")
        self.frameFKeys.setKeyText(5,"F5 \nMove to \nPlay")
        self.frameFKeys.setKeyText(7,"F7 \nDelete DB \nEntries")
        
    def createLabelFooter(self):
        strTextColor = "#000000" # Black
        strBGColor = "#d9d9d9" # Very light gray, almost white
        strFontStyle = self.strDefaultFont
        strFontSize = 14
    
        self.labelFooter = tk.Label(self, 
            text="<Del> to delete player, <Ins> to Manually Insert, or edit codename", 
            fg=strTextColor, bg=strBGColor, font=(strFontStyle,strFontSize))
        self.propagateWidget(self.labelFooter)
        
    def createMenuManager(self):
        self.menuManager = MenuManager_EditGame(self)
        self.menuManager.setDatabase(self.database)
        self.menuManager.setTeamBoxes(self.frameTeamBoxes)
        self.menuManager.createSelf()
        
    def gridify(self):
        # If either of below are edited, all widgets will need to be repositioned
        # i.e: All calls to grid with row/column updated
        intMainFrameCols = 24
        intMainFrameRows = 42
        # Position F Key - Row
        intPosFKeyRow = 35
        intFKeyRowSpan = 6
        intFKeyColSpan = 2
        
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.grid(column=0,row=0,sticky="NSEW")
        self.menuManager.grid(column=6,row=8,columnspan=12,rowspan=20,sticky="NSEW")
        self.menuManager.gridify()
        
        for i in range(intMainFrameCols):
            self.columnconfigure(i,weight=1, uniform="gridUniform")
        for i in range(intMainFrameRows):
            self.rowconfigure(i,weight=1, uniform="gridUniform")
    
        self.labelEditGame.grid(column=0,row=0,columnspan=24,rowspan=2,sticky="SEW")
        
        self.frameTeamBoxes.grid(column=2,row=2,columnspan=20, rowspan=31,sticky="NSEW")
        self.frameTeamBoxes.gridify()
        self.frameTeamBoxes.showSelf()
        
        self.frameFKeys.grid(column=0, row=intPosFKeyRow, rowspan=intFKeyRowSpan, columnspan=intMainFrameCols, sticky="NSEW")
        self.frameFKeys.gridify()
        
        self.labelFooter.grid(column=0,row=41,columnspan=24,rowspan=1,sticky="NSEW")
        
    def getMenuState(self):
        return self.menuManager.getMenuState()
        
    def getPlayerList(self):
        return self.frameTeamBoxes.getPlayerList()

    def closeDB(self):
        print("Closing DB...")
        self.database.closeDB_NoCommit()
        
    def moveArrow(self, intOffsetX, intOffsetY):
        if self.frameTeamBoxes.isValidArrowOffset(intOffsetX, intOffsetY):
            self.frameTeamBoxes.moveArrow(intOffsetX, intOffsetY)
            self.root.update()
            
    def getPlayerAtArrow(self):
        return self.frameTeamBoxes.getPlayerAtArrow()
        
    def openDeleteDBConfirmMenu(self):
        self.menuManager.showSelf()
        self.menuManager.openDeleteDBConfirmMenu()
        
    def bind_ChangeToPlay(self, mFunc):
        self.menuManager.bind_ChangeToPlay(mFunc)
            
    def openAddPlayerName(self):
        self.menuManager.openAddPlayerName()
        
    def closeAllMenus(self):
        self.menuManager.closeAllMenus()
        
    def openAddCodename(self):
        self.menuManager.openAddCodename()
        
    def openMoveToPlayConfirm(self):
        self.menuManager.showSelf()
        self.menuManager.openMoveToPlayConfirm()
        
    def switchToMainMenu(self):
        self.menuManager.switchToMainMenu()
        
    def addPlayer(self, strPlayer, strCode):
        self.frameTeamBoxes.addPlayer(strPlayer, strCode)
        self.root.update()
        
    def deletePlayer(self, event=None):
        self.frameTeamBoxes.deletePlayer()
        self.root.update()
        
    def clearAllPlayers(self):
        self.frameTeamBoxes.deleteAllPlayers()
        self.root.update()
        
    def debug_FillAllPlayers(self):
        listRedPlayerNames = ["Janice Evans", "Raymond Griffin", "Patrick Hill", "Matthew Bryant",
                            "Jason Martin", "Catherine Carter", "Kevin Sanders", "Gary Young",
                            "Anthony Russel", "Pamela Hart", "Leonardo Harris", "Nick Wells",
                            "Simon Mitchell", "Paul Willis", "Paula Reyes"]
        listGreenPlayerNames = ["Steven Perez", "Gary Patterson", "Janice Hall", "Kenneth Edwards",
                                "Walter Howard", "Norman Hughes", "Lewis Hayes", "Angela Shaw",
                                "Burt Davis", "Kevin Simpson", "Carlene Brown", "Frederick Baker",
                                "Derick Smith", "Stephen Morris", "Max Reed"]
        listRedCodenames = ["ProudPancake","ExcitingEgg","SmoggyGhost","HollowHorse",
                            "BarbaricMouse","GracefulTiger","BusyBear","BrawnyBee",
                            "DullBell","CharmingJellyfish", "GentleCow", "CleverPotato",
                            "SpitefulArmadillo","DapperVelociraptor","MeekMouse"]
        listGreenCodenames = ["PhantomFairy","GrumpyCat","ChiefRat","RaggedRabbit",
                            "SpikyWorm","DecisiveDuck","LoudCloud","GraySnail",
                            "SaltyPig","JollySponge","SpicySugar","DraconianDeer",
                            "SoftTomato","IcyIgloo","MoldyApple"]
        for j in range(0, 2):
            for i in range(0, 15):
                if j == 0:
                    self.frameTeamBoxes.setArrowPos(Frame_TeamBoxes.REDARROWPOS, i)
                    self.frameTeamBoxes.addPlayer(listRedPlayerNames[i],
                                                    listRedCodenames[i])
                else:
                    self.frameTeamBoxes.setArrowPos(Frame_TeamBoxes.GREENARROWPOS, i)
                    self.frameTeamBoxes.addPlayer(listGreenPlayerNames[i],
                                                    listGreenCodenames[i])