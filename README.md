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
### All filters
#### image size
    - small       +filterui:imagesize-small
    - medium      +filterui:imagesize-medium
    - large       +filterui:imagesize-large
    - extra_large +filterui:imagesize-wallpaper

#### color 
    - color_only      +filterui:color2-color
    - black_and_white +filterui:color2-bw
    - red             +filterui:color2-FGcls_RED
    - orange          +filterui:color2-FGcls_ORANGE
    - green           +filterui:color2-FGcls_GREEN

#### type 
    - photograph    +filterui:photo-photo
    - clipart       +filterui:photo-clipart
    - line_drawing  +filterui:photo-linedrawing
    - animated_gif  +filterui:photo-animatedgif
    - transparent   +filterui:photo-transparent

#### layout 
    - square  +filterui:aspect-square
    - wide    +filterui:aspect-wide
    - tall    +filterui:aspect-tall

#### people 
    - just_faces          +filterui:face-face
    - head_and_shoulders  +filterui:face-portrait

#### date 
    - past_24_hours +filterui:age-lt1440
    - past_week     +filterui:age-lt10080
    - past_month    +filterui:age-lt43200
    - past_year     +filterui:age-lt525600

#### license
    - all_creative_commons                      +filterui:licenseType-Any
    - public_domain                             +filterui:license-L1
    - free_to_share_and_use                     +filterui:license-L2_L3_L4_L5_L6_L7
    - free_to_share_and_use_commercially        +filterui:license-L2_L3_L4
    - free_to_modify_share_and_use              +filterui:license-L2_L3_L5_L6
    - free_to_modify_share_and_use_commercially +filterui:license-L2_L3
