# -*- coding: utf-8 -*-
#
#  script.py
#  colorific
#

import sys
import optparse

from colorific import config
from colorific.palette import (
    extract_colors, print_colors, save_palette_as_image, color_stream_mt,
    color_stream_st)


class Application(object):
    def __init__(self):
        self.parser = self.create_option_parser()

    def create_option_parser(self):
        usage = '\n'.join([
            "%prog [options]",
            "",
            "Reads a stream of image filenames from stdin, and outputs a ",
            "single line for each containing hex color values."])
        parser = optparse.OptionParser(usage)
        parser.add_option(
            '-p',
            '--parallel',
            action='store',
            dest='n_processes',
            type='int',
            default=config.N_PROCESSES)
        parser.add_option(
            '--min-saturation',
            action='store',
            dest='min_saturation',
            default=config.MIN_SATURATION,
            type='float',
            help="Only keep colors which meet this saturation "
                 "[%.02f]" % config.MIN_SATURATION)
        parser.add_option(
            '--max-colors',
            action='store',
            dest='max_colors',
            type='int',
            default=config.MAX_COLORS,
            help="The maximum number of colors to output per palette "
                 "[%d]" % config.MAX_COLORS)
        parser.add_option(
            '--min-distance',
            action='store',
            dest='min_distance',
            type='float',
            default=config.MIN_DISTANCE,
            help="The minimum distance colors must have to stay separate "
                 "[%.02f]" % config.MIN_DISTANCE)
        parser.add_option(
            '--min-prominence',
            action='store',
            dest='min_prominence',
            type='float',
            default=config.MIN_PROMINENCE,
            help="The minimum proportion of pixels needed to keep a color "
                 "[%.02f]" % config.MIN_PROMINENCE)
        parser.add_option(
            '--n-quantized',
            action='store',
            dest='n_quantized',
            type='int',
            default=config.N_QUANTIZED,
            help="Speed up by reducing the number in the quantizing step "
                 "[%d]" % config.N_QUANTIZED)
        parser.add_option(
            '-o',
            action='store_true',
            dest='save_palette',
            default=False,
            help="Output the palette as an image file")

        return parser

    def run(self):
        argv = sys.argv[1:]
        (options, args) = self.parser.parse_args(argv)

        if args:
            # image filenames were provided as arguments
            for filename in args:
                try:
                    palette = extract_colors(
                        filename,
                        min_saturation=options.min_saturation,
                        min_prominence=options.min_prominence,
                        min_distance=options.min_distance,
                        max_colors=options.max_colors,
                        n_quantized=options.n_quantized)

                except Exception as e:  # TODO: it's too broad exception.
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
                save_palette=options.save_palette)


def main():
    application = Application()
    application.run()


if __name__ == '__main__':
    main()
