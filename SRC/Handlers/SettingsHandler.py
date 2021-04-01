import yaml
import os

def GetAllData(Path) -> dict:
    try:
        with open(Path + "/Settings.yaml") as f:
            
            print(Path + "/Settings.yaml")

            Data = yaml.safe_load(f)

            ReturnMap = {}

            ReturnMap["ColorPallet"] = Data["ColorPallet"]

            ReturnMap["RefocusOnCopy"] = Data["RefocusOnCopy"]

        return ReturnMap

    except Exception as e:
        print(e)
        return None

def Write(Key, Info, Path) -> bool:
    try:
        with open(Path + "/Settings.yaml", "w") as f:
            
            Data = yaml.safe_load(f)

            Data[Key] = Info

            Dumped = yaml.dump(Data, f)

            return True

    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    print(GetAllData("/Users/mootbing/Desktop/textplifier/SRC/Settings.yaml"))