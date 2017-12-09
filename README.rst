===========================
Hieralb: Hierarchical Album
===========================

A niche package
---------------
Hieralb is composed of a small set of Python functions that implement a 
consistent identification scheme for images used in visual categorization. In
this package, a collection of images is referred to as an *album*. Within an
album, a given image can often be categorized at multiple levels (e.g., bird, 
kingfisher, ringed kingfisher) creating a hierarchy of images. In many 
applications, it is desirable to consider these different levels of 
categorization. Hieralb enables you to easily generate unique *image IDs* and
*class IDs* for all possible categories. Hieralb generates a set of plain text
files that specify the relationship between the actual images, image IDs and 
class IDs. Lastly, Hieralb provides a Python class so that the album's
structural relationships and ID's can easily be used in other Python
applications. 

Getting Started
---------------

These instructions will get you a copy of the project up and running on your 
local machine for development and testing purposes.

   1. Create a new folder <my_album_folder>.
   2. Create the folder “images” inside <my_album_folder>.
   3. Place domain images, organized using folders with corresponding class names inside the images folder (folder names will become the literal class names).
   4. To create the appropriate domain files run:``$ python create_album_files.py <my_album_folder>``

Installation
------------


Detailed introduction
---------------------
This file covers the creation and management of domain directories for use in 
applications that require organized image databases. The core organization 
principle is that an image can be classified at different levels. 
Classification levels are modeled using a hierarchical folder structure.

For example, consider a domain containing bird images. The bird directory 
might be organized in the following way:

images/-+
	|
	+- bird/ —----+
			|
			+- Parulidae/ -	-+- Bobolink/
			|		 +- Hooded_Oriole/
			|		 +- Scott_Oriole/
			|		
			+- Passeridae/	-+- Hooded_Warbler/
			|		 +- Kentucky_Warbler/
			|		 +- Magnolia Warbler/
			|
			+- Icteridae/ -	-+- Chipping_Sparrow/
					 +- Fox_Sparrow/
					 +- Harris_Sparrow/


===============
 Created Files
===============
Once you run:
    $ python create_album_files.py <my_album_folder>

The domain directory will contain (at least) the following three files:
    - classes.txt
    - images.txt
    - image_class0.txt

If the domain directory is more than one level deep (i.e, it contains nested classes), then additional files will be created. These files will follow the the structure:
    - class<n>_class<n+1>.txt
    

=============
 classes.txt
=============
A file with two columns, with a space delimeter
<class_id> <class_name>
NOTE: The class_id begins at 1 for each domain, thus class id is not unique across domains. The class_name is written with underscores instead of spaces (e.g., Red-Winged_Blackbird). The classes.txt file contains the class names from all hierarchical levels.

============
 images.txt
============
A file with two columns, with a space delimeter
<unqiue_image_id> <image_filename>
NOTE: The unique_image_id is constructed using a unique prefix for each domain (e.g., 10000000) which is added to a value starting at 1 (e.g., 10000001, 10000002, 10000002, ...). By using a prefix, the unique_image_id is unique across domains.

=================
 image_class0.txt
=================
A file with two columns, with a space delimeter. The two columns show the lowest mapping between image_id and class_id
<unique_image_id> <class_id>

=========================
 class<n>_class<n+1>.txt
=========================
A file with two columns, with a space delimeter. The two columns show the mapping between class_id <n> and class_id <n+1>
<class_id> <class_id>

Conventions and assumptions
---------------------------
- Requires Python 3
- Name folders using the singular form within the “images” folder (e.g., use
bird not birds)
- Use underscore as a placeholder for whitespace (e.g., “Hooded_Warbler”, not 
“Hooded Warbler”). No spaces can be used in folder or filenames.
- The depth of each leaf node (from the parent node) must be the same.

Notes
-----
- If deploying images to a server in order to be used in a website, take note of 
the image file sizes. If your application requires multiple images to be loaded
quickly, large image file sizes will increase page loading time.
- Depending on your OS, certain folder names may not be allowed making this
package mostly useless.

Installation
------------

Support
-------

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
