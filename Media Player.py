#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import all packages
import pygame
import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from mutagen.mp3 import MP3
import time
import threading
from tkinter import ttk
from ttkthemes import themed_tk as tk

#creating main window
root = tk.ThemedTk()
root.get_themes()
root.set_theme('arc') 

#root window contains status bar, left frame, right frame
#left frame contains playlist, add/del buttons
#right frame contains three more frames i.e. top, middle, bottom

#status bar
statusBar = ttk.Label(root, text='Welcome!', relief=SUNKEN, anchor='w', font='Times 15 italic')
statusBar.pack(side=BOTTOM, fill='x')


#create menubar
menuBar = Menu(root)
root.config(menu=menuBar)

"""Creating Frames"""
#creating right frame
rightFrame = Frame(root)
rightFrame.pack(side=RIGHT, padx=10)

#creating left frame
leftFrame = Frame(root)
leftFrame.pack(side=LEFT, padx=10)

#creating right top frame
topFrame = Frame(rightFrame)
topFrame.pack(pady=30, padx=30)

#creating right middle frame
middleFrame = Frame(rightFrame)
middleFrame.pack(pady=15, padx=30)

#creating right bottom frame
bottomFrame = Frame(rightFrame)
bottomFrame.pack(pady=10)

"""Creating Labels"""
timeLabel = ttk.Label(topFrame, text="Total Length : --:--", font='Ariel 12 bold')
timeLabel.pack()

lengthLabel = ttk.Label(topFrame, text="Remaining Length : --:--", relief=GROOVE, font='Ariel 12')
lengthLabel.pack(pady=5)

#creating listbox
songList = Listbox(leftFrame)
songList.pack()

#active functions
playList = []
def show_details(playSong):    
    file_data = os.path.splitext(playSong)
    if file_data[1] == '.mp3': #if imported file has mp3 format then
        audio = MP3(playSong)
        totalLength = audio.info.length
        
    else: #if imported file has wav format then do
        song = pygame.mixer.Sound(playSong)
        totalLength = song.get_length()
    
    mins, secs = divmod(totalLength, 60)
    mins = round(mins)
    secs = round(secs)
    timeFormat = '{:2d}:{:2d}'.format(mins, secs)
    timeLabel['text'] = 'Total Length : '+' '+timeFormat
    t1 = threading.Thread(target=start_count, args=(totalLength, ))# """Running the threads i.e. multithreading"""
    t1.setDaemon(True)
    t1.start() # """Main thread"""
    
#Running the time length count
def start_count(t):
    global paused
    """pygame.mixer.music.get_busy() returns a false when the music is actively playing"""
    while t:
        if paused:
            continue
        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeFormat = '{:2d}:{:2d}'.format(mins, secs)
            lengthLabel['text'] = 'Remaining Length : '+' '+timeFormat
            time.sleep(1)
            t -= 1
            if pygame.mixer.music.get_busy()==False:
                lengthLabel['text'] = 'Remaining Length : --:--'
                break
                
def play_music():
    global paused #initialize pause variable to False under mixer.init() for desired results
    stop_music()
    time.sleep(1)
    if paused:
        paused = False
        pygame.mixer.music.unpause()
        statusBar['text'] = 'Music Resumed'    
    else:
        try:
            selectedSong = songList.curselection()
            selectedSong = int(selectedSong[0])
            playSong = playList[selectedSong]
            pygame.mixer.music.load(playSong)
            pygame.mixer.music.play()
            statusBar['text']= 'Music Playing'+' - '+os.path.basename(playSong)
            show_details(playSong)
        except Exception:
            tkinter.messagebox.showerror('File not found', "Media Player could'nt find the file, please check again..")
             
def stop_music():
    pygame.mixer.music.stop()
    statusBar['text']= 'Music Stopped'

def pause_music():
    #creating a global variable for the purpose of pause and resume
    global paused
    paused = True
    pygame.mixer.music.pause()
    statusBar['text']= 'Music Paused'    

def rewind_music():
    play_music()
    statusBar['text']= 'Music Rewinded'

def mute_music():
    global muted
    if muted: #if the volume is muted do
        muted = False
        pygame.mixer.music.set_volume(.7)
        scale.set(70)
        muteButton.configure(image=volumePhoto)    
    else: #if the volume is not muted do
        muted = True
        pygame.mixer.music.set_volume(0)
        scale.set(0)
        muteButton.configure(image=mutePhoto)        
        
def set_vol(val):
    volume = float(val)/100 #deviding the value of var/100 because volume scale inputs values from 0.00-1.00
    pygame.mixer.music.set_volume(volume)
    
def about_us():
    tkinter.messagebox.showinfo('Information about player', 'This Applications was created using tkinter')
    
def browse_file():
    global fileName
    fileName = filedialog.askopenfilename()
    add_songs(fileName)

def add_songs(f):
    global fileName
    f = os.path.basename(f)
    index = 0
    songList.insert(index, f)
    playList.insert(index, fileName) #playlist for actually playing the song
    index += 1

def del_song():
    selectedSong = songList.curselection()
    selectedSong = int(selectedSong[0])
    songList.delete(selectedSong)
    playList.remove(selectedSong)
    
def on_close():
    pygame.mixer.music.stop()
    root.destroy()
    
    
#create submenu and drop down menu
"""Creating File sub menu"""
subMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='File', menu=subMenu)
subMenu.add_command(label='New File', command=browse_file)
subMenu.add_command(label='Exit', command=root.destroy)

"""Creating Help sub menu"""
subMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='Help', menu=subMenu)
subMenu.add_command(label='About Us', command=about_us)

#Configuring Main Window
root.title('Media Player')
root.iconbitmap('headphones.ico')

#initializing pygame mixer i.e. to operate music command (play, stop, pause etc...)
pygame.mixer.init()
paused = False
muted = False

#Uploading all the required photos
playPhoto = PhotoImage(file="play.png")  
stopPhoto = PhotoImage(file="stop.png") 
pausePhoto = PhotoImage(file="pause.png")
rewindPhoto = PhotoImage(file="rewind.png")
mutePhoto = PhotoImage(file="mute.png")
volumePhoto = PhotoImage(file="volume.png")

#Initializing widgets   
"""play button"""
playButton = ttk.Button(middleFrame, image=playPhoto, command=play_music)
playButton.grid(row=0, column=0, padx=10)
"""stop button"""
stopButton = ttk.Button(middleFrame, image=stopPhoto, command=stop_music)
stopButton.grid(row=0, column=1, padx=10)
"""pause button"""
pauseButton = ttk.Button(middleFrame, image=pausePhoto, command=pause_music)
pauseButton.grid(row=0, column=2, padx=10)
"""rewind button"""
rewindButton = ttk.Button(bottomFrame, image=rewindPhoto, command=rewind_music)
rewindButton.grid(row=0, column=0, padx=10)
"""rewind button"""
muteButton = ttk.Button(bottomFrame, image=volumePhoto, command=mute_music)
muteButton.grid(row=0, column=1, padx=10)
"""add Song button"""
addButton = ttk.Button(leftFrame, text='+ADD', command=browse_file)
addButton.pack(side=LEFT)
"""delete Song button"""
delButton = ttk.Button(leftFrame, text='-DEL', command=del_song)
delButton.pack(side=LEFT)
"""volume scale"""
scale = ttk.Scale(bottomFrame, from_=0, to_=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
pygame.mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, padx=10)


#starting the main loop of frames i.e. main window is displayed to the user because of frames
"""root.protocol is used to contact to some event"""
root.protocol('WM_DELETE_WINDOW', on_close) 
root.mainloop()


# In[ ]:




