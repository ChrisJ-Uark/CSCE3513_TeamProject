from sys import platform
import time
from pynput import keyboard
import tkinter as tk
from tkinter import ttk
from lib.editgame.Screen_EditGame import *
from lib.playgame.Screen_PlayGame import *
from lib.splash.Screen_Splash import *
from lib.AppState import *
from lib.InputListener import *

class App(tk.Frame):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)
        self.root = tkRoot
        self.root.configure(background="#000000")
    
        # Root Window
        self.root.title("Entry Terminal")
        self.root.geometry("1200x800+0+0") # Originally tested on 1200x800
        self.root.minsize(1000,700) # Minimum size of window is 1200x700 before scrunching
        #self.root.resizable(False, False)
        
        print("Running for platform: {}".format(platform))
        if platform == "win32" or platform == "win64" or platform == "win82":
            self.root.state("zoomed")
        else:
            self.root.wm_attributes('-zoomed',1)
        self.propagateWidget(self.root)
        
        self.gridConfigure()
        
        # Needed for bug with F10 key.
        self.inputSim = keyboard.Controller()
        
        self.appMembers()
        
        self.appState.setState(AppState.S_SPLASH)
        self.screen = self.screen_Splash
        self.changeScreens(AppState.S_SPLASH)
        self.startInputListener()
        self.root.update()
        print("Waiting 3 seconds...")
        self.idRootAfter = self.root.after(3000, self.showSplashFor3Sec)
    
    def appMembers(self):
        # App members
        # I moved this into it's own function just for the sake of separating things and clarity. -Mason Woodward
        self.screen_Splash = Screen_Splash(self)
        self.screen_Splash.grid(column=0, row=0,sticky="NSEW")
        self.screen_EditGame = Screen_EditGame(self)
        self.screen_EditGame.bind_ChangeToPlay(self.changeToPlay)
        self.screen_EditGame.grid(column=0, row=0,sticky="NSEW")
        self.screen_PlayGame = Screen_PlayGame(self)
        self.screen_PlayGame.bind_MoveToEdit(self.changeToEdit)
        self.screen_PlayGame.grid(column=0, row=0,sticky="NSEW")
        
        self.appState = AppState()
        self.appState.setState(AppState.S_SPLASH)
        self.inputListener = InputListener()
        self.inputListener.bindAllScreensAndAppState(self.screen_Splash, self.screen_EditGame,
                                                    self.screen_PlayGame, self.appState)
        
    def gridConfigure(self):
        # Using grid instead of pack to allow frame-on-frame for
        #    inserting player menu, and other similar menus
        # Put this into it's own function for the sake of separation and clarity
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        self["bg"] = "#000000"
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.grid(column=0, row=0,sticky="NSEW")
        
    # Size control - prevent widget from over-expanding outside grid cell
    # This should be applied to most widgets
    def propagateWidget(self, widget):
        widget.pack_propagate(0)
        widget.grid_propagate(0)
        
    def changeScreens(self, nextScreen):
        self.unloadCurrentScreen()
        self.loadScreen(nextScreen)
        self.root.update()
        
    # Used to bind in Screen_EditGame
    def changeToPlay(self):
        self.screen_EditGame.closeAllMenus()
        self.changeScreens(AppState.S_PLAYGAME)
        self.screen_PlayGame.startWaitTimer()
        
    # Used to bind in Screen_PlayGame
    def changeToEdit(self):
        self.screen_PlayGame.closeAllMenus()
        self.screen_PlayGame.resetGameTimer()
        self.screen_PlayGame.endTrafficGenerator()
        self.screen_PlayGame.clearGameAction()
        self.screen_PlayGame.resetScoreboard()
        self.changeScreens(AppState.S_EDITGAME)
            
    def unloadCurrentScreen(self):
        if self.appState.getState() == AppState.S_SPLASH:
            self.unloadScreen_Splash()
        elif self.appState.getState() == AppState.S_EDITGAME:
            self.unloadScreen_EditGame()
        elif self.appState.getState() == AppState.S_PLAYGAME:
            self.unloadScreen_PlayGame()
        else:
            print("Changing from unknown screen")
            
    def loadScreen(self, nextScreen):
        #change the title of this function... hopefully makes this more clear? Change back if y'all are not fans. - Mason Woodward
        if nextScreen == AppState.S_SPLASH:
            print("Loading Splash...")
            self.appState.setState(AppState.S_SPLASH)
            self.loadScreen_Splash()
        elif nextScreen == AppState.S_EDITGAME:
            print("Loading Edit Game...")
            self.appState.setState(AppState.S_EDITGAME)
            self.loadScreen_EditGame()
        elif nextScreen == AppState.S_PLAYGAME:
            print("Loading Play Game...")
            self.appState.setState(AppState.S_PLAYGAME)
            self.loadScreen_PlayGame()
        else:
            print("Not a valid screen!")
    
    def loadScreen_Splash(self):
        self.screen = self.screen_Splash
        self.screen.showSelf()
        
    def unloadScreen_Splash(self):
        self.screen.hideSelf()
            
    def loadScreen_EditGame(self):
        self.screen = self.screen_EditGame
        self.screen.showSelf()
        self.screen.tkraise()
        
    def unloadScreen_EditGame(self):
        self.screen.hideSelf()
        
    def loadScreen_PlayGame(self):
        self.screen = self.screen_PlayGame
        listPlayers = self.screen_EditGame.getPlayerList()
        listPlayerIDs = self.screen_EditGame.getPlayerIDList()
        self.screen.setPlayersUsingList(listPlayers, listPlayerIDs)
        self.screen.showSelf()
        
    def unloadScreen_PlayGame(self):
        self.screen.hideSelf()
        
    def showSplashFor3Sec(self):
        print("3 seconds finished.")
        self.root.after_cancel(self.idRootAfter)
        self.changeScreens(AppState.S_EDITGAME)
            
    def closeDB(self):
        if self.screen_EditGame == None:
            print("Closing DB...")
            self.database.closeDB_NoCommit()
        else:
            self.screen_EditGame.closeDB()
        
    def startInputListener(self):
        self.inputListener.start()
        
def driver_TK():
    tkRoot = tk.Tk()
    app = App(tkRoot)
    app.mainloop()
    app.closeDB()

if __name__ == "__main__":
    driver_TK()
