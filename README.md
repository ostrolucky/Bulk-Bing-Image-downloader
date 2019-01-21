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

### Usage
```
bbid.py [-h] [-s SEARCH_STRING] [-f SEARCH_FILE] [-o OUTPUT]
               [--adult-filter-on] [--adult-filter-off] [--filters FILTERS]
               [--limit LIMIT]

```
### Example
`./bbid.py -s "hello world"`

### Advanced filtering
You might want to apply some of Bing's filters, such as filter by license, image size, etc.
BBID doesn't expose to you nice, human readable variants of those, but allows you to utilize all filters exposed by Bing website.
All you need to do is apply filters you want via Bing website and copy them from URL. They are located after `&qft=` and before `&`.

For example, when you search for `code` and apply filters `past week` and image size `large`, URL you will see will be
`http://www.bing.com/images/search?sp=-1&pq=code&sc=0-0&sk=&cvid=39A810C4AF314AB6A5A923F4FB6E5282&q=code&qft=+filterui:age-lt10080+filterui:imagesize-large&FORM=IRFLTR`

Filters string you want to extract from this URL is `+filterui:age-lt10080+filterui:imagesize-large`. You can then apply them in BBID with --filters, e.g.
```
./bbid.py -s code --filters +filterui:age-lt10080+filterui:imagesize-large
```
