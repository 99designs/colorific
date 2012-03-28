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

import Image as Im
from colormath.color_objects import RGBColor

import multiprocessing

Color = namedtuple('Color', ['value', 'prominence'])

N_COLORS = 32 # start with an adaptive palette of this size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
THRESHOLD_DIST = 0.2 # max delta-e to merge two colors
SENTINEL = 'no more to process'
BLOCK_SIZE = 10
N_PROCESSES = 1

def color_stream_st(istream=sys.stdin):
    "Read filenames from the input stream and detect their palette."
    for line in istream:
        filename = line.strip()
        try:
            colors, bg_color = extract_colors(filename)
        except Exception, e:
            print >> sys.stderr, filename, e
            continue

        print_colors(filename, colors, bg_color)

def color_stream_mt(istream=sys.stdin, n=N_PROCESSES):
    """
    Read filenames from the input stream and detect their palette using
    multiple processes.
    """
    queue = multiprocessing.Queue(1000)
    lock = multiprocessing.Lock()

    pool = [multiprocessing.Process(target=color_process, args=(queue, lock))
            for i in xrange(n)]
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
                colors, bg_color = extract_colors(filename)
            except:
                continue
            lock.acquire()
            try:
                print_colors(filename, colors, bg_color)
            finally:
                lock.release()

def distance(c1, c2):
    "Calculate the visual distance between the two colors."
    return RGBColor(*c1).delta_e(RGBColor(*c2), method='cmc')

def rgb_to_hex(color):
    return '#%.02x%.02x%.02x' % color

def extract_colors(filename):
    """
    Determine what the major colors are in the given image.
    """
    # get point color count
    im = Im.open(filename)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    im = im.convert('P', palette=Im.ADAPTIVE, colors=N_COLORS).convert('RGB')
    data = im.getdata()
    dist = Counter(data)
    n_pixels = mul(*im.size)

    # aggregate colors
    aggregated = Counter({WHITE: 0, BLACK: 0})
    sorted_cols = sorted(dist.iteritems(), key=itemgetter(1), reverse=True)
    for c, n in sorted_cols:
        if c in aggregated:
            # exact match!
            aggregated[c] += n
        else:
            d, nearest = min((distance(c, alt), alt) for alt in aggregated)
            if d < THRESHOLD_DIST:
                # nearby match
                aggregated[nearest] += n
            else:
                # no nearby match
                aggregated[c] = n

    # order by prominence
    colors = sorted((Color(c, n / float(n_pixels)) \
                for (c, n) in aggregated.iteritems()),
            key=attrgetter('prominence'),
            reverse=True)

    # work out the background color
    corners = [(0, 0), (0, im.size[1]-1), (im.size[0]-1, 0),
            (im.size[0]-1, im.size[1]-1)]
    corner_dist = Counter(im.getpixel(corner) for corner in corners)
    (majority_col, majority_count), = corner_dist.most_common(1)
    if majority_count >= 3:
        # we have a background color
        bg_color, = [c for c in colors if c.value == majority_col]
        colors = [c for c in colors if c.value != majority_col]
    else:
        # no background color
        bg_color = None

    # keep any color within 10% of the majority color
    colors = [c for c in colors if c.prominence >= colors[0].prominence
            / 5.0][:5]

    return colors, bg_color

def print_colors(filename, colors, bg_color):
    colors, bg_color = extract_colors(filename)
    print '%s\t%s\t%s' % (
            filename,
            ','.join(rgb_to_hex(c.value) for c in colors),
            bg_color and rgb_to_hex(bg_color.value) or '',
        )
    sys.stdout.flush()

#----------------------------------------------------------------------------#

def _create_option_parser():
    usage = \
"""%prog [options]

Reads a stream of image filenames from stdin, and outputs a single line for
each containing hex color values."""

    parser = optparse.OptionParser(usage)
    parser.add_option('-p', '--parallel', action='store', dest='n_processes',
            type='int', default=N_PROCESSES)

    return parser

def main():
    argv = sys.argv[1:]
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    if args:
        parser.print_help()
        sys.exit(1)

    if options.n_processes > 1:
        color_stream_mt(n=options.n_processes)
    else:
        color_stream_st()

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    main()

