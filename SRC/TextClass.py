class Text:

    Regular = list("abcdefghijklmnopqrstuvwxyz")

    def __init__(self, String):
        self.TextString = String

    def GetString(self) -> str:
        return self.TextString

    def MatchTextToArrays(self, ArrayToCompare) -> list:
        
        NewText = []

        for character in self.TextString:
            if character.lower() in self.Regular:
                NewText.append(ArrayToCompare[int(self.Regular.index(str(character.lower())))])
            else:
                NewText.append(character)

        return NewText

    def GetFlippedText(self) -> str:
        Flipped = list("ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz") #taken from https://qwerty.dev/upside-down-text-generator/
        return "".join(list(reversed(self.MatchTextToArrays(Flipped))))

    def GetEmojiedText(self) -> str:
        EmojiText = list("🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿".replace(" ", ""))
        return "‎".join(self.MatchTextToArrays(EmojiText))

    def GetHackermanText(self) -> str:
        HackmanText = "a̶̢̦̮̼͉͑̏̄̍̐̓͝ b̸̫̖̳̯̼̰̣͒̅͆ c̴͕̺̩͗̃̈́̆̊̆̕͘̕͜ͅ ḋ̴̘͆̑̂͘͝ e̶̛͈͓͍̗̬͐̀̾̉̋͜ f̶͊̌̽̓̇̋̃̾̆̈́ͅ g̸̨̠̪̏́̅͆͊͗ h̸̢̥̱̮͍̱̝̺͐ i̵̝͇͊̉̀ ǰ̴̡̳̥̰͇̺͙̲̀͝ͅ k̶̨̟̭͚̮̥͆̀̑͋͑̓̒̑̋̉ l̵̜̭̤̼̠͛̀̇ m̶̹͍̹̥̺̰̊͆̉̋͒͌ n̴͇͈͙̥̻̟̺̿͗̓̐ ö̶̮̜́̑͌͘͘ p̶̤̯̟̀͐͋̆̀̄̈̚͜͝ q̵̢̛̖͈̹̮̰̲̹͖̦͊͋̌͝ r̴̖̻̅̓̄̆ s̴̹͈͎̝̐̀̑̍ ţ̴̟͖̖͍̓͑̕ u̵̢̖̟̭̪͆͆͆̐͑̊̋ v̵̡̢̢͈̮̗̳̮̱̄̊̔͌́́͗̎͜ w̸̭̪̳̗̳͖̲͑̄͊̋͜ x̸̟͗̑͊̈́̊̔͗̀̍͝ y̶̥̣̥̘͇̹̙̕͝ z̵̗̙̙͌͌̾̏̏̋̕̚͝".split(" ")
        return "‎".join(self.MatchTextToArrays(HackmanText))

    def GetFancyAssText(self) -> str:
        FancyFont = list("𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫")
        return "‎".join(self.MatchTextToArrays(FancyFont))


    def GetSpacedText(self) -> str:
        NewText = []

        for character in self.TextString:
            NewText.append(character + " ")
        
        return "".join(NewText)

    def GetAll(self) -> (list, list):

        All = {}

        for function in self.__dir__():
            if "Get" in str(function) and "Text" in str(function):
                All[str(function).replace("Get", "")] = getattr(self, function)()

        return (list(All.values()), list(All.keys()))

if __name__ == "__main__":
    t = Text("abcd")
    print(t.GetEmojiedText())