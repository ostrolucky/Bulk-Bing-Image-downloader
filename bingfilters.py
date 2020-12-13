from collections import OrderedDict

"""
Bing filters written by and adapted for BBID by Stephen Genusa
"""

image_size_filters = OrderedDict(
    [('All', ''),
     ('Small', '+filterui:imagesize-small'),
     ('Medium', '+filterui:imagesize-medium'),
     ('Large', '+filterui:imagesize-large'),
     ('Extra Large', '+filterui:imagesize-wallpaper'),
     ('Custom', '+filterui:imagesize-custom_')  # x_y
     ])

image_color_filters = OrderedDict(
    [('All', ''),
     ('Color', '+filterui:color2-color'),
     ('Black and White', '+filterui:color2-bw'),
     ('Red', '+filterui:color2-FGcls_RED'),
     ('Orange', '+filterui:color2-FGcls_ORANGE'),
     ('Yellow', '+filterui:color2-FGcls_YELLOW'),
     ('Green', '+filterui:color2-FGcls_GREEN'),
     ('Teal', '+filterui:color2-FGcls_TEAL'),
     ('Blue', '+filterui:color2-FGcls_BLUE'),
     ('Purple', '+filterui:color2-FGcls_PURPLE'),
     ('Pink', '+filterui:color2-FGcls_PINK'),
     ('Brown', '+filterui:color2-FGcls_BROWN'),
     ('Black', '+filterui:color2-FGcls_BLACK'),
     ('Gray', '+filterui:color2-FGcls_GRAY'),
     ('White', '+filterui:color2-FGcls_WHITE')
     ])

image_type_filters = OrderedDict(
    [('All', ''),
     ('Photograph', '+filterui:photo-photo'),
     ('Clipart', '+filterui:photo-clipart'),
     ('Line Drawing', '+filterui:photo-linedrawing'),
     ('Animated GIF', '+filterui:photo-animatedgif'),
     ('Transparent', '+filterui:photo-transparent')
     ])

image_layout_filters = OrderedDict(
    [('All', ''),
     ('Square', '+filterui:aspect-square'),
     ('Wide', '+filterui:aspect-wide'),
     ('Tall', '+filterui:aspect-tall')
     ])

image_face_filters = OrderedDict(
    [('All', ''),
     ('Just Faces', '+filterui:face-face'),
     ('Head and Shoulders', '+filterui:face-portrait')
     ])

image_age_filters = OrderedDict(
    [('All', ''),
     ('Past 24 Hours', '+filterui:age-lt1440'),
     ('Past Week', '+filterui:age-lt10080'),
     ('Past Month', '+filterui:age-lt43200'),
     ('Past Year', '+filterui:age-lt525600')
     ])

image_license_filters = OrderedDict(
    [('All', ''),
     ('All Create Commons', '+filterui:licenseType-Any'),
     ('Public Domain', '+filterui:license-L1'),
     ('Free to share and use', '+filterui:license-L2_L3_L4_L5_L6_L7'),
     ('Free to share and use commercially', '+filterui:license-L2_L3_L4'),
     ('Free to modify, share, and use', '+filterui:license-L2_L3_L5_L6'),
     ('Free to modify, share, and use commercially', '+filterui:license-L2_L3')
     ])

image_filter_types = OrderedDict(
    [('Sizes', image_size_filters),
     ('Colors', image_color_filters),
     ('ImageTypes', image_type_filters),
     ('Layouts', image_layout_filters),
     ('People', image_face_filters),
     ('Age', image_age_filters),
     ('License', image_license_filters)
     ])


def get_filter_type_help():
    help_text = "\nBing filter parameters\n"
    for filter in image_filter_types:
        help_text += " " * 3 + filter + "\n"
        for idx, key in enumerate(image_filter_types[filter].keys()):
            help_text += " " * 6 + str(idx) + " " + key + "\n"
        help_text += "\n"
        help_text += "Filter Example --filters Sizes[3];ImageTypes[1];License[2]\n"
    return help_text


def parse_filters(filters):
    filters = filters.split(";")
    filter_params = ''
    for filter in filters:
        filter_key = filter.split("[")[0]
        filter_value = int(filter.split("[")[1][0])
        the_filter = image_filter_types[filter_key]
        filter_params += the_filter[list(the_filter)[filter_value]]
    return filter_params
    # print(self.filter_params)
