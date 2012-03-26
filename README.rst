============
palette-py
============

Image palette detection in Python modelled after Paul Annesley's color
detector in PHP. Palette determines what the most important colors used in
your image are, and if one of them is a background color.

by Dennis Hotson & Lars Yencken

Usage
=====

Palette is meant to run in a streaming manner. You can run it on a single
image by echo'ing the image to palette::

    $ echo myimage.png | palette
    myimage.png #3e453f,#2ea3b7,#bee6ea,#51544c,#373d38 #ffffff

Each input line should be a filename. Each output line will be a tab-delimited
string containing the filename, major colors in order, and (optionally) a
detected background color.

To run on an entire directory tree of images::

  $ find . -name '*.jpg' | palette

Palette has an experimental multiprocessing mode, accessed by the `-n`
argument. For example, to run the same example using 8 processes::

    $ find . -name '*.jpg' | palette -n 8

You can also get usage information for palette by running `palette --help`.

