# -*- coding: utf-8 -*-
#
#  test_colorific.py
#  palette-detect
#

import unittest
import itertools

import colorific

CORE_COLORS = [
        '#000000', # black
        '#0000ff', # blue
        '#00ff00', # green
        '#ff0000', # red
        '#ffffff', # white
    ]

class ConversionTest(unittest.TestCase):
    def setUp(self):
        self.pairs = [
                ((0, 0, 0), '#000000'),
                ((255, 255, 255), '#ffffff'),
                ((255, 0, 0), '#ff0000'),
                ((0, 255, 0), '#00ff00'),
                ((0, 0, 255), '#0000ff'),
            ]

    def test_hex_to_rgb(self):
        for rgb, hexval in self.pairs:
            self.assertEqual(colorific.hex_to_rgb(hexval), rgb)

    def test_rgb_to_hex(self):
        for rgb, hexval in self.pairs:
            self.assertEqual(colorific.rgb_to_hex(rgb), hexval)

class VisualDistanceTest(unittest.TestCase):
    def test_core_colors(self):
        for c1, c2 in itertools.combinations(CORE_COLORS, 2):
            assert not self.similar(c1, c2)

    def test_apparent_mistakes(self):
        mistakes = [
                ('#f1f1f1', '#f2f2f2'),
                ('#f2f2f2', '#f3f3f3'),
                ('#fafafa', '#fbfbfb'),
                ('#7c7c7c', '#7d7d7d'),
                ('#29abe1', '#29abe2'),
            ]
        for c1, c2 in mistakes:
            assert self.similar(c1, c2)

    def distance(self, c1, c2):
        return colorific.distance(
                colorific.hex_to_rgb(c1),
                colorific.hex_to_rgb(c2),
            )

    def similar(self, c1, c2):
        return self.distance(c1, c2) < colorific.MIN_DISTANCE

def suite():
    return unittest.TestSuite((
        unittest.makeSuite(ConversionTest),
        unittest.makeSuite(VisualDistanceTest),
    ))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=1).run(suite())

