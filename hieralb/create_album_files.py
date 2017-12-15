#!/usr/bin/python
# coding: utf-8

import os
import sys
import csv
from pathlib import Path

def main():
	# User supplied input
    album_directory = Path(sys.argv[1])
    image_id_prefix = int(sys.argv[2])
    
    # Check if album directory exists.
    if not album_directory.exists():
        raise Exception('The supplied album directory does not exist.')

	# The minimum set of files that will be created.
    classes_filename = "classes.txt"
    images_filename = "images.txt"
    image_class_filename = "image_class0.txt"
    class_class_filename = "class_class.txt"

	# Check if album files already exist.
    do_generate_files = False
    classes_exist = (album_directory / classes_filename).exists()
    images_exist = (album_directory / images_filename).exists()
    image_class_exist = (album_directory / image_class_filename).exists()
    class_class_exist = (album_directory / class_class_filename).exists()

    if classes_exist | images_exist | image_class_exist | class_class_exist:
        print('Some files already exist. Are you sure you would like to continue? Old files will be overwritten. (yes/no)')
        user_response = input()
        if (user_response == 'yes') or (user_response == 'y'):
            print('Generating album files...')
            do_generate_files = True
        else:
            print('Did not generate album files.')
            do_generate_files = False
    else:
        do_generate_files = True

    if do_generate_files:
        album_image_path = album_directory / "images"

        # Curteous print
        print("Album Directory: %s" % album_directory)
        print("Image Directory Path: %s" % album_image_path)
        max_depth_found = determine_max_depth(album_image_path)
        print("Image Directory Depth: %d" % max_depth_found)
        print("Using image ID prefix: %d" % image_id_prefix)

        # Open the required files.
        classes_file = (album_directory / classes_filename).open('w')
        images_file = (album_directory / images_filename).open('w')
        image_class_file = (album_directory / image_class_filename).open('w')
        class_class_file = (album_directory / class_class_filename).open('w')
        
        # Open additional files as required by depth, e.g., open 
        # class1_class0.txt if max_depth_found = 2.
        optional_files = [(album_directory / "class{0}_class{1}.txt".format(x-1, x)).open('w') for x in range(1, max_depth_found)]

        class_id_counter = 0
        image_id_counter = image_id_prefix + 1
        level_counter = [0] * max_depth_found

        start_depth = len(album_image_path.parts)

        for dir_name, subdir_list, file_list in os.walk(str(album_image_path), topdown=True):
            # Found directory
            dir_name = Path(dir_name)
            dir_depth = len(dir_name.parts) - start_depth
            base = dir_name.name
            if not base == 'images':
                # Any directory encountered is a class.
                s = "%d %s\n" % (class_id_counter, base)
                classes_file.write(s)

                level_counter[dir_depth - 1] = class_id_counter
                if (dir_depth - 1) != 0:
                    s = "%d %d\n" % (level_counter[dir_depth - 1], level_counter[dir_depth - 2])
                    class_class_file.write(s)
                    # Handle Optional Levels
                    distance_from_bottom = max_depth_found - dir_depth
                    optional_files[distance_from_bottom].write(s)

                # Files encountered are images
                for fname in file_list:
                    if not fname.startswith('.'):
                        # The image id and the actual image path starting after directory "images"
                        s1 = "%d %s\n" % (image_id_counter, dir_name.relative_to(album_image_path) / fname)
                        images_file.write(s1)
                        # Mapping from image_id to class_id
                        s2 = "%d %d\n" % (image_id_counter, class_id_counter)
                        image_class_file.write(s2)
                        image_id_counter = image_id_counter + 1
                # NOTE: The class counter must be incremented after files examined.
                class_id_counter = class_id_counter + 1

        # Close the required files.
        classes_file.close()
        images_file.close()
        image_class_file.close()
        class_class_file.close()

        # Close any optional files.
        for x in range(1, max_depth_found):
            optional_files[x-1].close()

        print("Successfully wrote:")
        print("\t%s" % classes_filename)
        print("\t%s" % images_filename)
        print("\t%s" % image_class_filename)
        print("\t%s" % class_class_filename)
        for x in range(1, max_depth_found):
            print("\tclass{0}_class{1}.txt".format(x-1, x))    
        print("")

def listdir_nohidden(path):
    '''
    Return non-hidden files.
    '''
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def determine_max_depth(album_path):
    '''
    Return the maximum depth of a directory.
    '''
    max_depth_found = 0
    start_depth = len(album_path.parts)
    for root, dirs, files in os.walk(str(album_path)):
        root = Path(root)
        depth = len(root.parts) - start_depth
        if depth > max_depth_found:
            max_depth_found = depth
    return max_depth_found

if __name__ == "__main__":
    main()
