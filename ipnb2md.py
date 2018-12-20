#!/usr/bin/env python3
import sys
import os
import nbformat


def to_markdown(fname):
    s = ''
    cells = nbformat.read(fname, nbformat.NO_CONVERT)['cells']
    for cell in cells:
        markdown = cell['cell_type'] == 'markdown'
        try:
            slidetype = cell['metadata']['slideshow']['slide_type']
        except KeyError:
            slidetype = 'none'
        s += '\n'
        if markdown:
            s += '\n<!-- {} -->\n'.format(slidetype)
        else:
            s += '\n```\n'
        s += cell['source']
        if not markdown:
            s += '\n```\n'
    return s


usage = """Usage ipnb2md.py Input_Notebook_File
In the output
Following comment lines demarcate markdowncells
<!-- slide|sub-slide|fragment|none -->
Code cells are demarcated by ```
"""
if len(sys.argv) < 2:
    print(usage)
    print("\nNo arguments provided. Exiting ...\n")
    exit()
(dirname, fname) = os.path.split(sys.argv[1].rstrip('\n\r'))
(base, ext) = os.path.splitext(fname)
if ext == '':
    ext = '.ipynb'
notebook_file = base + ext
markdown_file = base + '.md'
markdown_path = os.path.join(dirname, markdown_file)
notebook_path = os.path.join(dirname, notebook_file)
if not os.path.isfile(notebook_path):
    print('File', notebook_path, 'does not exist. Exiting ...\n')
    exit()

with open(markdown_path, 'w', encoding='utf-8') as f:
    print(to_markdown(notebook_path), file=f)
