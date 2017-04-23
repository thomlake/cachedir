from distutils.core import setup

setup(
    name='cachedir',
    version='0.1.0',
    author='tllake',
    author_email='thom.l.lake@gmail.com',
    packages=['cachedir'],
    install_requires=['filelock'],
    description='Simple file system based caching.',
    long_description=open('README.md').read())