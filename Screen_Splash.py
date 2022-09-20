import tkinter as tk
from tkinter import ttk

class Screen_Splash(tk.Frame):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)
        self.root = tkRoot
        
        self.createScreen()
        self.gridify()
        
        
    # Size control - prevent widget from over-expanding outside grid cell
    # This should be applied to most widgets
    def propagateWidget(self, widget):
        widget.pack_propagate(False)
        widget.grid_propagate(False)
        
    def destroyMain(self):
        self.mainFrame.destroy()
        
    def hideSelf(self):
        self.mainFrame.grid_remove()
        
    def showSelf(self):
        self.mainFrame.grid()
        
    def createScreen(self):
        strBGColor = "#000000"
    
        self.mainFrame = tk.Frame(self.root, 
            bg=strBGColor) 
        self.propagateWidget(self.mainFrame)
        self.imgSplash = tk.PhotoImage(file="./logo.png")
        self.labelSplash = tk.Label(self.mainFrame,
            image=self.imgSplash)
        
    def gridify(self):
        self.mainFrame.grid(column=0,row=0,sticky="NSEW")
        self.labelSplash.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        
