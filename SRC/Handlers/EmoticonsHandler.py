import requests
from bs4 import BeautifulSoup
import re

def GetEmoticons() -> list: #uses the table on this site https://slangit.com/emoticons/kaomoji

    Emoticons = []

    try:
        url = requests.get("https://slangit.com/emoticons/kaomoji")
        soup = BeautifulSoup(url.content, 'html.parser')

        for EachElement in soup.find_all("td", attrs={"class":"center"}):
            Emoticons.append(re.sub("</.*>", "", str(EachElement)).replace("<td class=\"center\">", ""))
        
        return Emoticons

    except Exception as e:
        print(e)
        return None
    
if __name__ == "__main__":
    print(GetEmoticons())