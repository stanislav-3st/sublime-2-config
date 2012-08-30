#!/usr/bin/env python

import webbrowser
import tempfile
import sys
import SilverCity
import os
import urllib
from SilverCity import LanguageInfo

xhtml_prefix = \
r"""
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>%(title)s</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <link rel="stylesheet" href="%(css)s" />
</head>
<body>
<span class="code_default">
"""

suffix = \
"""
</span>
</body>
</html>
"""

usage = \
"""
Lexer options:
  --generator=perl|python|...  use the indicated html generator
  --css=file                   refer to the indicated css file
  --view                       view the generated file in a browser window
  --title=title                set the title of the HTML document

usage: source2html.py [Lexer options] source [outfile]
   or: source2html.py --list-generators
"""

def collect_options(args):
    switches = {}
    other_args = []
    for arg in args:
        if arg.startswith('--'):
            if arg.find('=') != -1:
                key, value = arg.split('=', 1)
            else:
                key = arg
                value = 1
            switches[key[2:]] = value
        else:
            other_args.append(arg)

    return switches, other_args



def create_generator(source_file_name, generator_name):
    if generator_name:
        return LanguageInfo.find_generator_by_name(generator_name)()
    else:
        return LanguageInfo.guess_language_for_file(
                        source_file_name).get_default_html_generator()()

def generate_html(
        source_file_name,
        target_file_name = None,
        css = '',
        generator = None,
        title = '',
        view = 0,
        prefix = xhtml_prefix,
        suffix = suffix):

    if target_file_name is None:
        if view:
            target_file_name = tempfile.mktemp('.html')
            target_file = open(target_file_name, 'w')
        else:            
            target_file = sys.stdout
    else:
        target_file = open(target_file_name, 'w')

    if not css:
        css = 'file:' + urllib.pathname2url(SilverCity.get_default_stylesheet_location())
        
    generator = create_generator(source_file_name, generator)
    target_file.write(xhtml_prefix % {'title' : title or os.path.basename(source_file_name), 'css' : css})
    source = open(source_file_name, 'r').read()
    generator.generate_html(target_file, source)
    target_file.write(suffix)

    if view:
        target_file.close()
        webbrowser.open(target_file_name)

if __name__ == "__main__":
    args = sys.argv[1:]
    if (args == 0) or ("--help" in args) or ("-help" in args):
        print usage
        sys.exit(0)

    switches, other_args = collect_options(args)
    if switches.has_key('list-generators'):
        lexers = LanguageInfo.get_generator_names_descriptions()
        lexers.sort()
        print "\nGenerator Options:"
        for name, description in lexers:
            print "  --generator=%s (%s)" % (name, description)
        print
        sys.exit(0)
        
    if len(other_args) == 1:
        html_args = { 'source_file_name' : other_args[0] }
    elif len(other_args) == 2:
        source_file_name, target_file_name = other_args
        html_args = { 'source_file_name' : source_file_name,
                      'target_file_name' : target_file_name
                    }

    else:
        print usage
        sys.exit(1)

    html_args.update(switches)
    generate_html(**html_args)