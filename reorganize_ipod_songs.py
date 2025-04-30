#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install mutagen tinytag')


# In[1]:


import pathlib
import os
import re

from tinytag import TinyTag

import shutil
import logging


# In[ ]:


cwd = pathlib.Path.cwd()

if cwd.name == 'ipod_recover_rename':
    logging.info('Current Working Directory is:', cwd)
    logging.info('Path is project root')
else:
    logging.info('Current Working Directory is:', cwd)
    logging.warning('Path is not project root')
    logging.error("Recomend navigating to the project root in terminal and opening your chosen idea via the command 'code .'")
    raise NameError('Please correct current working directory to the project root')


# In[4]:


old_path = cwd / "Music"
after_path = cwd / "After"


# In[5]:


if not os.path.exists(after_path): 
    # if the After directory is not present  
    # then create it. 
    os.makedirs(after_path) 


# In[6]:


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



# In[7]:


# https://stackoverflow.com/questions/17547273/flatten-complex-directory-structure-in-python
#Move all files from music to (created) intermediary
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


# In[8]:


move_flatten(after_path)


# In[ ]:


walk = list(os.walk(after_path))
for path, _, _ in walk[::]:
    if len(os.listdir(path)) == 0:
        # remove empty directories
        os.removedirs(path)


# In[ ]:


test_mp3 = after_path / 'CUYL.mp3'
test_m4a = after_path / 'XWHW.m4a'
test_m4p = after_path / 'DMZZ.m4p'
test_flac = after_path / 'ASCS.flac'
test_wav = after_path / 'GSDE.wav'
test_wma = after_path / 'AFES.wma'

test_files = [test_mp3, test_m4a, test_m4p, test_flac, test_wav, test_wma]


# In[ ]:


# Handles names with / \ liek AC/DC 
def sanitize_string(file_dir_string):
    pattern = r'[/\\]'
    new = re.sub(pattern, "_", file_dir_string)
    return new.strip()


# In[ ]:


def parse_metadata(f):
    file_path = after_path / f
    file = TinyTag.get(file_path)

    name_dict = {'album':'', 'artist':'', 'title':'', 'ext': ''}
    artist = file.artist
    album = file.album
    title = file.title
    suffix = file_path.suffix

    for key, val in zip(['artist', 'album', 'title', 'ext'],[artist, album, title, suffix]):
        if val is not None:
            name_dict[key] = sanitize_string(val)
        else:
            name_dict[key] = 'Metadata_DNE'
    return name_dict



# In[ ]:


def move_and_rename(file, name_dict):
    # build folder and file paths
    artist_path = after_path / name_dict['artist']
    album_path = artist_path /  name_dict['album']
    title = name_dict['title']
    suffix = name_dict['ext']
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


# In[ ]:


# TODO: Add support for images as album art links
#   Only dataset I have is already flattened... put them at root?
#   place them manually and test (do not know how ipods would have handled this)
files = os.listdir(after_path)
count = 1
for file in files:
    logging.info(f'working on {count}/{len(files)}: {file}')
    name_dict = parse_metadata(file)
    new = move_and_rename(file, name_dict)
    logging.info('moved and renamed to:', new)
    count += 1


# TODO: 
# 
# 1. rename files to artist_album_title.ext
# 2. Add files to artist-album-song structure
#     1. walk file list and make [artist, album, title.ext]
#     2. check if artist-album folders exist, make them if DNE 
#     3. rename to title.ext and move to appropriate folder tree

# In[ ]:





# In[ ]:




