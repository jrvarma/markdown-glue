#!/usr/bin/env python3
# inspired by
# http://stackoverflow.com/questions/23292242/converting-to-not-from-ipython-notebook-format
# and by https://github.com/gatsoulis/py2ipynb
import sys
import os
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook
import re

_encoding_declaration_re = re.compile(r"^#.*coding[:=]\s*([-\w.]+)")


def to_notebook(s):
    s += """
<!-- slide -->
This dummy cell which will be ignored
"""
    lines = s.splitlines()
    cells = []
    cell_lines = []
    state = 'markdowncell'
    slide_re = re.compile("<!-- *(?P<type>slide|subslide|fragment|none)")
    slidetype = "slide"

    for line in lines:
        slide_specifier = slide_re.search(line)
        fence = line.lstrip().startswith('```')
        new_block = slide_specifier or fence
        if new_block:
            if slidetype == 'none':
                metadata = {}
            else:
                metadata = {"slideshow": {"slide_type": slidetype}}
            cell = new_cell(state, cell_lines, metadata)
            if cell is not None:
                cells.append(cell)
            # state = 'markdowncell' if m.group('code') is None else 'codecell'
            if fence and state == 'markdowncell':
                state = 'codecell'
            else:
                state = 'markdowncell'
            if slide_specifier:
                slidetype = slide_specifier.group("type")
            elif cell is None:
                # use preceding slide specifier if no intervening content
                pass
            else:
                # a code block is a fragment unless otherwise specified
                slidetype = "fragment"
            cell_lines = []
        else:
            cell_lines.append(line)
    nb = new_notebook(cells=cells,
                      metadata={'language': 'python', })
    return nb


def new_cell(state, lines, metadata):
    text = '\n'.join(lines)
    text = text.strip('\n')
    if text:
        if state == 'codecell':
            return new_code_cell(source=text, metadata=metadata)
        else:
            return new_markdown_cell(source=text, metadata=metadata)


usage = """Usage md2iynb.py Input_Markdown_File
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
    ext = '.md'
markdown_file = base + ext
notebook_file = base + '.ipynb'
markdown_path = os.path.join(dirname, markdown_file)
notebook_path = os.path.join(dirname, notebook_file)
if not os.path.isfile(markdown_path):
    print('File', markdown_path, 'does not exist. Exiting ...\n')
    exit()

with open(markdown_path, 'r', encoding='utf-8') as f:
    markdown_file_str = f.read()
nb = to_notebook(markdown_file_str
                 .replace('\n# %', '\n%')
                 .replace('\n#%', '\n%'))
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f, version=4)
