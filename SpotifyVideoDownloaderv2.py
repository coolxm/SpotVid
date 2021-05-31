import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from PIL import ImageTk
import threading
from queue import Queue
from json import load
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch
from pytube import YouTube
import requests
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor


isOn = False
t1 = []
started = False

def dispatch(out_q, URI, dirname, choice):

    ##load in credentials
    try:
        credentials = load(open(requests.get('http://localhost:8080/Oauth')))
        print('went online')
    except Exception:
        credentials = load(open('spotAuth.json'))
        
    client_id = credentials['client_id']
    client_secret = credentials['client_secret']
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
    sp = Spotify(client_credentials_manager=client_credentials_manager)

    out_q.put(ytdError.config(text="connected",fg="green"))

    def download(song, out_q, dirname, choice):
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
        print(song['title'] + f" name = {threading.current_thread().name}")
    ytdError.config(text=" ")
    manCheck.delete(0,'end')

    username = "Test_1"
    playlist_id = URI

    try:
        results = sp.user_playlist(username, playlist_id, 'tracks')
    except Exception:    
        out_q.put(ytdError.config(text="Error, URI not found"))
        return
    
    playlist = []
    for i in range(0, len(results['tracks']['items'])):
        r = results['tracks']['items'][i]['track']
        playlist.append(r)
        out_q.put(DisPlay.insert(i, r['name'] + " " + r['artists'][0]['name']))

    if not (len(playlist) >= 1):
        out_q.put(ytdError.config(text="found playlist empty"))
        return

    downloadlist = []
    def ytsearch(i):
        #define youtube url's
        try:
            YT = YoutubeSearch(playlist[i]['name'] + " " + playlist[i]['artists'][0]['name'], max_results=5).to_dict()
        except Exception:
            return None

        if YT is not None:

            for i in range(0, len(YT), 1):
                splitDur = YT[i]['duration'].split(':')
                durVid = int(splitDur[0]) * 60 + int(splitDur[1])
                durSong = playlist[i]['duration_ms'] // 1000 + 60
                print(splitDur, durVid, durSong)
                if durVid <= durSong:
                    x = i
                    break
            
            if x != None:
                downloadlist.append(YT[int(x)])

            out_q.put(CurrentOp.insert(i, YT[int(x)]['title']))
        
    workers = 10
    with ThreadPoolExecutor(max_workers=workers) as excecutor:
        excecutor.map(ytsearch, range(len(playlist)))

    workers = 10
    with ThreadPoolExecutor(max_workers=workers) as excecutor:
        excecutor.map(download, downloadlist, repeat(q), repeat(dirname), repeat(choice))

    out_q.put(CurrentOp.delete(0, 'end'))
    out_q.put(CurrentOp.insert(0, 'Done'))

    


if __name__ == "__main__":

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
            initialdir='D:/ZE'
            )
        
        if(len(dirname) > 1):
            locationError.config(text=dirname,fg="green")

        else:
            locationError.config(text="Please Choose Folder!!",fg="red")

##def GUI
#__start def screen__

    root = tk.Tk()
    root.title("Spotify_video_Downloader")
    root.geometry("1500x800")

    #__end def screen__
    q = Queue()
    def Start():
        URI = ytdEntry.get()
        choice = ytdchoices.get()
        t1 = threading.Thread(target = dispatch, args = (q, URI, dirname, choice))
        t1.start()
        started = True 
    
    f = 0
    if started == True:
        f = q.get()
    if type(f) == 'function':
        f()


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
    downloadbtn = tk.Button(root,text="Donwload",width=10,bg="red",fg="white",font =("Arial",12, "bold"), command=Start)
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