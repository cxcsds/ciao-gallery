# Creating Gallery Pages

This `README` explains how to run the `gallery.py` script to
regenerate the gallery `.xml` pages along with (optionally) 
the `.png` files.


## The script `gallery.py`

The `gallery.py` script is used to generate the CIAO gallery pages.

It will 

- (optionally) run each command used to create the 
images to be displayed. 
- (optionally) run `ds9` to create the images and run the
imagemagick `convert` routine to create the thumbnails. 
- creates the `.xml` files for each of the separate gallery 
pages including the `index.html` and `thumbnails.xml` files.
- create scripts that can be used with the SDS regression test
suite, ie the `.MAIN` ksh files.

By default the script will use the config file `gallery.cfg`.
It will always overwrite existing files.

### Examples

The basic usage is

```bash
$ python gallery.py
...
```

This will parse the `gallery.cfg` in the current directory.  It expects
the required input data to be in the `data` sub-directory.  It will write
the output `.xml` files in the current directory and the `.png` files in the
`pngs` sub-directory.

To publish the files you need to copy these files into the directories
used by the publishing scripts:

```bash
$ cp pngs/*png ../pngs
$ cp *xml ../
```

User is responsible for making sure files have appropriate permissions.

There are three command line options

- `--skip-ds9` : do not run ds9 nor convert to create the PNG files.
- `--skip-run` : do not actually run the commands needed to create the output files
- `--infile filename` : use `filename` instead of `gallery.cfg`, useful when writing new examples

So if you want to just regenerate the `xml` files use

```bash
$ python gallery.py --skip-ds9 --skip-run
```


## The config file `gallery.cfg`

The config file is a (***gasp***) Windows `.ini` style config file.
Why?  It's easy to parse and there is not a lot of need to escape
special characters.

Feel free to convert to json or xml or yaml if you wish.

Each section should have the following keys, even if the values are blank:

```
[page.example.name]
title : 
requires : 
commands : 
outfile :
ds9_extras : 
pretext :
posttest : 
```


### `[page.name]` 

The convention is that the section name will be a _dotted_ name
where the first string is used as the page name and section header.

Examples are numbers in the order present in the config file. 

It's recommended that all examples that belong to the same page be
grouped together.

### `requires`

A space separated list of file names that the example assumes/requires already be
present in the input `data` sub-directory before the commands
are run.  

This is also used when making the regression test scripts; it looks
for them in `$CT_INDIR` directory.

### `provides` (not shown)

This is not required and not used, but is present in many of the
`gallery.cfg` examples.

### `commands`

This is a list of the commands to run to generate the outputs
for the example.  You cannot continue an example onto a new-line, ie
trailing back-slash does not work.  

Multi-line commands are supported.  Each command should be complete on a single line of text.
Separate commands are specified with new-lines.  

    Note: Each command is run in a separate subprocess. So 
    you cannot for example set environment variable or
    shell variables since they only exist within the 
    subprocess they were set.  Also things like 
    for loops are discouraged since writing them as a single line is tricky.
    
All commands should have clobber=yes (or equivalent)

If any command fails (exits with non-zero status), the script will
stop.

### `outfile`

The space separated list of output files to display with `ds9`.

The script does not actually check that these files exist and
some example extort this to add additional ds9 command line
arguments interspersed with output file names.


### `ds9_extras`

These are all the ds9 command line arguments needed to setup
the ds9 display.

    Users should clear their ds9 preferences. Things like
    log scale and region formats may affect the outputs.
    
The actual ds9 command will look something like

`ds9 ${outfile} ${ds9_extras} -saveimage png {filename} -exit`


Most of the examples will have either `--geometry %(geom_sqr)s` 
or `--geometry $(geom_wide)s`.  The `geom_sqr` and `geom_wide` are defined in the `[DEFAULT]`
section of the config file and are used like macros.

When generating the text for the `.xml` files, the script will
split ds9 commands longer than 150 characters onto multiple
lines.


### `pretext`

This is `xml` style text that will appear before the example image.
This is the text that describes what the example is going to show
and discuss things like non-default options.

The script does not validate the format of the text.  The pages
have to be published for the syntax of the text to be validated.

### `posttest`

This is `xml` style text that will appear after the example
and various commands.  This describes the results; and for example
in the case of multi-frame images is used to describe the contents 
of the frame.

The script does not validate the format of the text.  The pages
have to be published for the syntax of the text to be validated.

## Tips

The only character that needs to be escaped in the config file is `%`,
ie ten percent is `10%%`.

When writing new examples it can be useful to put them into a separate
config file and use the `--infile filename` option.  This is because you cannot
selectively run the commands, run ds9, nor generate the text for individual
sections or pages.

Multi-line values are supported but the continued value must 
be indented, eg

```
pretext: <p>
    foo
    </p>
``` 

works, but

```
pretext:
<p>
foo
</p>
```

does not.  Preceding white space is stripped by the 
config parser, so things like `<syntax/>` elements work just fine.

