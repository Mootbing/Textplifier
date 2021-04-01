import pyperclip

def GetText() -> str:
    return pyperclip.paste()

def Copy(String):
    pyperclip.copy(String)