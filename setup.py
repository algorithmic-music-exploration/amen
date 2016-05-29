from setuptools import setup, find_packages

import imp
import os

version = imp.load_source('amen.version', 'amen/version.py')

# Tacky fix to include examples as data files
current_path = os.path.abspath(os.path.dirname(__file__))
example_path = os.path.join(current_path, 'examples')
example_files = os.listdir(example_path)
example_paths = [os.path.join('examples', f) for f in example_files]

setup(
    name='amen',
    version=version.version,
    description='Algorithmic music remixing',
    url='http://github.com/algorithmic-music-exploration/amen',
    download_url='http://github.com/algorithmic-music-exploration/amen/releases',
    packages=find_packages(),
    package_data={'amen': ['example_audio/*.wav']},
    data_files=[('examples', example_paths)],
    classifiers=[
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    keywords='audio music sound',
    license='ISC',
    install_requires=[
        'librosa >= 0.4.3',
        'pandas >= 0.16.0',
        'pysoundfile >= 0.8',
        'six >= 1.10.0',
    ],
)
