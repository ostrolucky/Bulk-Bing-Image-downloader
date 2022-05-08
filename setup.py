import setuptools
import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

scripts = glob.glob('*.py') + glob.glob('*/*.py')

setuptools.setup(
    name="bbid",
    version="1.0",
    author="Gabriel Ostrolucký",
    description='Script to download images from Bing search engine',
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
    install_requires=[],
)