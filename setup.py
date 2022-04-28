import setuptools
from distutils.core import setup
import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    with open("requirements.txt", "r") as fh:
        requirements = list(map(str.strip, filter(None, fh.readlines())))
except:
    requirements = []


scripts = glob.glob('*.py') + glob.glob('*/*.py')

setuptools.setup(
    name="bbid",  # Replace with your own username
    version="1.0",
    author="Gabriel Ostrolucký",
    description='Audio preprocessing script. Splits audio files to segments using subtitle files or on silences.'
                '\nSpecifically for transcribed audio files.'
                '\nThis is a preprocessing step for speech datasets (specifically LibriSpeech).'
                '\nAnd will generate a ".trans.txt" file.'
                '\nGooey GUI is used if it is installed and no arguments are passed.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ostrolucky/Bulk-Bing-Image-downloader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=scripts,
    entry_points={
        'console_scripts': [
            'bbid=bbid.bbid:main',
        ]
    },
    python_requires='>=3',
    install_requires=requirements,
)