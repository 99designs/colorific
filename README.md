# colorific

Image palette detection in Python modelled after Paul Annesley's color
detector in PHP. `colorific` determines what the most important colors
used in your image are, and if one of them is a background color.

_by Dennis Hotson & Lars Yencken_

## Usage

`colorific` is meant to run in a streaming manner. You can run it on a single image by echo'ing in the image::

    $ echo myimage.png | colorific
    myimage.png #3e453f,#2ea3b7,#bee6ea,#51544c,#373d38 #ffffff

Each input line should be a filename. Each output line will be a tab-delimited
string containing the filename, major colors in order, and (optionally) a
detected background color.

To run on an entire directory tree of images::

    $ find . -name '*.jpg' | colorific

`colorific` has an experimental multiprocessing mode, accessed by the `-n`
argument. For example, to run the same example using 8 processes::

    $ find . -name '*.jpg' | colorific -p 8

You can also get usage information by running `colorific --help`.

## Example

Here's a concrete example of use. This is the NASA Ares logo:

![NASA Ares Logo](http://media.quietlyamused.org.s3.amazonaws.com/palette/500px-NASA-Ares-logo.svg.png)

Let's run palette detection on it:

    $ echo 500px-NASA-Ares-logo.svg.png | colorific
    500px-NASA-Ares-logo.svg.png  #0065b9,#bbd6ec,#ff0000

These correspond to the colors:

![Ares palette](http://media.quietlyamused.org.s3.amazonaws.com/palette/ares-palette.png)

Note that black and white have been stripped away, and minor colors introduced
through antialiasing are not present.

