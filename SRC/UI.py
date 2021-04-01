import tkinter as tk
import os

#files
from Handlers import ClipboardHandler, SettingsHandler, EmoticonsHandler
from Classes import TextClass

FilePath = os.path.dirname(os.path.abspath(__file__))

class App:

    def __init__(self, window, Width, Height):

        #constructor stuff
        self.window = window
        self.Width = Width
        self.Height = Height

        #default settings values
        self.BGColor = "#355C7D"
        self.TopBarColor = "#F67280"
        self.SideBarColor = "#F8B195"
        self.EmergencyMessageColor = "red"
        self.DefaultMessageColor = self.TopBarColor
        self.RefocusOnCopy = False

        self.SetUpData()

        #images loading
        self.StuffToRemoveLater = []
        self.RefreshImage = tk.PhotoImage(file = FilePath + "/Images/Refresh.png").subsample(2, 2)
        self.SettingsImage = tk.PhotoImage(file = FilePath + "/Images/Settings.png").subsample(2, 2)
        self.SelectionTextImage = tk.PhotoImage(file = FilePath + "/Images/SelectTextPanel.png").subsample(2, 2)
        self.SelectionEmojiTextImage = tk.PhotoImage(file = FilePath + "/Images/TextMojis.png").subsample(2, 2)

        self.SetUpUI()

        self.ClipboardEventListener("")

    def SetUpData(self):

        Data = SettingsHandler.GetAllData(FilePath)
        print(Data)

        if Data is None:
            self.ShowMessage("Failed To Load Settings", 1000, self.EmergencyMessageColor)
            return

        self.TopBarColor = Data["ColorPallet"][0]
        self.SideBarColor = Data["ColorPallet"][1]
        self.BGColor = Data["ColorPallet"][2]
        self.DefaultMessageColor = Data["ColorPallet"][3]
        self.EmergencyMessageColor = Data["ColorPallet"][4]

        self.RefocusOnCopy = Data["RefocusOnCopy"]

    def SetUpUI(self):

        VersionInfo = "Textplifier v0.1"

        window.geometry(f"{self.Width}x{self.Height}")
        
        window.title(VersionInfo)
        window.resizable(False, False)

        self.SideBar = tk.Frame(width=52, height=self.Height, bg=self.SideBarColor)
        self.SideBar.place(x = 0, y = 0, anchor = "nw")

        self.TopBar = tk.Frame(width=self.Width, height=50, bg=self.TopBarColor)
        self.TopBar.place(x = 0, y = 0, anchor = "nw")

        #content
        self.ContentPane = tk.Frame(width=self.Width-52, height=self.Height-50, bg=self.BGColor)
        self.ContentPane.place(x = 52, y = 50, anchor = "nw")

        self.MakeButtonUI()

        self.StuffToRemoveLaterettings = tk.Button(image = self.SettingsImage, highlightbackground=self.BGColor, command=self.MakeSettings)
        self.StuffToRemoveLaterettings.place(x = 0, rely = 1, anchor = 'sw')

        self.ShowTextOptions = tk.Button(image = self.SelectionTextImage, highlightbackground=self.BGColor, command=self.MakeButtonUI)
        self.ShowTextOptions.place(x = 0, y = 50, anchor = 'nw')

        self.ShowEmojiOptions = tk.Button(image = self.SelectionEmojiTextImage, highlightbackground=self.BGColor, command=self.MakeButtonEmojiText)
        self.ShowEmojiOptions.place(x = 0, y = 100, anchor = 'nw')

    def ClipboardEventListener(self, LastText):

        if not self.RefocusOnCopy:
            return

        CurrentCopy = ClipboardHandler.GetText()

        if CurrentCopy != LastText:
            print("Update Text")
            self.MakeButtonUI()
            self.window.focus_force()
        
        self.window.after(1000, lambda: [self.ClipboardEventListener(CurrentCopy)])

    def MakeButtonUI(self):

        TextObject = TextClass.Text(ClipboardHandler.GetText())

        ListOfTexts = TextObject.GetAll()[0]
        ListOfButtonNames = TextObject.GetAll()[1]

        self.ClearButtons()

        CurrentText = tk.Label(text=TextObject.GetString(), font=("Helvetica", 25), bg=self.TopBarColor, foreground="white")
        CurrentText.place(relx = 0.5, y = 25, anchor = 'center')
        self.StuffToRemoveLater.append(CurrentText)

        for i in range(len(ListOfTexts)):

            ButtonsTemp = tk.Button(text=ListOfButtonNames[i], font=("Helvetica", 15), foreground="black", command = lambda i=i: [ClipboardHandler.Copy(ListOfTexts[i]), self.ShowMessage(f"Message copied successfully!", 1000)], highlightbackground=self.BGColor)
            ButtonsTemp.place(relx = 0.5, y = 25 * i + 75, anchor = 'center')
            self.StuffToRemoveLater.append(ButtonsTemp)

        #last

        ButtonRefresh = tk.Button(image = self.RefreshImage, highlightbackground=self.BGColor)
        ButtonRefresh.place(relx = 0, y = 0, anchor = 'nw')
        self.StuffToRemoveLater.append(ButtonRefresh)
        ButtonRefresh["command"] = lambda: [self.MakeButtonUI(), self.ShowMessage(f"Force Refreshed Clipboard!", 1000)]
    
    def ClearButtons(self):

        for button in self.StuffToRemoveLater:
            button.destroy()

        self.StuffToRemoveLater = []

    def MakeButtonEmojiText(self):

        self.ClearButtons()

        TopText = tk.Label(text="Text Emojis", font=("Helvetica", 25), bg=self.TopBarColor, foreground="white")
        TopText.place(relx = 0.5, y = 25, anchor = 'center')
        self.StuffToRemoveLater.append(TopText)

        TextBox = tk.Listbox(highlightbackground = self.BGColor, bg=self.BGColor, foreground="white", borderwidth = 0, highlightthickness = 0)
        TextBox.place(x = 52, y = 50, anchor = "nw", width = self.Width, height=250)
        self.StuffToRemoveLater.append(TextBox)

        Emoticons = EmoticonsHandler.GetEmoticons()

        if Emoticons is None:
            self.ShowMessage("Failed To Load Emoticons", 1000, self.EmergencyMessageColor)

            self.MakeButtonUI()

            return

        for i in range(len(Emoticons)):

            TextBox.insert(i, Emoticons[i])

            TextBox.bind('<Double-1>', lambda x: [ClipboardHandler.Copy(str(TextBox.get(TextBox.curselection()))), self.ShowMessage("Emoticon Copied Successfully!", 1000)])

    def MakeSettings(self):

        self.ClearButtons()

        self.SetUpData()

        TopText = tk.Label(text="Settings", font=("Helvetica", 25), bg=self.TopBarColor, foreground="white")
        TopText.place(relx = 0.5, y = 25, anchor = 'center')
        self.StuffToRemoveLater.append(TopText)

        def SetRefocusOnCopy(Checked):
            SettingsHandler.Write("RefocusOnCopy", self.RefocusOnCopy, FilePath)
            self.RefocusOnCopy = Checked 

        IsChecked = tk.IntVar(value = int(self.RefocusOnCopy))
        Checkbox = tk.Checkbutton(text="Refocus On Copy?", variable = IsChecked, command = lambda: [SetRefocusOnCopy(bool(IsChecked.get()))])
        Checkbox.place(x = 50, y = 50, anchor = "nw")

    def ShowMessage(self, Message, Length, Color = ""):

        if Color == "":
            Color = self.DefaultMessageColor
        
        DisplayBar = tk.Frame(width=self.Width, height=50, bg=Color)
        DisplayBar.place(relx = 0, rely = 0.9)

        DisplayMessage = tk.Label(text=Message, font=("Helvetica", 20), bg=Color, foreground="white")
        DisplayMessage.place(relx = 0.5, rely = 0.9, anchor = 'n')

        self.window.after(Length, lambda: [DisplayBar.destroy(), DisplayMessage.destroy()])


if __name__ == "__main__":
    window = tk.Tk()

    Application = App(window, 300, 300)

    window.mainloop()