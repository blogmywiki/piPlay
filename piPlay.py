#!/usr/bin/env python3

from tkinter import *
import time, os, subprocess, datetime

playing = False
trackindex = 0

# returns duration of track in seconds
def getTrackLength(thing):
    bumf = ""
    bumfList = []
    trackLength = ""
    snog = trackArray[thing].replace(' ','\ ')
    foo = "omxplayer -i " + snog

    try:
        bumf = subprocess.check_output(foo, shell=True, stderr=subprocess.STDOUT)
    except Exception as e:
        bumf = str(e.output) # horrible kludge to get round exceptions but capture text
    bumfList = str(bumf).split('\\n')

# does not cope with brackets or ampersands in track filenames and probably crashes if you play anything by Muse
    for line in bumfList:
#        print(line) # debug line
        if line.startswith('  Duration'):
            line_mins = int(line[15:17])
            line_secs = int(line[18:20])
            trackSecs = line_secs + (line_mins*60)

    return trackSecs

# get artist and title metadata
def getMeta(tracknumber):
    bumf = ""
    bumfList = []
    songtitle = ""
    artist = ""
    snog = trackArray[tracknumber].replace(' ','\ ')
    foo = "omxplayer -i " + snog
    try:
        bumf = subprocess.check_output(foo, shell=True, stderr=subprocess.STDOUT)
    except Exception as e:
        bumf = str(e.output) # horrible kludge to get round exceptions but capture text
    bumfList = str(bumf).split('\\n')
    for line in bumfList:
#        print(line) # debug line
        if line.startswith('    artist'):
            artist = line[22:]
        if line.startswith('    title'):
            songtitle = line[22:]
    return artist,songtitle

# returns string with out time in HH:MM:SS format
def getEndTime(tk):
    tkDuration = trackList[tk][2]
    timeNow = str(datetime.datetime.now().time())
    timeHour = timeNow[0:2]
    timeMin = timeNow[3:5]
    timeSec = timeNow[6:8]
    tH = int(timeHour)
    tM = int(timeMin)
    tS = int(timeSec)
    tkS = tkDuration % 60
    tkM = (tkDuration - tkS) / 60
    endSec = int(round(tS+tkS, 0))
    endMin = int(tM + tkM)
    endHour = int(tH)
    if endSec > 59:
        endMin += 1
        endSec = endSec % 60
    if endMin > 59:
        endHour += 1
        endMin = endMin % 60
    endHourString = leadingZero(str(endHour))
    endMinString = leadingZero(str(endMin))
    endSecString = leadingZero(str(endSec))
    endTime = endHourString + ":" + endMinString + ":" + endSecString
    return str(endTime)


# makes strings a fixed length
def colform(txt, width):
    if len(txt) > width:
        txt = txt[:width]
    elif len(txt) < width:
        txt = txt + (" " * (width - len(txt)))
    return txt


# adds a leading 0 to single character strings
def leadingZero(n):
    if len(n) == 1:
            n = '0' + n
    return n

# returns the track length in a string M:SS format
def displayDuration(s):
    disTime = int(s)
    sec = disTime % 60
    m = (disTime - sec)/60
    secString = leadingZero(str(sec))
    minString = str(m)[:-2]
    if len(minString) == 1:
        minString = " " + minString # add leading space to line up longer tracks durations
    t = minString + ":" + secString
    return t

# if no playlist.m3u file found, make one from audio files found in directory
# edit audioFileTypes list to add more file types as needed (but don't add 'aif' because reasons)
if not os.path.exists('playlist.m3u'):
    audioFileTypes = ['.mp3','.MP3','.wav','.WAV','.m4a','.M4A','.aiff','.AIFF','.ogg','.OGG']
    os.system('clear')
    print("No playlist.m3u file found so I am making you one with these files:")
    dirList = os.listdir(".")
    newDir = []
    for x in range(len(dirList)):
        for q in audioFileTypes:
            if q in dirList[x]:
                print(dirList[x])
                newDir.append(dirList[x])
    fo = open("playlist.m3u", "w")
    fo.write("#EXTM3U\n\n")
    for item in newDir:
        fo.write("%s\n" % item)
    fo.close()
    time.sleep(2)

#open the playlist file and read its contents into a list
playlist = open('playlist.m3u')
trackArray = playlist.readlines()

# clean up the track list array of metadata and \n characters
# iterate over list in reverse order as deleting items from list as we go
for i in range(len(trackArray)-1,-1,-1):
    if trackArray[i].startswith('\n') or trackArray[i].startswith('#'):
        trackArray.pop(i)
trackArray.sort()
print(trackArray)

# read tracks into array to hold track info in format:
# filename - display name - duration as float - display duration - (track status not implemented)
trackList = []
for a in range(len(trackArray)):
#    rep = {"\ ": " ", "\\'": "\'", "\&": "&","\(": "(","\)": ")"} # define desired replacements here
    # use these three lines to do the replacement
#    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
#    pattern = re.compile("|".join(rep.keys()))
#    newName = pattern.sub(lambda m: rep[re.escape(m.group(0))], trackArray[a])
#    print a+1,newName
    thisTrackLength = getTrackLength(a)
    trackList.append([trackArray[a][:-1],colform(trackArray[a][:-1],40),thisTrackLength,displayDuration(thisTrackLength)])

print(trackList)

class pyPlayGUI:


    def __init__(self, master):
        self.master = master
        master.title("piPlay 0.2")

        self.label = Label(master, font=("Droid Sans Mono",10), text="          Track                                        |   Dur")
        self.label.grid(row=0, column=0)

        self.tracklistbox = Listbox(master, width=50, height=17, font=("Droid Sans Mono",14), selectmode="single")

        self.scroll = Scrollbar()
        self.scroll.grid(row=1, column=1, rowspan=5, sticky="ns")
        self.scroll.config(command=self.tracklistbox.yview)

        self.tracklistbox.config(yscrollcommand=self.scroll.set)
        self.tracklistbox.grid(row=1, column=0, padx=5, rowspan=5)

        for item in trackList:
            self.tracklistbox.insert("end",item[1]+"   "+item[3])

        self.tracklistbox.select_set(0)

        self.play_button = Button(master, text="PLAY", command=self.play, height=5, width=7, bg="lightgray")
        self.play_button.grid(row=1, column=2, padx=25)

#        self.tracklistbox.bind('<space>',self.play)  DOESN'T WORK - and binding to button requires focus

        self.stop_button = Button(master, text="STOP", command=self.stop, height=5, width=7)
        self.stop_button.grid(row=2, column=2)

        self.pause_button = Button(master, text="PAUSE", command=self.pause, height=5, width=7)
        self.pause_button.grid(row=3, column=2)

        self.skipfwd_button = Button(master, text="30 >", command=self.skipfwd)
        self.skipfwd_button.grid(row=4, column=2)

        self.skipback_button = Button(master, text="< 30", command=self.skipback)
        self.skipback_button.grid(row=5, column=2)

        self.close_button = Button(master, text="Close app", command=self.close)
        self.close_button.grid(row=6, column=0)

        self.nowPlaying = Label(master, text=" \n ")
        self.nowPlaying.grid(row=7, column=0)

        self.outTimeWord = Label(master, text="Out time:")
        self.outTimeWord.grid(row=7, column=2)

        self.outTimeLabel = Label(master, text="        ", font=("Droid Sans Mono",14))
        self.outTimeLabel.grid(row=8, column=2)


    def play(self):
        global playerprocess, trackindex
        global playing
        playing = True
        selection = self.tracklistbox.curselection()
        filename = trackList[selection[0]][0]
        songtitle = getMeta(selection[0])[1]
        artist = getMeta(selection[0])[0]
        self.outTimeLabel.config(text=getEndTime(selection[0]))
        self.nowPlaying.config(text="Now playing: "+filename+ "\nTitle: "+songtitle+"    Artist: "+artist)
        self.play_button.config(bg="lightgreen", activebackground="lightgreen")
        playerprocess = subprocess.Popen(["omxplayer",filename],stdin=subprocess.PIPE)
        trackindex = selection[0]
        self.tracklistbox.select_clear(trackindex)
        self.tracklistbox.itemconfig(trackindex, {'bg':'lightgreen'})
        self.tracklistbox.select_set(trackindex+1)

    def stop(self):
        global playing, trackindex
        if playing:
            playing = False
            self.nowPlaying.config(text=" \n ")
            self.outTimeLabel.config(text="        ")
            self.play_button.config(bg="#D6D6D6",activebackground="#EFEFEF")
            self.tracklistbox.itemconfig(trackindex, {'bg':'white'})
            playerprocess.stdin.write('q'.encode())
            playerprocess.stdin.flush()

    def pause(self):
        global playing
        if playing:
            playerprocess.stdin.write('p'.encode())
            playerprocess.stdin.flush()

    def skipfwd(self):
        global playing
        if playing:
            playerprocess.stdin.write("\027[C".encode())
            playerprocess.stdin.flush()

    def skipback(self):
        global playing
        if playing:
            playerprocess.stdin.write("\027[D".encode())
            playerprocess.stdin.flush()

    def close(self):
        root.destroy()


root = Tk()
root.geometry('720x540')
my_gui = pyPlayGUI(root)



time1 = ''
clock = Label(root, font=('Droid Sans Mono', 36))
clock.grid(row=8, column=0)
def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    clock.after(200, tick)
tick()

playinglabel = Label(root, font=('Droid Sans Mono', 10))
playinglabel.grid(row=6, column=2)
def checkplaying():
    global playerprocess, playing, trackindex
    if playing:
        poll = playerprocess.poll()
        if poll == None:
            playinglabel.config(text="PLAYING", bg="lightgreen")
        else:
            playinglabel.config(text="ready", fg="black")
            my_gui.nowPlaying.config(text=" \n ")   # this is done thrice, remove one?
            my_gui.outTimeLabel.config(text="        ")  # this is done thrice, remove one
            my_gui.play_button.config(bg="#D6D6D6", activebackground="#EFEFEF")
            playing = False
            my_gui.tracklistbox.itemconfig(trackindex, {'bg':'white','fg':'blue'})
            print('track finished playing of its own accord')
    else:
        playinglabel.config(text="-ready-", bg="#D6D6D6")
        my_gui.nowPlaying.config(text=" \n ")   # this is done thrice, remove one
        my_gui.outTimeLabel.config(text="        ")  # this is done thrice, remove one
    playinglabel.after(500, checkplaying)
checkplaying()

root.mainloop()
