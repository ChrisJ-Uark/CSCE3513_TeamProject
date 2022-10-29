import tkinter as tk
from tkinter import ttk
from lib.Menu import *

class Menu_MoveToPlayConfirm(Menu):
    def __init__(self, tkRoot, mSubmitYes, mSubmitNo):
        super().__init__(tkRoot)
        
        self.methodSubmitYes = mSubmitYes
        self.methodSubmitNo = mSubmitNo
        self.createSelf()
        self.gridify()

    def enableSelf(self):
        self.tkraise()
        self.buttonSubmitYes["state"]="normal"
        self.buttonSubmitNo["state"]="normal"
        self.buttonSubmitYes.bind("<Return>",self.submitYes)
        self.buttonSubmitNo.bind("<Return>",self.submitNo)
        
    def disableSelf(self):
        self.buttonSubmitYes["state"]="disabled"
        self.buttonSubmitNo["state"]="disabled"
        self.buttonSubmitYes.unbind("<Return>")
        self.buttonSubmitNo.unbind("<Return>")
        
    def submitNo(self,event=None):
        self.methodSubmitNo()
        
    def submitYes(self, event=None):
        self.methodSubmitYes()
            
    def createSelf(self):
        strBorderColor = "#5b5bc3"
        strBGColor = "#000000"
        strTextcolorError = "#FF0000" # True Red
        strTextcolorMain = "#FFFFFF" # Full White
        strFont = self.strDefaultFont
        intTextsizeHead = 20
        intTextsizeError = 14
        intTextsizeMain = 16
    
        self.propagateWidget(self)
        self.frameInterior = tk.Frame(self, bg=strBGColor)
        self.labelHead = tk.Label(self.frameInterior,
            text="You are about to move \nto the \'Play Screen\' Window",
            fg = strTextcolorMain, bg=strBGColor,font=(strFont,intTextsizeHead))
        self.labelHint = tk.Label(self.frameInterior,
            text="Are you certain to wish to continue?",
            fg = strTextcolorMain, bg=strBGColor, font=(strFont,intTextsizeMain))
        self.buttonSubmitYes = tk.Button(self.frameInterior,
            text="Yes",
            command=self.submitYes,
            state="disabled",
            fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeMain))
        self.buttonSubmitYes.bind("<Return>",self.submitYes)
        self.buttonSubmitNo = tk.Button(self.frameInterior,
            text="No",
            command=self.submitNo,
            state="disabled",
            fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeMain))
        self.buttonSubmitNo.bind("<Return>",self.submitNo)
        
    def gridify(self):
        intBorderSize = 10
        self.frameInterior.pack(side="top", fill="both", expand=True, 
            padx=intBorderSize, pady=intBorderSize)
        
        intFrameInsPCols = 12
        intFrameInsPRows = 12
        
        for i in range(intFrameInsPCols):
            self.frameInterior.columnconfigure(i,weight=1,uniform="uniformIns")
        for i in range(intFrameInsPRows):
            self.frameInterior.rowconfigure(i,weight=1,uniform="uniformIns")
        self.labelHead.grid(column=0,row=0,columnspan=intFrameInsPCols,rowspan=2,sticky="NSEW")
        self.labelHint.grid(column=0,row=5,rowspan=2,columnspan=intFrameInsPCols,sticky="NSEW")
        self.buttonSubmitYes.grid(column=3,row=9,rowspan=2,columnspan=2,sticky="NSEW")
        self.buttonSubmitNo.grid(column=7,row=9,rowspan=2,columnspan=2,sticky="NSEW")