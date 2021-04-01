import tkinter as tk
import os
import ClipboardHandler
import TextClass

FilePath = os.path.dirname(os.path.abspath(__file__))
DarkGrey = "#2F2F2F"
BabyBlue = "#8CBBFF"

class App:

    def __init__(self, window, Width, Height):

        self.Buttons = []
        self.window = window
        self.Width = Width
        self.Height = Height

        self.SetUpUI()

        self.ClipboardEventListener("")

    def SetUpUI(self):

        VersionInfo = "Textplifier v0.1"

        window.geometry(f"{self.Width}x{self.Height}")
        
        window.title(VersionInfo)
        window.resizable(False, False)

        SideBar = tk.Frame(width=50, height=self.Height, bg="#b46d3f")
        SideBar.place(x = 0, y = 0, anchor = "nw")

        TopBar = tk.Frame(width=self.Width-50, height=50, bg=BabyBlue)
        TopBar.place(x = 50, y = 0, anchor = "nw")

        #content
        ContentPane = tk.Frame(width=self.Width-50, height=550, bg=DarkGrey)
        ContentPane.place(x = 50, y = 50, anchor = "nw")

        self.UpdateUI()

    def ClipboardEventListener(self, LastText):

        CurrentCopy = ClipboardHandler.GetText()

        if CurrentCopy != LastText:
            print("Update Text")
            self.UpdateUI()
            self.window.focus_force()
        
        self.window.after(1000, lambda: [self.ClipboardEventListener(CurrentCopy)])

    def UpdateUI(self):

        TextObject = TextClass.Text(ClipboardHandler.GetText())

        ListOfTexts = TextObject.GetAll()[0]
        ListOfButtonNames = TextObject.GetAll()[1]

        print(ListOfButtonNames)

        for button in self.Buttons:
            button.destroy()

        self.Buttons = []

        CurrentText = tk.Label(text=TextObject.GetString(), font=("Helvetica", 25), bg=BabyBlue, foreground="white")
        CurrentText.place(relx = .5, y = 25, anchor = 'center')
        self.Buttons.append(CurrentText)

        for i in range(len(ListOfTexts)):

            ButtonsTemp = tk.Button(text=ListOfButtonNames[i], font=("Helvetica", 15), foreground="black", command = lambda i=i: [ClipboardHandler.Copy(ListOfTexts[i]), self.DisplayMessageBoard(f"Message copied successfully!", 1000)], highlightbackground=DarkGrey)
            ButtonsTemp.place(relx = .5, y = 25 * i + 75, anchor = 'center')
            self.Buttons.append(ButtonsTemp)

        #last

        ButtonRefresh = tk.Button(font=("Helvetica", 15), highlightbackground=DarkGrey)
        ButtonRefresh["text"] = "Force Refresh"
        ButtonRefresh.place(relx = 1, y = 62.5, anchor = 'e')
        self.Buttons.append(ButtonRefresh)
        ButtonRefresh["command"] = lambda: [self.UpdateUI()]
    
    def DisplayMessageBoard(self, Message, Length):
        
        DisplayBar = tk.Frame(width=self.Width, height=50, bg=BabyBlue)
        DisplayBar.place(relx = 0, rely = 0.925)

        DisplayMessage = tk.Label(text=Message, font=("Helvetica", 20), bg=BabyBlue, foreground="white")
        DisplayMessage.place(relx = 0.5, rely = 0.94, anchor = 'n')

        self.window.after(Length, lambda: [DisplayBar.destroy(), DisplayMessage.destroy()])


if __name__ == "__main__":
    window = tk.Tk()

    Application = App(window, 300, 600)

    window.mainloop()