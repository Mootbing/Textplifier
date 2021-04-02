import tkinter as tk
from tkinter import colorchooser
import os
import webbrowser
import sys

#files
from Handlers import ClipboardHandler, SettingsHandler, EmoticonsHandler
from Classes import TextClass

FilePath = os.path.dirname(sys.argv[0])

# thank you so much https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
if getattr(sys, 'frozen', False):
    FilePath = os.path.dirname(sys.executable)
elif __file__:
    FilePath = os.path.dirname(__file__)

class App:

    def __init__(self, window, Width, Height):

        #constructor stuff
        self.window = window
        self.Width = Width
        self.Height = Height

        #default settings values
        self.ColorArray = [
            "#F67280",
            "#F8B195",
            "#355C7D",
            "#F67280",
            "red"
        ]

        self.RefocusOnCopy = False

        self.SetUpData()

        #images loading
        self.StuffToRemoveLater = []
        self.RefreshImage = tk.PhotoImage(file = FilePath + "/Images/Refresh.png").subsample(2, 2)
        self.SettingsImage = tk.PhotoImage(file = FilePath + "/Images/Settings.png").subsample(2, 2)
        self.SelectionTextImage = tk.PhotoImage(file = FilePath + "/Images/SelectTextPanel.png").subsample(2, 2)
        self.SelectionEmojiTextImage = tk.PhotoImage(file = FilePath + "/Images/TextMojis.png").subsample(2, 2)
        self.SelectHelpTextImage = tk.PhotoImage(file = FilePath + "/Images/Info.png").subsample(2, 2)

        self.SetUpUI()

        self.Emoticons = EmoticonsHandler.GetEmoticons()

        if self.Emoticons is None:
            self.ShowMessage("Failed To Load Emoticons", 1000, self.ColorArray[4])
            self.MakeButtonUI()
            return

        self.ClipboardEventListener(ClipboardHandler.GetText())

    def SetUpData(self):

        Data = SettingsHandler.GetAllData(FilePath)

        if Data is None:
            self.ShowMessage("Failed To Load Settings", 1000, self.ColorArray[4])
            return

        self.ColorArray = Data["ColorPallet"]

        self.RefocusOnCopy = Data["RefocusOnCopy"]

    def SetUpUI(self):

        VersionInfo = "Textplifier v0.1"

        self.window.geometry(f"{self.Width}x{self.Height}")
        
        self.window.title(VersionInfo)
        self.window.resizable(False, False)

        Icon = tk.PhotoImage(file=FilePath + "/Images/TextAmplifier.png")

        self.window.iconbitmap(FilePath + "/TextAmplifier.ico")
        self.window.tk.call('wm', 'iconphoto', self.window._w, Icon)
        self.window.iconphoto(False, Icon)

        self.SideBar = tk.Frame(width=52, height=self.Height)
        self.SideBar.place(x = 0, y = 0, anchor = "nw")

        self.TopBar = tk.Frame(width=self.Width, height=50)
        self.TopBar.place(x = 0, y = 0, anchor = "nw")

        #content
        self.ContentPane = tk.Frame(width=self.Width-52, height=self.Height-50)
        self.ContentPane.place(x = 52, y = 50, anchor = "nw")

        self.RefreshBackgroundColors()

        self.MakeButtonUI()

        self.StuffToRemoveLaterettings = tk.Button(image = self.SettingsImage, highlightbackground=self.ColorArray[2], command=self.MakeSettings)
        self.StuffToRemoveLaterettings.place(x = 0, rely = 1, anchor = 'sw')

        self.ShowTextOptions = tk.Button(image = self.SelectionTextImage, highlightbackground=self.ColorArray[2], command=self.MakeButtonUI)
        self.ShowTextOptions.place(x = 0, y = 50, anchor = 'nw')

        self.ShowEmojiOptions = tk.Button(image = self.SelectionEmojiTextImage, highlightbackground=self.ColorArray[2], command=self.MakeButtonEmojiText)
        self.ShowEmojiOptions.place(x = 0, y = 100, anchor = 'nw')

        self.ShowHelp = tk.Button(image = self.SelectHelpTextImage, highlightbackground=self.ColorArray[2], command=lambda: [print(FilePath + "/Help.html"), webbrowser.open("file://" + FilePath + "/Help/Help.html")])
        self.ShowHelp.place(x = 0, y = self.Height - 50, anchor = 'sw')

    def ClipboardEventListener(self, LastText):

        CurrentCopy = ClipboardHandler.GetText()

        if self.RefocusOnCopy and CurrentCopy != LastText:
            self.ShowMessage("Detected New Clipboard!", 1000)
            self.MakeButtonUI()
            self.window.focus_force()
        
        self.window.after(1000, lambda: [self.ClipboardEventListener(CurrentCopy)])

    def MakeButtonUI(self):

        TextObject = TextClass.Text(ClipboardHandler.GetText())

        ListOfTexts = TextObject.GetAll()[0]
        ListOfButtonNames = TextObject.GetAll()[1]

        self.ClearButtons()

        CurrentText = tk.Label(text=TextObject.GetString(), font=("Helvetica", 25), bg=self.ColorArray[0], foreground="white")
        CurrentText.place(x = (self.Width + 50)//2, y = 25, anchor = 'center')
        self.StuffToRemoveLater.append(CurrentText)

        ListOfTextFeatures = tk.Listbox(font=("Helvetica", 18), justify=tk.CENTER, highlightbackground = self.ColorArray[2], bg=self.ColorArray[2], foreground="white", borderwidth = 0, highlightthickness = 0)
        ListOfTextFeatures.place(x = 52, y = 50, anchor = "nw", width = self.Width-50, height=self.Height - 50)
        self.StuffToRemoveLater.append(ListOfTextFeatures)

        for i in range(len(ListOfTexts)):
            ListOfTextFeatures.insert(i, ListOfButtonNames[i])
            ListOfTextFeatures.bind('<Double-1>', lambda x: [self.ShowMessage(f"Message copied successfully!", 1000), ClipboardHandler.Copy(String = str(ListOfTexts[int(ListOfTextFeatures.curselection()[0])]))])  

        #last
        ButtonRefresh = tk.Button(image = self.RefreshImage, highlightbackground=self.ColorArray[2])
        ButtonRefresh.place(relx = 0, y = 0, anchor = 'nw')
        self.StuffToRemoveLater.append(ButtonRefresh)
        ButtonRefresh["command"] = lambda: [self.MakeButtonUI(), self.ShowMessage(f"Force Refreshed Clipboard!", 1000)]
    
    def ClearButtons(self):

        for button in self.StuffToRemoveLater:
            button.destroy()

        self.StuffToRemoveLater = []

    def MakeButtonEmojiText(self):

        self.ClearButtons()

        TopText = tk.Label(text="Text Emojis", font=("Helvetica", 25), bg=self.ColorArray[0], foreground="white")
        TopText.place(relx = 0.5, y = 25, anchor = 'center')
        self.StuffToRemoveLater.append(TopText)

        TextBox = tk.Listbox(font=("Helvetica", 18), highlightbackground = self.ColorArray[2], justify=tk.CENTER, bg=self.ColorArray[2], foreground="white", borderwidth = 0, highlightthickness = 0)
        TextBox.place(x = 52, y = 50, anchor = "nw", width = self.Width - 50, height=250)
        self.StuffToRemoveLater.append(TextBox)

        for i in range(len(self.Emoticons)):
            TextBox.insert(i, self.Emoticons[i])

            TextBox.bind('<Double-1>', lambda x: [ClipboardHandler.Copy(str(TextBox.get(TextBox.curselection()))), self.ShowMessage("Emoticon Copied Successfully!", 1000)])

    def MakeSettings(self):

        self.ClearButtons()

        self.SetUpData()

        TopText = tk.Label(text="Settings", font=("Helvetica", 25), bg=self.ColorArray[0], foreground="white")
        TopText.place(relx = 0.5, y = 25, anchor = 'center')
        self.StuffToRemoveLater.append(TopText)

        def SetRefocusOnCopy(Checked):
            self.RefocusOnCopy = Checked 
            if SettingsHandler.Write("RefocusOnCopy", self.RefocusOnCopy, FilePath):
                self.ShowMessage("Successfully Saved Setting", 1000)
            else:
                self.ShowMessage("Unable to Save Setting", 1000, self.ColorArray[4])

        IsChecked = tk.IntVar(value = int(self.RefocusOnCopy))
        Checkbox = tk.Checkbutton(text="Refocus On Copy?", bg=self.ColorArray[2], foreground="white", highlightbackground=self.ColorArray[2], variable = IsChecked, command = lambda: [SetRefocusOnCopy(bool(IsChecked.get()))])
        Checkbox.place(x = (self.Width + 54)//2, y = 50, anchor="n")
        self.StuffToRemoveLater.append(Checkbox)

        Data = SettingsHandler.GetAllData(FilePath)

        def SetColors(Color, Index):

            if Color is None:
                return

            self.ColorArray[Index] = Color

            if SettingsHandler.Write("ColorPallet", Color, FilePath, True, Index):
                self.ShowMessage("Successfully Saved Setting", 1000)
                self.RefreshBackgroundColors()
                self.MakeSettings() #refresh
            else:
                self.ShowMessage("Unable to Save Setting", 1000, self.ColorArray[4])

        i = 0

        for i in range(len(Data["ColorPallet"])):
            Tempbutton = tk.Button(text="Change "+Data["ColorPalletKey"][i], highlightbackground=Data["ColorPallet"][i], width = 25)
            self.StuffToRemoveLater.append(Tempbutton)
            Tempbutton.place(x = (self.Width + 54)//2, y = 80 + i * 20, anchor="n")
            Tempbutton.configure(command = lambda i=i : [SetColors(colorchooser.askcolor(self.ColorArray[i])[1], i)])
        
        i += 1

        def ResetColorsOfTheme():
            self.ColorArray = Data["ColorPalletDefault"]
            if SettingsHandler.Write("ColorPallet", self.ColorArray, FilePath):
                self.ShowMessage("Successfully Saved Setting", 1000)
                self.RefreshBackgroundColors()
                self.MakeSettings() #refresh
            else:
                self.ShowMessage("Unable to Save Setting", 1000, self.ColorArray[4])

        ResetColors = tk.Button(text="Reset Theme Colors", highlightbackground = self.ColorArray[2], width = 25)
        ResetColors.place(x = (self.Width + 54)//2, y = 90 + i * 20, anchor="n")
        ResetColors.configure(command = lambda i=i : [ResetColorsOfTheme()])
        self.StuffToRemoveLater.append(ResetColors)

    def RefreshBackgroundColors(self):
        self.TopBar.config(bg=self.ColorArray[0])
        self.SideBar.config(bg=self.ColorArray[1])
        self.ContentPane.config(bg=self.ColorArray[2])

    def ShowMessage(self, Message, Length, Color = ""):

        if Color == "":
            Color = self.ColorArray[3]
        
        DisplayBar = tk.Frame(width=self.Width, height=50, bg=Color)
        DisplayBar.place(relx = 0, rely = 0.9)

        DisplayMessage = tk.Label(text=Message, font=("Helvetica", 20), bg=Color, foreground="white")
        DisplayMessage.place(relx = 0.5, rely = 0.9, anchor = 'n')

        self.window.after(Length, lambda: [DisplayBar.destroy(), DisplayMessage.destroy()])


if __name__ == "__main__":
    window = tk.Tk()

    Application = App(window, 300, 300)

    window.mainloop()