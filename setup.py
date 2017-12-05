from setuptools import setup

def readme():
    '''
    Read in README file.
    '''
    with open('README.rst') as f:
        return f.read()

setup(name='hieralb',
      version='0.1.0',
      description='Tools for managing hierarchical albums of images.',
      long_description=readme(),
      classifiers=[
          'Programming Language :: Python :: 3',
      ],
      author='Brett D. Roads',
      author_email='brett.roads@gmail.com',
      license='MIT',
      packages=['hieralb'],
      include_package_data=True,
      )
