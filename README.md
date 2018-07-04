# spottelbot
Adding missing features to spotify by using a telegram bot

# Reason 

The spotify client has two major weaknesses: 

## 1. No  ist of recently played tracks
There's no way to show the last played  track(s) - instead the recently played _playlists_
(as if that would be hard to remember)  are shown. This is more than annoying - if
spotiy forgets the current title (and it does so regulary, especially when using spotify
connect) there's no built-in way to see at _which_ position in the current playlist 
playback stopped. If you know the playlist by heart, you _may_ remember, but if you
are using relatively new/fresh playlist, it's pure guesswork.

## 2. No bookmarks
Related to the missing list of recenlty played tracks: Suppose you want to interrupt your
current playlist and temporarily switch to something different, say, you're listening
to an audio book and want to perform some workout using your workout playlist. After 
that you want to continue listening to your audio book, but where exactly did you stop?
A bookmark would solve this problem, but there's no such feature in spotify.

Both features have been requested in the past 
([Playhistory, 2014(!)](https://community.spotify.com/t5/Live-Ideas/Mobile-Listening-History-On-Mobile/idi-p/633072),
[Bookmarks, 2016](https://community.spotify.com/t5/Desktop-Windows/How-to-bookmark-a-song-in-an-album-or-playlist/td-p/1535398))
but to the current date, both features has not been added. Oh, there are workarounds
like using last.fm, sending yourself a WhatsApp message with the title you wand to 
"bookmark", but this is ridicolous - I consider both to be *essential* features in 
any player.

Well, to mitigate this there's spottelbot - a telegram bot interacting with spotify so
you always access your recently played tracks or set bookmarks. For example

* /last 5: Will give you 5 recently played tracks
* /last 2-50: Shows you the recently played tracks starting at 2, ending at 50 (max)
* /mark mybookmark 1: sets a bookmark named "mybookmark" with the value of the last played track
* /list: Shows the bookmarks set
* /help: Shows you all available commands

## Installing 
Before using the bot, you have to manually do certain steps, they are described in INSTALL.md


