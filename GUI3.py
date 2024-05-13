from tkinter import Tk, IntVar
from tkinter import filedialog
import tkinter.ttk as ttk
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from mutagen.mp3 import MP3
from pygame import mixer
from AlbumLoader1_1 import addAlbum
from AddSong import addSong
from My_widgets import Form
import json
import shutil
import eyed3
from helpingfunctions import addData
from DataLoader import refreshData

#todos
#TODO Make canvas to react on Enter to rename files.
#TODO Make convert function which will convert seconds to minutes
#TODO and seconds or hours, minutes and seconds.

with open("params.json", "r") as file:
    params = json.load(file)

with open("data.json", "r") as file2:
    data: dict[str, dict[str, str | int | dict[str, str | int | None]]] = json.load(file2)
    songsPlaylistTag = ""
    for i in range(len(data)):
        if data[str(i)]["name"] == "Songs":
            songsPlaylistTag = str(i)
            break
settings = {
    
    "playing": False,
    "lastPlaying": ""
}


def changeVal() -> None:
    try:
        val = myTree.selection()[0]
    except IndexError:
        return
    time = myTree.item(val)["values"][1]
    name = myTree.item(val)["values"][0]
    
    if nameEntry.get() == "":
        return
    
    if "." not in val:
        os.rename("MusicAlbums\\" + name, "MusicAlbums\\" + nameEntry.get())
        data[val]["name"] = nameEntry.get()
    else:
        dotIndex = val.index(".")
        folderTag = val[:dotIndex]
        # folderName = myTree.item(val[:dotIndex])["values"][0]
        folderName = data[folderTag]["name"]
        track = "MusicAlbums\\" + folderName + "\\" + str(myTree.item(val)["values"][0])
        track2 = "MusicAlbums\\" + folderName + "\\" + nameEntry.get()
        data[folderTag]["songs"][val]["name"] = nameEntry.get()
        if track == settings["lastPlaying"]:
            pos = mixer.music.get_pos()
            mixer.music.stop()
            mixer.music.unload()
            os.rename("MusicAlbums\\" + folderName + "\\" + str(name) + ".mp3", track2 + ".mp3")
            mixer.music.load(track2 + ".mp3")
            mixer.music.play()
            settings["lastPlaying"] = track2 #TODO Make renamed music file play from stopped time
        else:
            os.rename("MusicAlbums\\" + folderName + "\\" + str(name) + ".mp3", track2 + ".mp3")
    myTree.item(val, values= (nameEntry.get(), time))
    nameEntry.delete(0, "end")


def pauseUnpause() -> None:
    if settings["lastPlaying"] != "":
        if settings["playing"]:
            mixer.music.pause()
            settings["playing"] = False
        else:
            mixer.music.unpause()
            settings["playing"] = True
    return


def startPause() -> None:
    try:
        val = myTree.selection()[0]
    except IndexError:
        pauseUnpause()
        return
    if "." in val:
        dotIndex = val.index(".")
        album = myTree.item(val[:dotIndex])["values"][0]
        track = "MusicAlbums\\" + album + "\\" + str(myTree.item(val)["values"][0])
    else:
        pauseUnpause()
        return
    if settings["lastPlaying"] != track:
        mixer.music.unload()
        if ".mp3" in track:
            mixer.music.load(track)
        else:
            mixer.music.load(track + ".mp3")
        settings["lastPlaying"] = track
        mixer.music.play()
        settings["playing"] = True
    else:
        pauseUnpause()
        

def showMenu() -> None:
    def addFromDevice():
        files = filedialog.askopenfilenames(filetypes= [("MP3 files", "*.mp3")])
        if files == []:
            return
        else:
            for file in files:
                name = file[::-1]
                name = name.replace("(", "_").replace(")", "_")
                name = name[:name.index("/")]
                name = name[::-1]
                track = "MusicAlbums\Songs\\" + name
                shutil.copy(file, track)
                audio = eyed3.load("MusicAlbums\Master_of_Puppets\Master_of_Puppets.mp3")
                songsCount = len(data[songsPlaylistTag]["songs"])
                data[songsPlaylistTag]["songs"][f"{songsPlaylistTag}.{songsCount}"] = {
                    "name": name,
                    "lenght": int(MP3(track).info.length),
                    "artist": audio.tag.artist
                }
                seconds = data[songsPlaylistTag]["songs"][f"{songsPlaylistTag}.{songsCount}"]["lenght"]
                minutes, seconds = divmod(seconds, 60)
                if seconds < 10:
                    seconds = "0" + str(seconds) 
                time = f"{minutes}:{seconds}"
                myTree.insert(songsPlaylistTag, "end", f"{songsPlaylistTag}.{songsCount}", values= (name, time))
        root2.destroy()
        return
                
    
    def makeAddSongWin():
        
        def addingSong(n, r, l):
            nonlocal root2
            path = addSong(name= n, art= r, link= l)
            if path == None:
                return
            songsCount = len(data[songsPlaylistTag]["songs"])
            addData(data, path)
            name = data[songsPlaylistTag]["songs"][f"{songsPlaylistTag}.{songsCount - 1}"]["name"]
            # artist = data[songsPlaylistTag]["songs"][f"{songsPlaylistTag}.{songsCount - 1}"]["artist"]
            seconds = data[songsPlaylistTag]["songs"][f"{songsPlaylistTag}.{songsCount - 1}"]["lenght"]
            minutes, seconds = divmod(seconds, 60)
            if seconds < 10:
                seconds = "0" + str(seconds) 
            time = f"{minutes}:{seconds}"
            myTree.insert(songsPlaylistTag, "end", f"{songsPlaylistTag}.{songsCount}", values= (name, time))
            root2.destroy()
        
        nonlocal root2
        root2.destroy()
        root2 = Tk()
        root2.geometry("300x150")
        nameForm = Form(root2, text= "Name", entryText= "Song name")
        nameForm.place(x= 20, y= 20)
        
        artistForm = Form(root2, text= "Artist", entryText= "Artist name for example metallica")
        artistForm.place(x= 20, y= 50)
        
        linkForm = Form(root2, text= "Link", entryText= "Enter video link of format: https://www.youtube.com")
        linkForm.place(x= 20, y= 80)
        
        addButton2 = ttk.Button(root2, text= "Add", command= lambda: addingSong(n= nameForm.get(), r= artistForm.get(), l= linkForm.get()))
        addButton2.place(x= 120, y= 110)
        
        root2.mainloop()
    
    def makeAddAlbumWin():
        
        def addingAlbum(n, a, d, link):
            nonlocal root2
            addAlbum(albName= n, art= a, delx= d, l= link)
            refreshData()
            myTree.delete(*myTree.get_children())
            setTree()
            root2.destroy()
        
        nonlocal root2
        
        root2.destroy()
        root2 = Tk()
        root2.geometry("300x180")
        nameForm = Form(root2, text= "Name", entryText= "Album name")
        nameForm.place(x= 20, y= 20)

        artistForm = Form(root2, text= "Artist", entryText= "Artist name")
        artistForm.place(x= 20, y= 50)
        
        linkForm = Form(root2, text= "Link", entryText= "Enter link in this format: https://www.youtube.com")
        linkForm.place(x= 20, y= 80)
        
        delx = IntVar()
        deluxeButton = ttk.Checkbutton(root2, variable= delx, text= "Deluxe")
        deluxeButton.place(x= 20, y= 110)
        
        addButton3 = ttk.Button(root2, text= "Add album", command= lambda: addingAlbum(n= nameForm.get(), a= artistForm.get(), d= delx.get(), link= linkForm.get()))
        addButton3.place(x= 120, y= 150)
        
        
        root2.mainloop()
    
    root2 = Tk()
    root2.geometry("150x100")
    root2.title("Select adding")
    root2.resizable(False, False)
    fromDeviceButton = ttk.Button(root2, text= "From device", command= addFromDevice)
    fromDeviceButton.pack()
    
    addSongButton = ttk.Button(root2, text= "Add song", command= makeAddSongWin)
    addSongButton.pack()
    
    addAlbumButton = ttk.Button(root2, text= "Add album", command= makeAddAlbumWin)
    addAlbumButton.pack()

    root2.mainloop()


def newAlbum() -> None:
    os.mkdir(r"MusicAlbums\NewAlbum" + str(params["album.count"]))
    myTree.insert("", "end", str(params["album.count"] - 1), values= ("NewAlbum" + str(params["album.count"]), "00:00"))
    data[str(params["album.count"] - 1)] = {
        "name": "NewAlbum" + str(params["album.count"]),
        "lenght": 0,
        "songs": {}
    }
    selected = myTree.selection()
    for _ in selected:
        myTree.selection_remove(_)
    myTree.selection_add(params["album.count"] - 1)
    params["album.count"] += 1


def addTo() -> None:
    selected = myTree.selection()
    if nameEntry.get() == "":
        return
    for _ in selected:
        try:
            if "." in _:
                dotIndex = _.index(".")
                album = _[:dotIndex]
                albIndex = album
                album = myTree.item(album)["values"][0]
                track = myTree.item(_)["values"][0]
                trackLoc = "MusicAlbums\\" + album + "\\" + track + ".mp3"
                trackDest = "MusicAlbums\\" + nameEntry.get() + "\\" + track + ".mp3"
                for i in range(len(data)):
                    if data[str(i)]["name"] == nameEntry.get():
                        destAlbum = str(i)
                addData(data, trackLoc, album= destAlbum)
                shutil.copyfile(trackLoc, trackDest)
                songsCount = len(data[destAlbum]["songs"])
                name = data[albIndex]["songs"][_]["name"]
                seconds = data[albIndex]["songs"][_]["lenght"]
                minutes, seconds = divmod(seconds, 60)
                if seconds < 10:
                    seconds = "0" + str(seconds) 
                time = f"{minutes}:{seconds}"
                myTree.insert(destAlbum, "end", destAlbum + "." + str(songsCount), values= (name, time))
        except Exception as e:
            print("exception", e)
    nameEntry.delete(0, "end")
            

def saveAll() -> None:
    with open("params.json", "w") as file:
        json.dump(params, file, indent= 4)
    with open("data.json", "w") as file2:
        json.dump(data, file2, indent= 4)
    refreshData()
    root.destroy()


def delete() -> None:
    selected = myTree.selection()
    for _ in selected:
        try:
            if "." in _:
                dotIndex = _.index(".")
                album = _[:dotIndex]
                albumIndex = album
                del data[albumIndex]["songs"][_]
                album = myTree.item(album)["values"][0]
                track = myTree.item(_)["values"][0]
                trackLoc = "MusicAlbums\\" + album + "\\" + track + ".mp3"
                os.remove(trackLoc)
            else:
                album = myTree.item(_)["values"][0]
                shutil.rmtree("MusicAlbums\\" + album)
                params["album.count"] -= 1
                del data[_]
                # print(_)
            myTree.delete(_)
        except Exception as e:
            print("Exception:", e)


root = Tk()
root.geometry("400x480")
root.title("Mp3 manager")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", saveAll)

myFrame = ttk.Frame(root)
myFrame.pack()

treeScroll = ttk.Scrollbar(myFrame)
treeScroll.pack(side= "right", fill= "y")

myTree = ttk.Treeview(myFrame, yscrollcommand= treeScroll.set)
myTree.pack(side= "left")
treeScroll.config(command= myTree.yview)

myTree["columns"] = ("Name", "Time")
myTree.column("#0", width= 0)
myTree.column("Name", width= 200)
myTree.column("Time", width= 100)

myTree.heading("#0")
myTree.heading("Name", text= "Name", anchor= "center")
myTree.heading("Time", text= "Time", anchor= "w")

def setTree():
    # directories = os.listdir("MusicAlbums")
    directories = list(data.keys())
    # print(directories)
    count = 0
    # Setting tree values
    for i in directories:
        total = 0
        myTree.insert("", "end", str(count), values= (data[i]["name"], ""))
        # subdirs = os.listdir("MusicAlbums\\" + i)
        subdirs = list(data[i]["songs"].keys())
        for j in range(len(subdirs)):
            # seconds = int(MP3("MusicAlbums\\" + i + "\\" + subdirs[j]).info.length)
            seconds = data[i]["songs"][subdirs[j]]["lenght"]
            total += seconds
            minutes, seconds = divmod(seconds, 60)
            if seconds < 10:
                seconds = "0" + str(seconds) 
            time = f"{minutes}:{seconds}"
            myTree.insert(str(count), "end", str(count) + "." + str(j), values= (data[i]["songs"][subdirs[j]]["name"][:-4], time))
        minutes, seconds = divmod(total, 60)
        hours, minutes = divmod(minutes, 60)
        if minutes < 10:
            minutes = "0" + str(minutes)
        if seconds < 10:
            seconds = "0" + str(seconds)
        
        myTree.item(count, values= (data[i]["name"], f"{hours}:{minutes}:{seconds}"))
        count += 1

setTree()

myFrame2 = ttk.Frame(root)
myFrame2.pack()
nameEntry = ttk.Entry(myFrame2)
nameEntry.pack(pady= 10)

myButton = ttk.Button(myFrame2, text= "Change name", command= changeVal)
myButton.pack()

separator = ttk.Separator(root, orient= "horizontal")
separator.pack(fill= "x", pady= 5)

myFrame3 = ttk.Frame(root)
myFrame3.pack()

startPauseButton = ttk.Button(myFrame3, text= "Start/Pause", command= startPause)
startPauseButton.pack(pady= 5)

addButton = ttk.Button(myFrame3, text= "Add", command= showMenu)
addButton.pack(pady= 5)

newAlbumButton = ttk.Button(myFrame3, text= "New", command= newAlbum)
newAlbumButton.pack(pady= 5)

addToButton = ttk.Button(myFrame3, text= "Add to", command= addTo)
addToButton.pack(pady= 5)

deleteButton = ttk.Button(myFrame3, text= "Delete", command= delete)
deleteButton.pack()

mixer.init()

root.mainloop()