# This program sorts files into folders according to their extensions.
# To make it work, place the program in the working directory.

import os
import shutil

files = os.listdir(os.getcwd())

list_files = []
set_dirs = set()
for item in files:
    if os.path.isfile(item) and item != __file__.rsplit('/', maxsplit=1)[-1]:
        list_files.append(item)
        set_dirs.add(item.rsplit('.', maxsplit=1)[-1].upper())

for directory in set_dirs:
    if not os.path.exists(directory):
        os.makedirs(directory)

for file in list_files:
    path = file.rsplit('.', maxsplit=1)[-1].upper()
    shutil.move(file, path)
