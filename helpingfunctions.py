import eyed3
from mutagen.mp3 import MP3
import json

def addData(data, path: str, album= -1):
    # with open("data.json", "r") as file:
    #     data = json.load(file)
    
    if album == -1:
        for j in data:
            if data[j]["name"] == "Songs":
                album = j
                break
        if album == -1:
            raise FileNotFoundError("Songs folder does not exist")
    
    songCount = len(data[album]["songs"])
    audio = eyed3.load(path)
    seconds = int(MP3(path).info.length)
    artist = audio.tag.artist
    name = path[::-1]
    i = name.index("\\")
    name = name[:i][::-1]
    data[album]["songs"][f"{album}.{songCount}"] = {
        "name": name,
        "lenght": seconds,
        "artist": artist
    }
    
    # with open("data.json", "w") as file:
        # json.dump(data, file, indent= 4)

if __name__ == "__main__":
    with open("data.json", "r") as file:
        data = json.load(file)
    addData("MusicAlbums\Master_of_Puppets\Master_of_Puppets.mp3")
    with open("data.json") as file:
        json.dump(data, file, indent= 4)