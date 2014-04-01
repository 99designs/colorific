colorific
=========

.. image:: https://badge.fury.io/py/colorific.png
    :target: http://badge.fury.io/py/colorific

.. image:: https://travis-ci.org/99designs/colorific.png?branch=master
        :target: https://travis-ci.org/99designs/colorific

.. image:: https://pypip.in/d/colorific/badge.png
        :target: https://crate.io/packages/colorific?version=latest

Image palette detection in Python modelled after Paul Annesley's color detector
in PHP. colorific determines what the most important colors used in your image
are, and if one of them is a background color.

*by Dennis Hotson & Lars Yencken*

Installation
------------

The easiest way to install colorific is with Python's pip and virtualenv::

    $ virtualenv colorific-sandbox
    $ ./colorific-sandbox/bin/pip install colorific

You can then run colorific from ``./colorific-sandbox/bin/colorific``.

Usage
-----

colorific is meant to run in a streaming manner. You can run it on a single image by echo'ing in the image::

    $ echo myimage.png | colorific
    myimage.png #3e453f,#2ea3b7,#bee6ea,#51544c,#373d38 #ffffff

Each input line should be a filename. Each output line will be a tab-delimited string containing the filename, major colors in order, and (optionally) a detected background color.

To run on an entire directory tree of images::

    $ find . -name '*.jpg' | colorific

For a small amount of images, colorific can also be invoked with the image file names provided as arguments::

    $ colorific myimage.png
    myimage.png #3e453f,#2ea3b7,#bee6ea,#51544c,#373d38 #ffffff

You can also get a rendered palette with hex codes for each image with the ``-o`` argument::

    $ colorific -o myimage.png
    myimage.png #3e453f,#2ea3b7,#bee6ea,#51544c,#373d38 #ffffff
    $ ls
    myimage.png  myimage_palette.png

You can use an experimental multiprocessing mode with the ``-n`` argument. For example, to run the same example using 8 processes::

    $ find . -name '*.jpg' | colorific -p 8

You can also get usage information by running ``colorific --help``.

Example
-------

Here's a concrete example of use. This is the NASA Ares logo:

.. image:: http://media.quietlyamused.org.s3.amazonaws.com/palette/500px-NASA-Ares-logo.svg.png

Let's run palette detection on it::

    $ echo 500px-NASA-Ares-logo.svg.png | colorific
    500px-NASA-Ares-logo.svg.png  #0065b9,#bbd6ec,#ff0000

These correspond to the colors:

.. image:: http://media.quietlyamused.org.s3.amazonaws.com/palette/ares-palette.png

Note that black and white have been stripped away, and minor colors introduced
through antialiasing are not present.

Changelog
---------

devel
~~~~~

- Use the recent 1.7.8 Pillow release instead of the master branch
- Pin the colormath to 1.0.9 or earlier, given API changes in newer code

0.2.1
~~~~~

- Project renamed to ``colorific``
- Tuning around quantization and color merging
- Use patched Pillow dependency to avoid segmentation fault bug
- Support for outputting a palette file per image

0.2.0
~~~~~

- Tuning around background color, similarity thresholds for merging, and minimum saturation
- Make an importable module

0.1.0
~~~~~

- Functional palette detection
