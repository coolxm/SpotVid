import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from PIL import ImageTk
from threading import Thread
from queue import Queue
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests


isOn = False
t1 = []

def dispatch(*args, **kwargs):
    print("ts")

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

##def GUI
#__start def screen__

    root = tk.Tk()
    root.title("Spotify_video_Downloader")
    root.geometry("1500x800")

    #__end def screen__

    def Start():
        q = Queue()
        t1 = Thread(target = dispatch, args = (q, SpUrl, dirname))
        t1.start()
    
    

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