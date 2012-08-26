#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  palette.py
#  palette_detect
#

"""
Detect the main colors used in an image.
"""

import sys
import optparse
from collections import Counter, namedtuple
from operator import itemgetter, mul, attrgetter
import multiprocessing
import colorsys

from PIL import Image as Im
from PIL import ImageChops, ImageDraw
from colormath.color_objects import RGBColor

Color = namedtuple('Color', ['value', 'prominence'])
Palette = namedtuple('Palette', 'colors bgcolor')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# algorithm tuning
N_QUANTIZED = 100       # start with an adaptive palette of this size
MIN_DISTANCE = 10.0     # min distance to consider two colors different
MIN_PROMINENCE = 0.01   # ignore if less than this proportion of image
MIN_SATURATION = 0.05   # ignore if not saturated enough
MAX_COLORS = 5          # keep only this many colors
BACKGROUND_PROMINENCE = 0.5     # level of prominence indicating a bg color

# multiprocessing parameters
BLOCK_SIZE = 10
N_PROCESSES = 1
SENTINEL = 'no more to process'

def color_stream_st(istream=sys.stdin, save_palette=False, **kwargs):
    "Read filenames from the input stream and detect their palette."
    for line in istream:
        filename = line.strip()
        try:
            palette = extract_colors(filename, **kwargs)
        except Exception, e:
            print >> sys.stderr, filename, e
            continue

        print_colors(filename, palette)
        if save_palette:
            save_palette_as_image(filename, palette)

def color_stream_mt(istream=sys.stdin, n=N_PROCESSES, **kwargs):
    """
    Read filenames from the input stream and detect their palette using
    multiple processes.
    """
    queue = multiprocessing.Queue(1000)
    lock = multiprocessing.Lock()

    pool = [multiprocessing.Process(target=color_process, args=(queue, lock),
            kwargs=kwargs) for i in xrange(n)]
    for p in pool:
        p.start()

    block = []
    for line in istream:
        block.append(line.strip())
        if len(block) == BLOCK_SIZE:
            queue.put(block)
            block = []
    if block:
        queue.put(block)

    for i in xrange(n):
        queue.put(SENTINEL)

    for p in pool:
        p.join()

def color_process(queue, lock):
    "Receive filenames and get the colors from their images."
    while True:
        block = queue.get()
        if block == SENTINEL:
            break

        for filename in block:
            try:
                palette = extract_colors(filename)
            except:
                continue
            lock.acquire()
            try:
                print_colors(filename, palette)
            finally:
                lock.release()

def distance(c1, c2):
    "Calculate the visual distance between the two colors."
    return RGBColor(*c1).delta_e(RGBColor(*c2), method='cmc')

def rgb_to_hex(color):
    return '#%.02x%.02x%.02x' % color

def hex_to_rgb(color):
    assert color.startswith('#') and len(color) == 7
    return (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))

def extract_colors(filename_or_img, min_saturation=MIN_SATURATION,
        min_distance=MIN_DISTANCE, max_colors=MAX_COLORS,
        min_prominence=MIN_PROMINENCE, n_quantized=N_QUANTIZED):
    """
    Determine what the major colors are in the given image.
    """
    if Im.isImageType(filename_or_img):
        im = filename_or_img
    else:
        im = Im.open(filename_or_img)

    # get point color count
    if im.mode != 'RGB':
        im = im.convert('RGB')
    im = autocrop(im, WHITE) # assume white box
    im = im.convert('P', palette=Im.ADAPTIVE, colors=n_quantized,
            ).convert('RGB')
    data = im.getdata()
    dist = Counter(data)
    n_pixels = mul(*im.size)

    # aggregate colors
    to_canonical = {WHITE: WHITE, BLACK: BLACK}
    aggregated = Counter({WHITE: 0, BLACK: 0})
    sorted_cols = sorted(dist.iteritems(), key=itemgetter(1), reverse=True)
    for c, n in sorted_cols:
        if c in aggregated:
            # exact match!
            aggregated[c] += n
        else:
            d, nearest = min((distance(c, alt), alt) for alt in aggregated)
            if d < min_distance:
                # nearby match
                aggregated[nearest] += n
                to_canonical[c] = nearest
            else:
                # no nearby match
                aggregated[c] = n
                to_canonical[c] = c

    # order by prominence
    colors = sorted((Color(c, n / float(n_pixels)) \
                for (c, n) in aggregated.iteritems()),
            key=attrgetter('prominence'),
            reverse=True)

    colors, bg_color = detect_background(im, colors, to_canonical)

    # keep any color which meets the minimum saturation
    sat_colors = [c for c in colors if meets_min_saturation(c, min_saturation)]
    if bg_color and not meets_min_saturation(bg_color, min_saturation):
        bg_color = None
    if sat_colors:
        colors = sat_colors
    else:
        # keep at least one color
        colors = colors[:1]

    # keep any color within 10% of the majority color
    colors = [c for c in colors if c.prominence >= colors[0].prominence
            * min_prominence][:max_colors]

    return Palette(colors, bg_color)

def norm_color(c):
    r, g, b = c
    return (r/255.0, g/255.0, b/255.0)

def detect_background(im, colors, to_canonical):
    # more then half the image means background
    if colors[0].prominence >= BACKGROUND_PROMINENCE:
        return colors[1:], colors[0]

    # work out the background color
    w, h = im.size
    points = [(0, 0), (0, h/2), (0, h-1), (w/2, h-1), (w-1, h-1),
            (w-1, h/2), (w-1, 0), (w/2, 0)]
    edge_dist = Counter(im.getpixel(p) for p in points)

    (majority_col, majority_count), = edge_dist.most_common(1)
    if majority_count >= 3:
        # we have a background color
        canonical_bg = to_canonical[majority_col]
        bg_color, = [c for c in colors if c.value == canonical_bg]
        colors = [c for c in colors if c.value != canonical_bg]
    else:
        # no background color
        bg_color = None

    return colors, bg_color

def print_colors(filename, palette):
    print '%s\t%s\t%s' % (
            filename,
            ','.join(rgb_to_hex(c.value) for c in palette.colors),
            palette.bgcolor and rgb_to_hex(palette.bgcolor.value) or '',
        )
    sys.stdout.flush()

def save_palette_as_image(filename, palette):
    "Save palette as a PNG with labeled, colored blocks"
    output_filename = '%s_palette.png' % filename[:filename.rfind('.')]
    size = (80 * len(palette.colors), 80)
    im = Im.new('RGB', size)
    draw = ImageDraw.Draw(im)
    for i, c in enumerate(palette.colors):
        (x1, y1) = (i * 80, 0)
        (x2, y2) = ((i + 1) * 80 - 1, 79)
        draw.rectangle([(x1, y1), (x2, y2)], fill=c.value)
        draw.text((x1 + 4, y1 + 4), rgb_to_hex(c.value), (90, 90, 90))
        draw.text((x1 + 3, y1 + 3), rgb_to_hex(c.value))
    im.save(output_filename, "PNG")

def meets_min_saturation(c, threshold):
    return colorsys.rgb_to_hsv(*norm_color(c.value))[1] > threshold

def autocrop(im, bgcolor):
    "Crop away a border of the given background color."
    if im.mode != "RGB":
        im = im.convert("RGB")
    bg = Im.new("RGB", im.size, bgcolor)
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

    return im # no contents, don't crop to nothing

#----------------------------------------------------------------------------#

def _create_option_parser():
    usage = \
"""%prog [options]

Reads a stream of image filenames from stdin, and outputs a single line for
each containing hex color values."""

    parser = optparse.OptionParser(usage)
    parser.add_option('-p', '--parallel', action='store', dest='n_processes',
            type='int', default=N_PROCESSES)
    parser.add_option('--min-saturation', action='store',
            dest='min_saturation', default=MIN_SATURATION, type='float',
            help='Only keep colors which meet this saturation [%.02f]' %
                    MIN_SATURATION)
    parser.add_option('--max-colors', action='store', dest='max_colors',
            type='int', default=MAX_COLORS,
            help='The maximum number of colors to output per palette [%d]' %
                    MAX_COLORS)
    parser.add_option('--min-distance', action='store', dest='min_distance',
            type='float', default=MIN_DISTANCE,
            help='The minimum distance colors must have to stay separate [%.02f]' % MIN_DISTANCE)
    parser.add_option('--min-prominence', action='store',
            dest='min_prominence', type='float', default=MIN_PROMINENCE,
            help='The minimum proportion of pixels needed to keep a color [%.02f]' % MIN_PROMINENCE)
    parser.add_option('--n-quantized', action='store',
            dest='n_quantized', type='int', default=N_QUANTIZED,
            help='Speed up by reducing the number in the quantizing step [%d]' % N_QUANTIZED)
    parser.add_option('-o', action='store_true',
            dest='save_palette', default=False,
            help='Output the palette as an image file')

    return parser

def main():
    argv = sys.argv[1:]
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    if args:
        # image filenames were provided as arguments
        for filename in args:
            try:
                palette = extract_colors(filename,
                                min_saturation=options.min_saturation,
                                min_prominence=options.min_prominence,
                                min_distance=options.min_distance,
                                max_colors=options.max_colors,
                                n_quantized=options.n_quantized)
            except Exception, e:
                print >> sys.stderr, filename, e
                continue
            print_colors(filename, palette)
            if options.save_palette:
                save_palette_as_image(filename, palette)
        sys.exit(1)

    if options.n_processes > 1:
        # XXX add all the knobs we can tune
        color_stream_mt(n=options.n_processes)
    else:
        color_stream_st(
                min_saturation=options.min_saturation,
                min_prominence=options.min_prominence,
                min_distance=options.min_distance,
                max_colors=options.max_colors,
                n_quantized=options.n_quantized,
                save_palette=options.save_palette
            )

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    main()

