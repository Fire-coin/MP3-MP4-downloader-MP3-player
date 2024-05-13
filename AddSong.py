from moviepy.editor import *
import urllib.request
import pytube
from re import findall
import os
import json
from helpingfunctions import addData
import re

with open("params.json", "r") as file:
    params = json.load(file)

def addSong(terminal= False, name= "", art= "", link= "") -> str:
    try:
        if link == "":
            vidName = "+".join(input("Enter video name: ").split()) if terminal else "+".join(name.split())

            artist = "+".join(input("Enter artist: ").split()) if terminal else "+".join(art.split())

            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + vidName + artist)
            videoLinks = findall(r"/watch\?v=(\S{11})", html.read().decode())
            ytVideoUrl = "https://www.youtube.com/watch?v=" + videoLinks[0]
        else:
            ytVideoUrl = link
            vidName = "Untitled_Song_No" + str(params["songs"])
            params["songs"] += 1

        yt: pytube.YouTube = pytube.YouTube(ytVideoUrl)
        video = yt.streams.get_highest_resolution()
        vidName = "_".join(vidName.split("+"))
        video.download("VideoAlbums\Videos", filename= vidName + ".mp4")

        videoPath = "VideoAlbums\Videos\\" + vidName + ".mp4"

        video = VideoFileClip(videoPath)
        video.audio.write_audiofile(vidName + ".mp3")
        fileName = vidName + ".mp3"
        os.rename(f"{fileName}", f"MusicAlbums\Songs\{fileName}")
        # addData(f"MusicAlbums\Songs\{fileName}")

        with open("params.json", "w") as file:
            json.dump(params, file, indent= 4)
        return f"MusicAlbums\Songs\{fileName}"
    except:
        print("An error occured please enter link...")

if __name__ == "__main__":
    addSong(terminal= True)