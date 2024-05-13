from moviepy.editor import *
import urllib.request
import pytube
import re
import os
import json

def addAlbum(terminal = False, albName= "", art= "", delx= 0, l= ""):
    def downloadVid(url: str, vidName: str) -> None:
        yt: pytube.YouTube = pytube.YouTube(url)
        video = yt.streams.get_highest_resolution()
        fullName = vidName
        fullName = "_".join(fullName.split())
        video.download("VideoAlbums\\" + albumName, filename= fullName + ".mp4")
        videoPath = "VideoAlbums\\" + albumName + "\\" + fullName + ".mp4"

        video = VideoFileClip(videoPath)
        video.audio.write_audiofile(fullName + ".mp3")
        fileName = fullName + ".mp3"
        os.rename(f"{fileName}", "MusicAlbums\\" + albumName + "\\" + fileName)

    with open("params.json", "r") as file:
        settings = json.load(file)
    if l == "":
        link = 0
    else:
        link = 1
        # link = int(input("Link? yes(1)/no(0): "))
    if link == 0:
        if not terminal:
            albumName = albName
            artist = art
            deluxe = delx
        else:
            albumName = input("Enter album name: ")
            artist = input("Enter artist name: ")
            deluxe = int(input("Deluxe? yes(1)/no(0): "))
        

        html = urllib.request.urlopen("https://www.youtube.com/@" + artist + "/releases")

        pattern = r"playlistId\":\"(\S*)" + albumName + r"(\S{0})"
        albumLink = re.findall(pattern, html.read().decode(), re.IGNORECASE)
        albumLink = list(map(lambda n: n[0][:41], albumLink))

        html = urllib.request.urlopen("https://www.youtube.com/@" + artist + "/releases")

        pattern2 = r"playlistId\":\"(\S*)" + albumName + r"(\S{1})"
        albumLink2 = re.findall(pattern2, html.read().decode(), re.IGNORECASE)
        albumLink2 = list(map(lambda n: n[0][:41], albumLink2))

        if deluxe == 1:
            albumLink.remove(albumLink2[0])
        else:
            albumLink = albumLink2
        playlist = albumLink[0]
        playlistLink = "https://www.youtube.com/playlist?list=" + playlist
    else:
        rawLink = input("Enter link: ") if terminal else l
        albumName = input("Enter album name: ") if terminal else "Untitled_Album_No" + str(settings["album.count"])
        playlistLink = "https://www.youtube.com/playlist?list=" + re.findall(r"list=(\S{41})", rawLink)[0]
    playlisthtml = urllib.request.urlopen(playlistLink)
    videoLinks = list(set(re.findall(r"/watch\?v=(\S{11})", playlisthtml.read().decode())))
    
    settings["album.count"] += 1
    albumName = "_".join(albumName.split())
    os.mkdir("MusicAlbums\\" + albumName)
    os.mkdir("VideoAlbums\\" + albumName)

    for i, vid in enumerate(videoLinks):
        downloadVid("https://www.youtube.com/watch?v=" + vid, str(i + 1))
    # TODO make video title finder
    # for j in videoLinks:   
    #     videohtml = urllib.request.urlopen("https://www.youtube.com/watch?v=" + j)
        # videoTitle = re.findall(r"\"title\":\"([a-zA-Z0-9\s!,-.]+)\"", videohtml.read().decode(), re.IGNORECASE)
        # print(videoTitle)
    with open("params.json", "w") as file:
        json.dump(settings, file, indent= 4)
if __name__ == "__main__":
    addAlbum(terminal= True)