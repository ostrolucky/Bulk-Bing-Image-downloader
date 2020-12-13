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
- human readable filters

### Usage
```
bbid.py [-h] [-s SEARCH_STRING] [-f SEARCH_FILE] [-o OUTPUT]
               [--adult-filter-on] [--adult-filter-off] [--filters FILTERS]
               [--limit LIMIT]
```
Or if you would like, you can watch [YouTube tutorial](https://youtu.be/nJ4CixTsYQI)

### Example
`./bbid.py -s "hello world"`

Windows users
`python ./bbid.py -s "hello world"`

### Advanced filtering
You might want to apply some of Bing's filters, such as filter by license, image size, etc. Run the program without any parameters and you will get a list of filter options.

Say, for example, you only want images with the License type of "Public Domain"

--filters License[2]

Or you want public domain clipart

--filters License[2];ImageTypes[2]

- Use the corresponding filter type Sizes, Colors, ImageTypes, Layouts, People, Age and License with the selection in square brackets []
- Each additional filter type should be seperated by only a semicolon ; without spaces as shown in the above example
