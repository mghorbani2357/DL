"""setup.py for Morebit"""

__author__ = "Mohsen Ghorbani"
__email__ = "m.ghorbani2357@gmail.com"
__copyright__ = "Copyright 2021, Mohsen Ghorbani"

from setuptools import setup, find_packages
import os
import versioneer

this_dir = os.path.abspath(os.path.dirname(__file__))

REQUIREMENTS = filter(None, open('requirements.txt').read().splitlines())

setup(
    name='dl',
    author=__author__,
    author_email=__email__,
    license="MIT",
    zip_safe=False,
    packages=find_packages(exclude=["tests*"]),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    classifiers=[k for k in open('CLASSIFIERS').read().split('\n') if k],
    install_requires=list(REQUIREMENTS),
    long_description=open('README.md').read() + open('HISTORY.md').read(),
    long_description_content_type='text/markdown',
    description='Advance Download Manager',
)
