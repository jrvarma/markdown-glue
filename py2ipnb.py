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
# <markdowncell>
# This dummy cell which will be ignored
"""
    lines = s.splitlines()
    cells = []
    cell_lines = []
    state = u'codecell'
    slide_re = re.compile("cell> *: *(?P<type>slide|sub-slide|fragment)")
    slideshow = slide_re.search(s)
    slidetype = ""

    def metadata():
        if slideshow:
            return {"slideshow": {"slide_type": slidetype}}
        else:
            return {}

    def slidespec(line):
        m = slide_re.search(line)
        if m:
            return m.group("type")
        else:
            return "slide"

    for line in lines:
        if (
                line.startswith(u'# <nbformat>') or
                _encoding_declaration_re.match(line)):
            pass
        elif line.startswith(u'# <codecell>'):
            cell = new_cell(state, cell_lines, metadata())
            if cell is not None:
                cells.append(cell)
            state = u'codecell'
            slidetype = slidespec(line)
            cell_lines = []
        elif line.startswith(u'# <markdowncell>'):
            cell = new_cell(state, cell_lines, metadata())
            if cell is not None:
                cells.append(cell)
            state = u'markdowncell'
            slidetype = slidespec(line)
            cell_lines = []
        else:
            cell_lines.append(line)
    nb = new_notebook(cells=cells,
                      metadata={'language': 'python', })
    return nb


def new_cell(state, lines, metadata):
    if state == u'codecell':
        text = u'\n'.join(lines)
        text = text.strip(u'\n')
        if text:
            return new_code_cell(source=text, metadata=metadata)
    elif state == u'markdowncell':
        text = remove_comments(lines)
        if text:
            return new_markdown_cell(source=text, metadata=metadata)


def remove_comments(lines):
    new_lines = []
    for line in lines:
        if line.startswith(u'#'):
            new_lines.append(line[2:])
        else:
            new_lines.append(line)
    text = u'\n'.join(new_lines)
    text = text.strip(u'\n')
    return text


usage = """Usage py2iynb.py Input_Python_File
Following comment lines in python file demarcate cells
# <codecell>
# <markdowncell> [slide|sub-slide|fragment]
#% ipython magic commands beginning with % (for example %matplotlib inline)
"""
if len(sys.argv) < 2:
    print(usage)
    print("\nNo arguments provided. Exiting ...\n")
    exit()
(dirname, fname) = os.path.split(sys.argv[1].rstrip('\n\r'))
(base, ext) = os.path.splitext(fname)
if ext == '':
    ext = '.py'
python_file = base + ext
notebook_file = base + '.ipynb'
python_path = os.path.join(dirname, python_file)
notebook_path = os.path.join(dirname, notebook_file)
if not os.path.isfile(python_path):
    print('File', python_path, 'does not exist. Exiting ...\n')
    exit()

with open(python_path, 'r', encoding='utf-8') as f:
    python_file_str = f.read()
nb = to_notebook(python_file_str
                 .replace('\n# %', '\n%')
                 .replace('\n#%', '\n%'))
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f, version=4)
