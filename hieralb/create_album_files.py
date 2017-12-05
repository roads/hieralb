'''
Script to create album files.
'''
#!/usr/bin/python

import os
import sys
import csv
# NOTE: file assumes being called from location of function
# TODO: handle flat directory case
# TODO: if files exist, prompt, and save image_id mapping and class_id mapping
# make scripts command line callable without having to write path

def main():
	# User supplied input
    domain_directory = sys.argv[1]

	# Minimum set of files
    classes_filename = "classes.txt"
    images_filename = "images.txt"
    image_class_filename = "image_class0.txt"
    class_class_filename = "class_class.txt"

	# Check if files already exist
    classes_exist = os.path.isfile(domain_directory + "/" + classes_filename)
    images_exist = os.path.isfile(domain_directory + "/" + images_filename)
    image_class_exist = os.path.isfile(domain_directory + "/" + image_class_filename)

    do_generate = False
    create_conversion_files = True
    if classes_exist | images_exist | image_class_exist:
        print('Some files already exist. Are you sure you would like to continue? (yes/no)')
        # r = raw_input() # Python 2
        r = input()
        if (r == 'yes') or (r == 'y'):
            print('Generating new files')
            do_generate = True
            create_conversion_files = True
        else:
            print('Did not generate new files')
            do_generate = False
            create_conversion_files = False
    else:
        do_generate = True
        create_conversion_files = False

    if do_generate:
        # NOTE: It is important that paths are normalized to correctly determine directory
        # depth
        domain_image_path = domain_directory + "/images"

        # Curteous print
        s = "Domain Directory: %s" % domain_directory
        print(s)
        s = "Image Directory Path: %s" % domain_image_path
        print(s)
        max_depth_found = determine_max_depth(domain_image_path)
        s = "Image Directory Depth: %d" % max_depth_found
        print(s)

		# Image Prefix
        image_id_prefix = 0
        if domain_directory == "birds":
            image_id_prefix = 1000000
        elif domain_directory == "lesions":
            image_id_prefix = 2000000
        elif domain_directory == "rocks_Nosofsky_etal_2016":
            image_id_prefix = 3000000
        else:
            image_id_prefix = 0
        s = "Using Image ID Prefix: %d" % image_id_prefix

        if create_conversion_files:

            old_classes_data = {'class_id' : [], 'class_name' : []}
            with open(domain_directory + "/" + classes_filename, 'r') as f:
                reader = csv.reader(f, delimiter=' ')
                for row in reader:
                    old_classes_data['class_id'].append(row[0])
                    old_classes_data['class_name'].append(row[1])

            old_images_data = {'image_id' : [], 'filename' : []}
            with open(domain_directory + "/" + images_filename, 'r') as f:
                reader = csv.reader(f, delimiter=' ')
                for row in reader:
                    old_images_data['image_id'].append(row[0])
                    old_images_data['filename'].append(row[1])


        # Open a required files
        classes_file = open(domain_directory + "/" + classes_filename, 'w')
        images_file = open(domain_directory + "/" + images_filename, 'w')
        image_class_file = open(domain_directory + "/" + image_class_filename, 'w')
        # Open additional files as required by depth
        # e.g., class1_class0.txt if there is a maxDepth of 2
        optional_files = [open(domain_directory + "/class{0}_class{1}.txt".format(x-1, x),'w') for x in range(1, max_depth_found)]

        class_class_file = open(domain_directory + "/" + class_class_filename, 'w')

        class_id_counter = 0
        image_id_counter = image_id_prefix + 1
        level_counter = [0] * max_depth_found

        start_depth = domain_image_path.count(os.path.sep)

        for dir_name, subdir_list, file_list in os.walk(domain_image_path, topdown=True):
            # Found directory
            dir_depth = dir_name.count(os.path.sep) - start_depth
            base = os.path.basename(os.path.normpath(dir_name))
            if not base == 'images':
                # Any directory encoutered is a class
                s = "%d %s\n" % (class_id_counter, base)
                classes_file.write(s)

                # s = "dir_depth: %d" % (dir_depth - 1)
                # print( s )
                level_counter[dir_depth - 1] = class_id_counter
                # s = "level_counter: %d %d %d" % (level_counter[0], level_counter[1], level_counter[2])
                # print( s )
                if (dir_depth - 1) != 0:
                    s = "%d %d\n" % (level_counter[dir_depth - 1], level_counter[dir_depth - 2])
                    class_class_file.write(s)

                # Handle Optional Levels
                predict_class_id_counter = class_id_counter + 1
                for sname in subdir_list:
                    distance_from_bottom = max_depth_found - dir_depth
                    s = "%d %d\n" % (predict_class_id_counter, class_id_counter)
                    optional_files[distance_from_bottom - 1].write(s)
                    predict_class_id_counter = predict_class_id_counter + 1

                # Files encountered are images
                for fname in file_list:
                    if not fname.startswith('.'):
                        # The image id and the actual image path starting after directory "images"
                        s1 = "%d %s\n" % (image_id_counter, os.path.join(get_last_n_path(dir_name, dir_depth), fname))
                        images_file.write(s1)
                        # Mapping from image_id to class_id
                        s2 = "%d %d\n" % (image_id_counter, class_id_counter)
                        image_class_file.write(s2)
                        image_id_counter = image_id_counter + 1
                # NOTE: class counter must be incremented after files examined
                class_id_counter = class_id_counter + 1

        # Close required files
        classes_file.close()
        images_file.close()
        image_class_file.close()
        # Close any optional files
        for x in range(1, max_depth_found):
            optional_files[x-1].close()

        class_class_file.close()

        print("Successfully wrote:")
        print("\t%s" % classes_filename)
        print("\t%s" % images_filename)
        print("\t%s" % image_class_filename)
        for x in range(1, max_depth_found):
            print("\tclass{0}_class{1}.txt".format(x-1, x))
        print("\t%s" % class_class_filename)
        print("")

def listdir_nohidden(path):
    '''
    List non-hidden files
    '''
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def determine_max_depth(dPath):
    max_depth_found = 0
    start_depth = dPath.count(os.path.sep)
    for root, dirs, files in os.walk(dPath, topdown=True):
        depth = root.count(os.path.sep) - start_depth
        if depth > max_depth_found:
            max_depth_found = depth
    return max_depth_found

def get_last_n_path(dir_name, N):
    completed_path = ''
    for index in range(N):
        completed_path = os.path.join(os.path.split(dir_name)[1], completed_path)
        dir_name = os.path.split(dir_name)[0]
    return completed_path

if __name__ == "__main__":
    main()
