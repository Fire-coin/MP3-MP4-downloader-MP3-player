import os
import json
from mutagen.mp3 import MP3
import eyed3

def refreshData():
    data = {}

    directories = os.listdir("MusicAlbums")
    count = 0
    for i in directories:
        i = i.replace("(", "_").replace(")", "_")
        total = 0
        data[str(count)] = {}
        data[str(count)]["name"] = i
        data[str(count)]["lenght"] = 0
        data[str(count)]["songs"] = {}
        subdirs = os.listdir("MusicAlbums\\" + i)
        for j in range(len(subdirs)):
            path = "MusicAlbums\\" + i + "\\" + subdirs[j]
            # print(path)
            seconds = int(MP3(path).info.length)
            audio = eyed3.load(path)
            artist = audio.tag.artist
            data[str(count)]["lenght"] += seconds
            songData = {
                "name": subdirs[j],
                "lenght": seconds,
                "artist": artist
            }
            data[str(count)]["songs"][f"{count}.{j}"] = songData
        count += 1

    with open("data.json", "w") as file:
        json.dump(data, file, indent= 4)

if __name__ == "__main__":
    refreshData()