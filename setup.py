from setuptools import setup

def readme():
    '''
    Read in README file.
    '''
    with open('README.rst') as f:
        return f.read()

setup(name='hieralb',
      version='0.1.2',
      description='Tools for managing hierarchical albums of images.',
      long_description=readme(),
      url='https://github.com/roads/hieralb',
      classifiers=[
          'Programming Language :: Python :: 3',
      ],
      author='Brett D. Roads',
      author_email='brett.roads@gmail.com',
      license='MIT',
      packages=['hieralb'],
      install_requires=['pandas', 'pathlib', 'imageio'],
      python_requires='>=3',
      include_package_data=True,
      )
