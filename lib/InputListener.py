from pynput import keyboard
from lib.AppState import *
from lib.editgame.Screen_EditGame import *
from lib.playgame.Screen_PlayGame import *
from lib.splash.Screen_Splash import *

class InputListener:
    def __init__(self):
        self.listener = None
        # Needed for bug with F10 key.
        self.inputSim = keyboard.Controller()
        
    def bindAllScreensAndAppState(self, splash, edit, play, appState):
        self.screen_Splash = splash
        self.screen_EditGame = edit
        self.screen_PlayGame = play
        self.appState = appState
        
    #condensed Screen and AppState into one function
        
    def start(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.start()
        
    def isRunning(self):
        return self.listener != None
        
    def on_release(self, key):
        return True
		#Simplified this function
        
    def on_press(self, key):
        if self.appState.getState() == AppState.S_EDITGAME:
            if self.screen_EditGame.getMenuState() == self.screen_EditGame.PLAYERSELECT:
                self.editgame_PlayerSelect(key)
            elif self.screen_EditGame.getMenuState() != self.screen_EditGame.PLAYERSELECT:
                self.editgame_PlayerIns(key)
        elif self.appState.getState() == AppState.S_PLAYGAME:
            self.playgame_Listen(key)
        elif self.appState.getState() == AppState.S_SPLASH:
            pass
        self.any_InputListen(key)
        
    def any_InputListen(self, key):
        if key == keyboard.Key.f10:
            self.inputSim.press(keyboard.Key.f10)
        
    def editgame_PlayerSelect(self, key):
        if key == keyboard.Key.up:
            self.screen_EditGame.moveArrow(0,-1)
        elif key == keyboard.Key.down:
            self.screen_EditGame.moveArrow(0,1)
        if key == keyboard.Key.left:
            self.screen_EditGame.moveArrow(-1,0)
        elif key == keyboard.Key.right:
            self.screen_EditGame.moveArrow(1,0)
            
        if key == keyboard.Key.insert:
            self.screen_EditGame.openAddPlayerName()
        if key == keyboard.Key.delete:
            self.screen_EditGame.deletePlayer()
            
        if key == keyboard.Key.f5:
            self.screen_EditGame.openMoveToPlayConfirm()
            
        if key == keyboard.Key.f7:
            self.screen_EditGame.openDeleteDBConfirmMenu()
            
    def editgame_PlayerIns(self, key):
        if key == keyboard.Key.esc:
            self.screen_EditGame.closeAllMenus()
            
    def playgame_Listen(self, key):
        if key == keyboard.Key.f5:
            if self.screen_PlayGame.getMenuState() == Screen_PlayGame.MENU_MAIN or self.screen_PlayGame.getMenuState() == Screen_PlayGame.MENU_WAITSTART:
                self.screen_PlayGame.openMoveToEditMenu()
        if key == keyboard.Key.esc:
            self.screen_PlayGame.closeAllMenus()