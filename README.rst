===========================
Hieralb: Hierarchical Album
===========================

A niche package
---------------
Hieralb is composed of a small set of Python functions that implement a
consistent identification scheme for images used in visual categorization. In
this package, a collection of images is referred to as an *album*. Within an
album, a given image can often be categorized at multiple levels (e.g., bird,
kingfisher, ringed kingfisher) creating a hierarchy of categories. In many
applications, it is desirable to consider these different levels of
categorization. Hieralb enables you to easily generate unique *image IDs* and
*class IDs* for all possible categories. Hieralb generates a set of plain text
files that specify the relationship between the actual images, image IDs and
class IDs. Lastly, Hieralb provides a Python class so that the album's
structural relationships and ID's can easily be used in other Python
applications.

Getting Started
---------------
These instructions provide a guick overview of what you need to do to get
started. More detailed instructions can be found below.

   1. Create a new folder ``<my_album_folder>``.
   2. Create the folder ``images`` inside ``<my_album_folder>``.
   3. Inside ``images``, create appropriately named folders. The folder names will become the literal class names.
   4. Place all of your images in the appropriate folders.
   5. To create the appropriate album files run:``$ python create_album_files.py <my_album_folder> <my_album_prefix>``

Installation
------------
There are two ways to get Hieralb:

   1. Install using pip: ``pip install hieralb``
   2. Clone from Git Hub: https://github.com/roads/hieralb.git

Detailed instructions
---------------------
This file covers the creation and management of domain directories for use in
applications that require organized image databases. The core organization
principle is that an image can be classified at different levels.
Classification levels are modeled using a hierarchical folder structure.

For example, consider an album containing bird images. Let's call this album
birds-9, since there are nine different species. Let us also assume that we want
to capture two different levels of categorization: the *taxonomic family* and
*taxonomic species*. The bird directory might be organized in the following way:

.. code-block:: bash

  birds-9/
  └── bird/
      ├── Parulidae/
      │   ├── Bobolink/
      │   ├── Hooded_Oriole/
      │   └── Scott_Oriole/
      ├── Passeridae/
      │   ├── Hooded_Warbler/
      │   ├── Kentucky_Warbler/
      │   └── Magnolia Warbler/
      └── Icteridae/
          ├── Chipping_Sparrow/
          ├── Fox_Sparrow/
          └── Harris_Sparrow/

After arranging the ``image/`` directory to your satisfaction (with the actual
images placed in the appropriate species folder), you can run:
``$ python create_album_files.py birds-9 10000000``

After running the script, the album directory will contain (at least) the
following three text files:

- classes.txt
   - A file listing all the classes (from all hierarchical levels) along with
     their corresponding class_id.
   - The file is composed of two columns using a space delimeter: <class_id>
     <class_name>
   - The class_id begins at 0 for each album, thus the class ID is not
     unique across albums. The root class in the directory tree is assigned
     class_id 0.
- images.txt
   - A file listing all the images and their corresponding imag_id.
   - The file is composed of two columns using a space delimeter:
     <unqiue_image_id> <image_filename>
   - The unique_image_id is constructed using a numerical prefix supplied by the
     user (e.g., 10000000) which is added to a value starting at 1 (e.g.,
     10000001, 10000002, 10000002, ...). By using a prefix, the unique_image_id
     is unique across albums. Use the prefix "0" if you don't want to use a prefix.
- image_class0.txt
   - A file mapping each image to its finest-grained class.
   - The file is composed of two columns using a space delimeter:
     <unique_image_id> <class_id>
- class_class.txt
   - A file listing the mapping between a child class and its parent class.
   - A file composed of two columns using a space delimeter: <child class_id>
     <parent class_id>

If the ``image/`` directory is more than one level deep (i.e, it contains nested
classes), then additional files will be created. These files will follow the
structure:

- class<n>_class<n+1>.txt
   - A file listing the mapping between a class level n and its parent level n+1.
   - A file composed of two columns using a space delimeter: <child class_id>
     <parent class_id>
   - Level zero starts at the deepest leaf node of the directory tree.

Conventions and assumptions
---------------------------
- Code has only been tested using Python 3
- Folder names should be singular within the “images” folder (e.g., use
bird not birds).
- Use underscore as a placeholder for whitespace (e.g., “Hooded_Warbler”, not
“Hooded Warbler”). Actual spaces can not be used in folder or filenames.
- The depth of each leaf node (from the parent node) must be the same.

Versioning
----------
This package folows the Semantic Versioning 2.0.0 rules (https://semver.org).

Authors
-------
- Brett D. Roads
See also the list of contributors who participated in this project.

License
-------
This project is licensed under the MIT License - see the LICENSE.txt file for details.
