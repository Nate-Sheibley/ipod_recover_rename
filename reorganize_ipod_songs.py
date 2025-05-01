#!/usr/bin/env python
# coding: utf-8

import pathlib
import os
import re
import shutil
import logging

from tinytag import TinyTag

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ipod_reorganize.log"),
        logging.StreamHandler()
    ]
)
# Set up logging
logging.info('Starting the script')

# Move all files from music to processing folder
# Takes a destination directory
# Walks through the directory and moves all files to the destination
# https://stackoverflow.com/questions/17547273/flatten-complex-directory-structure-in-python
def move_flatten(destination):
    all_files = []
    first_loop_pass = True
    for root, _dirs, files in os.walk(destination):
        if first_loop_pass:
            first_loop_pass = False
            continue
        for filename in files:
            all_files.append(os.path.join(root, filename))
    for filename in all_files:
        shutil.move(filename, destination)

# move all album art to the album art directory
# Takes a source directory and a destination directory
# Walks through the source directory and moves all image files to the destination
def move_album_art(source, destination):
    image_files = []
    files = os.listdir(source)
    for file in files:
        # Check if the file is an image
        if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
                # If it does, add it to the list
                image_files.append(after_path / file)
    for filename in image_files:
        shutil.move(filename, destination)

# Replcaes characters that would cause errors in directory and file names
# Takes a string and replaces all / and \ with _
# Returns the new string 
def sanitize_string(file_dir_string):
    pattern = r'[/\\]'
    new = re.sub(pattern, "_", file_dir_string)
    return new.strip()

# Read metadata from the file
# Takes a file
# Returns a dictionary with the keys: album, artist, title, file_ext
def parse_metadata(f):
    file_path = after_path / f
    file = TinyTag.get(file_path)

    name_dict = {'album':'', 'artist':'', 'title':'', 'ext': ''}
    artist = file.artist
    album = file.album
    title = file.title
    suffix = file_path.suffix

    for key, val in zip(['artist', 'album', 'title', 'file_ext'],[artist, album, title, suffix]):
        if val is not None:
            name_dict[key] = sanitize_string(val)
        else:
            name_dict[key] = 'Metadata_DNE'
    return name_dict

# Move the file to the directory struture (artist/album/file) and rename it to the song title
# takes a file and the associated parsed metadata dictionary
# returns the new file path
def move_and_rename(file, name_dict):
    # build folder and file paths
    artist_path = after_path / name_dict['artist']
    album_path = artist_path /  name_dict['album']
    title = name_dict['title']
    suffix = name_dict['file_ext']

    # check if album-artist folder paths exist, if not make them.
    # if artist folder DNE, make it
    if not os.path.isdir(artist_path):
        os.mkdir(artist_path)
    # if album folder DNE, make it
    if not os.path.isdir(album_path):
        os.mkdir(album_path)
    # move the song to the album-artist folder and rename it
    renamed_ordered_path = album_path / f'{title}{suffix}'
    shutil.move(after_path / file, renamed_ordered_path)

    return renamed_ordered_path



# Test if the current working directory is the project root
# important for later relative paths
cwd = pathlib.Path.cwd()

logging.info('Current Working Directory is: %s', cwd)

# Check if the script is being run from the correct directory
if cwd.name == 'ipod_recover_rename':
    logging.info('Path is project root')
else:
    logging.warning('Path is not project root')
    logging.error("Recomend navigating to the project root in terminal")
    logging.error("or opening your chosen idea via the command 'code .'")
    raise NameError('Please correct current working directory to the project root')

# Generate relateive path to the music and processing folders
old_path = cwd / "Music"
after_path = cwd / "After"
art_path = cwd / "Album Art"

# Make the after directory if it does not exist
if not os.path.exists(after_path):
    os.makedirs(after_path)

# Make the art directory if it does not exist
if not os.path.exists(art_path):
    os.makedirs(art_path)

# Copy music folder to the after folder so we do not edit the original   
#TODO: Add support for flattened data
    # currently. this and move_flatten() only work if there is folder structure
    # potentially out of scope because ipod has folder structure always
f_list = os.listdir(old_path)
# copies music to after folder for processing of a copy of the music, ensuring no loss
for file in f_list:
    # prevents copying of the hidden files associated with ituns and ipods
    if file.startswith('._'):
        pass
    else:
        shutil.copytree(old_path / file, after_path / file)

# flatten the after directory so there is not folder structure 
# Turn it to loose music files
move_flatten(after_path)

# move the album art to the art directory
move_album_art(after_path, art_path)

walk = list(os.walk(after_path))
for path, _, _ in walk[::]:
    if len(os.listdir(path)) == 0:
        # remove empty directories
        os.removedirs(path)

# TODO: Add support for images as album art links
#   Only dataset I have is already flattened... put them at root?
#   place them manually and test (do not know how ipods would have handled this)
loose_files = os.listdir(after_path)
len_files = len(loose_files)
count = 1
for song_file in loose_files:
    logging.info('working on %s/%s: %s', count, len_files, song_file)
    metadata_dict = parse_metadata(song_file)
    new = move_and_rename(song_file, metadata_dict)
    logging.info('moved and renamed to: %s', new)
    count += 1

logging.info('Finished processing all files')
