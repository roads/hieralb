'''
Core module for hieralb.
'''
import os
import csv
import numpy as np

class Album(object):
    '''
    Class that specifies the hierarchical album.
    '''

    def __init__(self, album_path):

        """Initialize"""

        self.album_path = os.path.normpath(album_path)

        self.classes = self.__load_classes()
        self.images = self.__load_images()
        self.image_class0 = self.__load_image_class0()
        self.class_class = self.__load_class_class()

        self.n_exemplar = len(self.images.keys())
        self.n_class = len(self.classes.keys())

        #  Optional
        self.has_image_files = False
        self.image_files = {}
        
    def __load_classes(self):
        classes = {}
        with open(self.album_path + "/" + "classes.txt", 'r') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                classes[int(row[0])] = row[1]
        return classes

    def __load_images(self):
        images = {}
        with open(self.album_path + "/" + "images.txt", 'r') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                images[int(row[0])] = row[1]
        return images

    def __load_class_class(self):
        class_class = {}
        with open(self.album_path + "/" + "class_class.txt", 'r') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                class_class[int(row[0])] = int(row[1])
        return class_class

    def __load_image_class0(self):
        image_class0 = {}
        with open(self.album_path + "/" + "image_class0.txt", 'r') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                image_class0[int(row[0])] = int(row[1])
        return image_class0

    def attach_image_files(self):
        has_image_files = False;
        image_files = {}
        # TODO
        self.has_image_files = has_image_files
        self.image_files = image_files

    def get_image_ids(self):
        '''
        Return list of image ids
        '''
        image_ids = []
        for key in self.images:
            image_ids.append(key)
        return image_ids
