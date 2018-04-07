# piPlay
A simple Raspberry Pi audio playout system with GUI for radio or theatre. It runs from one Python 3 program on a vanilla Raspberry Pi running Raspbian and requires no other software or libraries to be installed.

# What is it?
It plays audio files. One track at a time. Then stops.
This may not sound like a big deal, but most GUI-front ends for audio players play though a playlist without stopping. If you work in radio or theatre, this is not what you want. You want to play 1 track at a time under your control.

The idea is based entirely on [CoolPlay](http://www.suppertime.co.uk/blogmywiki/2015/04/coolplaymac/), a Windows app which does the same thing far better. CoolPlay was widely used in BBC Radio News a few years ago in BBC World Service and also, I believe, in Radio 1 Newsbeat, Radio 5 Live and some Radio 4  programmes as well. I designed the splash screen for CoolPlay but nothing else.

# How do I use it?
Put this Python 3 program in the same directory as a bunch of audio files and run it. If you don't aldeady have an M3U-format playlist in the folder, it will make one for you with the tracks in alphabetical order. Highlight the track you want to play and press the PLAY button. It will tell you what time it will end if it carries on playing and if there is metadata with artist and tarck title information this appears below the tracklist. Currently playing tracks are highlighted in green, the next track to be played in grey. Tracks that have been played in full turn blue.

# How does it work?
Inside, it is like a sausage. You do not want to know how it works, what it is made of.

# No, really, how does it work?
It is based on [PyPlay](https://github.com/blogmywiki/PyPlay), a command-line Python program I wrote for Mac OS X that does a similar thing. The GUI PiPlay you see here is a cut-and-shunt job and a horrible piece of programming that already needs a re-write from the ground up.

It is a simple GUI-wrapper written using Tkinter for omxplayer. Omxplayer has some advantages: it can play almost any kind of audio file and allows extraction of metadata. But it's slow to start: there will be a short delay between pressing 'play' and the audio starting. I used aplay instead of omxplayer in [my Raspberry Pi cartwall](http://www.suppertime.co.uk/blogmywiki/2018/03/cartwall/) for this reason, but that only supports WAV files.

It scans the folder it's in and makes an M3U-format playlist file if it doesn't find one. It reads the filenames into an array along with the filename padded to a fixed length, its duration in seconds and its duration for display in minutes and seconds format. When you play a track it requests metadata for artist and track title info, but this probably should be part of the array with other track info.

# To-do list
Everything, really.
- Scrollbar on the tracklist. If there are more than 17 tracks, you can scroll down with the arrow keys but there are currently no scrollbars and no indication that other tracks exist off-screen.
- Add keypress controls for play, stop etc.
- GPIO control for play/stop/up/down.
- End preview to play last 5 seconds or so of a track.
- A progress bar. Probably beyond me.
- Some way of re-ordering / editing the playlist. If I can't do drag'n'drop then use up/down buttons?
