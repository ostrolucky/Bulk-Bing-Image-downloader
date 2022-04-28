Bulk Bing Image Downloader
==========================
*Bulk Bing Image Downloader (BBID)* is downloader which:
- downloads full-size images from bing image search results
- is asynchronous -> downloads images super fast
- is crossplatform
- bypasses bing API
- has option to disable adult content filtering
- is written in python 3.
- uses SSL connection

## Installation

```sh
pip install git+https://github.com/FarisHijazi/Bulk-Bing-Image-downloader
```

### Usage
```
usage: bbid.py [-h] [-f] [-o OUTPUT] [-a] [-g] [--filters FILTERS] [--limit LIMIT] [-t THREADS]
               search_string [search_string ...]

Bing image bulk downloader

positional arguments:
  search_string         Keyword to search

optional arguments:
  -h, --help            show this help message and exit
  -f, --search-file     search-string is a path to a file containing search strings line by line
  -o OUTPUT, --output OUTPUT
                        Output directory
  -a, --adult-filter-off
                        Disable adult filter
  -g, --animated-gif    Disable adult filter
  --filters FILTERS     Any query based filters you want to append when searching for images, e.g. +filterui:license-L1  
  --limit LIMIT         Make sure not to search for more than specified amount of images.
  -t THREADS, --threads THREADS
                        Number of threads
```
Or if you would like, you can watch [YouTube tutorial](https://youtu.be/nJ4CixTsYQI)

### Example

(no more need to surround your search with quotes)

`bbid hello world`

### Advanced filtering
You might want to apply some of Bing's filters, such as filter by license, image size, etc.
BBID doesn't expose to you nice, human readable variants of those, but allows you to utilize all filters exposed by Bing website.
All you need to do is apply filters you want via Bing website and copy them from URL. They are located after `&qft=` and before `&`.

For example, when you search for `code` and apply filters `past week` and image size `large`, URL you will see will be
`http://www.bing.com/images/search?sp=-1&pq=code&sc=0-0&sk=&cvid=39A810C4AF314AB6A5A923F4FB6E5282&q=code&qft=+filterui:age-lt10080+filterui:imagesize-large&FORM=IRFLTR`

Filters string you want to extract from this URL is `+filterui:age-lt10080+filterui:imagesize-large`. You can then apply them in BBID with --filters, e.g.
```
bbid code --filters +filterui:age-lt10080+filterui:imagesize-large
```

### Changelog

changes over [original repo](https://github.com/ostrolucky/Bulk-Bing-Image-downloader):
- added ability to install with pip
- now parses all metadata of the images, now the images are saved with the names of the search result as shown in bing
- searching no longer requires quotes or `-s`
  -  before: `bidd -s 'hello world'`
  -  now:....  `bidd hello world` 
