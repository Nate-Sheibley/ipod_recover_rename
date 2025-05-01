# ipod_recover_rename
Unscrambles and sorts mused pulled from ipod hard drives according to song metadata. Album art is seperated into an album art folder.

This has only been tested with .mp3, .m4a, .m4p, .flac, .wav, and .wma files as that is all I have in my library.

# Purpose
When an ipod had music added to it the ipod stores it in F## folders with 4 character strings filenames. 

This script will deconvolute those folders into one base folder, than sort the songs into artist-album-song dir-dir-file heirarchy.

It will move all album art to an album art folder. However, there is not way for me to associate the album art filenames itunes applied with any albums. These image files are named things like "AlbumArt_{55A0EFF2-E31C-43A7-906A-6C8F6CD977FB}_Large" and have no metadata. I am unsure how to approach parsing this.

# Instructions
Copy or move the "Music" folder from the ipod disk into the Music folder in this repo. Files in this folder will not be changed. The structure should be ipod_recover_rename/Music/ + a ton of folders with naming Fxy

Run the reorganize_ipod_songs.py script. 

The After/ directory will contain the reorganized music. 

The "Album Art/" folder will contain any album art


