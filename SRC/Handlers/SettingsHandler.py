import yaml
import os

def GetAllData(Path) -> dict:
    try:
        with open(Path + "/Settings.yaml") as f:
            Data = yaml.safe_load(f)

        return Data

    except Exception as e:
        print(e)
        return None

def Write(Key, Info, Path, IsArray = False, Index = 0) -> bool:
    try:
        with open(Path + "/Settings.yaml", "r") as f:
            Data = yaml.safe_load(f)

            if not IsArray:
                Data[Key] = Info
            else:
                Data[Key][Index] = Info

            with open(Path + "/Settings.yaml", "w") as f:
                Dumped = yaml.dump(Data, f)

            return True

    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    print(GetAllData("/Users/mootbing/Desktop/textplifier/SRC/Settings.yaml"))