from youtube_search import YoutubeSearch
import json
import tkinter as tk
from PIL import ImageTk
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tkinter import filedialog as fd
from pytube import YouTube
from threading import Thread
from tkinter import ttk
import requests
from queue import Queue

## global variables
dirname = ""
isOn = False
count = 0
playlist = []
xI = 0

##define functions
def StartSearch(): 
    q = Queue
    t1 = 4
#send search algorithms
def dispatchSearch():
    ytdError.config(text=" ")
    for i in range(len(manCheck.curselection())):
        manCheck.insert(i, " ")
        CurrentOp.insert(i, " ")
    searchSpotify()
    dispatchDownload()

#check lists and download wanted one
def dispatchDownload():
    global count, playlist, dirname, FllI
    choice = ytdchoices.get()

    #loop for every song
    if count + 1 < len(playlist) + 1:
        #search song + artist on YT
        YT = searchYT(playlist[count]['name'] + " " + playlist[count]['artists'][0]['name'])

        if YT is not None:
            x = None
            
            #Find which song you found seems best
            while 1:
                ##WIP -- manCheck
                #insert all titles in the listing
                if isOn:
                    fillManCheck(YT)
                    FllI = 0       
                    #when list is full
                    while True:
                        selection = manCheck.curselection()
                        print(selection)
                        if selection != ():
                            x = selection[0]
                            break                       
                ##end WIP

                ##autocheck -- time
                else: 
                    for i in range(0, len(YT), 1):
                        splitDur = YT[i]['duration'].split(':')
                        durVid = int(splitDur[0]) * 60 + int(splitDur[1])
                        durSong = playlist[count]['duration_ms'] // 1000 + 60
                        print(splitDur, durVid, durSong)
                        if durVid <= durSong:
                            x = i
                            break
                    break
            
            #if a song has been chosen multithread 
            if x != None:   
                Thread(target = download, args = (YT[int(x)], dirname, choice, )).start()
                CurrentOp.insert(count, '\n Downloading... \n' + YT[int(x)]['title'])

        root.after(100,dispatchDownload)
    count += 1

def searchSpotify():
    SpUrl = ytdEntry.get()
    username = "Test_1"
    playlist_id = SpUrl

    try:
        results = sp.user_playlist(username, playlist_id, 'tracks')
    except Exception:
        ytdError.config(text="Error, URI not found")
        
    for i in range(0, len(results['tracks']['items'])):
        r = results['tracks']['items'][i]['track']
        playlist.append(r)
        DisPlay.insert(i, r['name'] + " " + r['artists'][0]['name'])

    if len(playlist) > 0:
        root.after(100, dispatchDownload)

def searchYT(req):
    try:
        results = YoutubeSearch(req, max_results=5).to_dict()
    except Exception:
        return None
    # returns a dictionary

    return results

def fillManCheck(YT):
    FllI = 0
    if manCheck.size() < len(YT) + 2:
        try:
            manCheck.insert(FllI,YT[FllI]['title'])
            FllI += 1
        except Exception:
            return
    root.after(100, fillManCheck)
    

def download(song, dirname, choice):
        url = "https://youtube.com" + song['url_suffix']
        choice = ytdchoices.get()

        if(len(url)>1):
            yt = YouTube(url)
            if(choice == choices[0]):
                select = yt.streams.filter(progressive=True).first()

            elif(choice == choices[1]):
                select = yt.streams.filter(progressive=True,file_extension='mp4').last()

            elif(choice == choices[2]):
                select = yt.streams.filter(only_audio=True).first()
        
        select.download(dirname)
    

#tkinter functions
def switch():
    global isOn
    if isOn:
        Automatic_Toggle.config(image = off)
        isOn = False
    else:
        Automatic_Toggle.config(image = on)
        isOn = True

def select_dir():
    global dirname
    dirname = fd.askdirectory(
        title='download folder',
        initialdir='/'
        )
    
    if(len(dirname) > 1):
        locationError.config(text=dirname,fg="green")

    else:
        locationError.config(text="Please Choose Folder!!",fg="red")


if __name__ == "__main__":

##load in credentials
    try:
        credentials = json.load(open(requests.get('http://localhost:8080/Oauth')))
        print('went online')
    except Exception:
        credentials = json.load(open('spotAuth.json'))
    client_id = credentials['client_id']
    client_secret = credentials['client_secret']
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

##def GUI
#__start def screen__

    root = tk.Tk()
    root.title("Spotify_video_Downloader")
    root.geometry("1500x800")

    #__end def screen__


#define needed screen attributes
    #Ytd Link Label
    SpUrl = tk.StringVar()
    ytdLabel = tk.Label(root,text="Enter Spotify URI",font=("Arial",15))
    ytdLabel.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 0, sticky = "nsew")

    #Entry Box
    ytdEntry = tk.Entry(root,width=50, font=("Arial", 10))
    ytdEntry.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 1, sticky = "nsew")

    #Error Msg
    ytdError = tk.Label(root,text="",fg="red",font=("Arial",10))
    ytdError.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 2,sticky = "nsew")

    #Asking save file label
    saveLabel = tk.Label(root,text="Choose Download Directory",font=("Arial",15,"bold"))
    saveLabel.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 3, sticky = "nsew")

    #btn of save file
    saveEntry = tk.Button(root,width=10,bg="red",fg="white",text="Choose Path", font =("Arial",12, "bold"), command=select_dir)
    saveEntry.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 4, sticky = "nsew")

    #Error Msg location
    locationError = tk.Label(root,text="",fg="red",font=("Arial",10))
    locationError.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 5, sticky = "nsew")

    #Download Quality
    ytdQuality = tk.Label(root,text="Select Quality",font=("Arial",15))
    ytdQuality.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 6, sticky = "nsew")

    #combobox
    choices = ["720p","144p","Only Audio"]
    ytdchoices = ttk.Combobox(root,values=choices, font =("Arial",12, "bold"))
    ytdchoices.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 7, sticky = "nsew")

    #donwload btn
    downloadbtn = tk.Button(root,text="Donwload",width=10,bg="red",fg="white",font =("Arial",12, "bold"), command=StartSearch)
    downloadbtn.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 8, sticky = "nsew")

    SwitchMessage = tk.Label(root,text="Enable Manual Check? (WIP)",fg="black",font=("Arial",15))
    SwitchMessage.grid(pady = 10, column = 1, row = 9, sticky = "nsew")

    on = ImageTk.PhotoImage(file = ("switch-on.jpeg"))
    off = ImageTk.PhotoImage(file = ("switch-off.jpeg"))
    Automatic_Toggle = tk.Button(root, image = off, bd = 0, command = switch)
    Automatic_Toggle.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, sticky = "nsew")

    DisPlay = tk.Listbox(root, width = 60, height = 49)
    ScrollPlay = ttk.Scrollbar(root)
    ScrollPlay.config(command = DisPlay.yview)
    DisPlay.config(yscrollcommand = ScrollPlay.set)
    DisPlay.grid(column = 3, row = 0, sticky = "W", rowspan = 20)
    ScrollPlay.grid(column = 4, row = 0, sticky = "NSE", rowspan = 20)

    CurrentOp = tk.Listbox(root, width = 60, height = 49)
    ScrollOp = ttk.Scrollbar(root)
    ScrollOp.config(command = CurrentOp.yview)
    CurrentOp.config(yscrollcommand = ScrollOp.set)
    CurrentOp.grid(column = 5, row = 0, sticky = "W", rowspan = 20)
    ScrollOp.grid(column = 6, row = 0, sticky = "NSE", rowspan = 20)

    manCheck = tk.Listbox(root, width = 50, height = 49, selectmode = 'SINGLE')
    ScrollCheck = ttk.Scrollbar(root)
    ScrollCheck.config(command = manCheck.yview)
    manCheck.config(yscrollcommand = ScrollCheck.set)
    manCheck.grid(column = 7, row = 0, sticky = "W", rowspan = 20)
    ScrollCheck.grid(column = 8, row = 0, sticky = "NSE", rowspan = 20)

    tk.mainloop()
##end