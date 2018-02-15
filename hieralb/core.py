'''
Core module for hieralb.

Author: B.D. Roads
'''

import os
import csv
import pandas as pd
from pathlib import Path
import imageio

class Album(object):
    '''
    Class that specifies a hierarchical album.

    The Album class has three primary attributes:
      1. classes: A dictionary specifying the mapping between class ID's and a 
         class label (i.e., a string literal).
      
      2. class_class: A dictionary capturing the hierarchical relationships
         between the stimuli as a dictionary that specifies a map between a
         child class ID and a parent class ID.
      
      3. stimuli: A Pandas DataFrame that has a row for each unique stimulus.
         The DataFrame includes the following columns:
           a) stimulus_id
           c) leaf_class_id
           c) path    

    In addition, the Album class has the following additional attributes:
      - album_path
      - n_stimuli
      - n_class
      - has_image_files
      - image_files
    
    Actual image files can be loaded into the Album object by calling the 
    attach_image_files method.
    '''

    def __init__(self, album_path):

        """Initialize"""

        self.album_path = Path(album_path)

        # classes dictionary
        self.classes = self.__load_classes()

        # class_class dictionary
        self.class_class = self.__load_class_class()
        
        # stimuli DataFrame
        image_class0 = pd.read_csv(album_path / Path("image_class0.txt"), 
        header=None, names=('stimulus_id', 'leaf_class_id'), delimiter=' ')
        images = pd.read_csv(album_path / Path("images.txt"), header=None, 
        names=('stimulus_id', 'path'), delimiter=' ')
        stimuli = pd.merge( image_class0, images, on='stimulus_id')
        # Convert path strings to pathlib Path objects
        stimuli['path'] = stimuli['path'].map(lambda x: Path(x))
        self.stimuli = stimuli
        
        self.n_stimuli = len(stimuli)
        self.n_class = len(self.classes.keys())
        self.has_image_files = False
        self.image_files = {}

    def __load_classes(self):
        '''Load classes.txt into a dictionary
        '''
        classes = {}
        with open(self.album_path / Path("classes.txt"), 'r') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                classes[int(row[0])] = row[1]
        return classes

    def __load_class_class(self):
        '''Load class_class.txt into a dictionary
        '''
        class_class = {}
        with open(self.album_path / Path("class_class.txt"), 'r') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                class_class[int(row[0])] = int(row[1])
        return class_class

    def attach_image_files(self):
        '''Load image files into a dictionary
        '''
        image_files = {}
        filenames = self.stimuli.path
        for idx, filename in enumerate(filenames):
            full_path = str(self.album_path / Path('images') / filename)
            image_files[self.stimuli.stimulus_id[idx]] = \
            imageio.imread(full_path)
        self.has_image_files = True
        self.image_files = image_files
