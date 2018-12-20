# markdown-glue

I like to use markdown for everything (see my [blog post](https://jrvcomputing.wordpress.com/2018/12/20/markdown-for-everything/) for the motivation), and so I wrote a set of wrapper or glue scripts to convert to/from markdown using `pandoc`, `pweave`, `jupyter-nbconvert`, and `wkhtmltopdf`. All the hard work is done by these great tools. My scripts only glue them together to do the job quickly and painlessly.

# Prerequisites

* `python` for the `python` scripts `ipnb2md.py`, `md2ipnb.py` and `py2ipnb.py`
and a `unix` shell (say `bash`) for the other scripts `ipnb2pdf`, `md2beamer`, and `pwv-pandoc`. `Windows` power users should not find it hard to convert the shell scripts into `Windows` batch files.

* [`Jupyter`](https://jupyter.org/) with [`nbconvert`](https://github.com/jupyter/nbconvert) and [RISE](https://github.com/damianavila/RISE) for the conversions involving `Jupyter` notebooks.

* [`wkhtmltopdf`](https://wkhtmltopdf.org/) to convert `Jupyter` notebooks to `PDF` slides via `html`.

* [`pandoc`](https://pandoc.org/) and [LaTex](https://www.latex-project.org/) to turn `markdown` into  `PDF` [`beamer`](https://ctan.org/pkg/beamer?lang=en) slides via `LaTex`. If you want to "weave" markdown with embedded python, then you need [`pweave`](http://mpastell.com/pweave/).

# Create `Jupyter-RISE` slides from `markdown`

Write the content using `markdown`, then mark the beginning of slides, subslides and fragments using a comment line with the appropriate keyword:

    <!-- slide|sub-slide|fragment -->

The example file `markdown-file-for-jupyter-notebook-conversion.md` shows how this works. The script `md2ipnb.py` is basically a pre-processor and wrapper around `nbconvert` that turns this file into a `Jupyter-RISE` notebook:

    md2ipnb.py markdown-file-for-jupyter-notebook-conversion.md

will produce `markdown-file-for-jupyter-notebook-conversion.ipynb` which can be run in `Jupyter`.

You can intersperse code cells demarcated by lines containing three backticks

     ```
The example file `markdown-file-with-embedded-python-for-jupyter-notebook-conversion.md` shows how this works. 

# Create `Jupyter-RISE` slides from `python` file interspersed with `markdown` 

If your presentation is mostly `python` code with a bit of `markdown` here and there, it might be easier to start with a `python` file, and intersperse the `markdown` as comments in this file. Following comment lines can be used in the `python` file to demarcate cells:
    
    # <codecell> : [slide|sub-slide|fragment]
    # <markdowncell> : [slide|sub-slide|fragment]
    #% ipython magic commands beginning with % (for example %matplotlib inline)

The advantage is that the entire file is valid `python` code and can be edited and tested in your favourite `python` editor or IDE.

The example file `python-file-with-embedded-markdown-for-jupyter-notebook-conversion.py` shows how this works. The script `py2ipnb.py` is basically a pre-processor and wrapper around `nbconvert` that turns this file into a `Jupyter-RISE` notebook:

    py2ipnb.py python-file-with-embedded-markdown-for-jupyter-notebook-conversion.py

# Convert `Jupyter-RISE` notebooks to `markdown`

The script `ipnb2md.py` uses `nbconvert` and some post-processing to convert a `Jupyter-RISE` notebook to a `markdown` file in a format that `md2ipnb.py` can convert back. Especially useful if you like to keep your presentations as simple text files under version control, and you have pre-existing notebooks or you have edited the content in a running notebook.

# Convert `Jupyter-RISE` notebooks to `PDF` slides

The shell script `ipnb2pdf` uses `nbconvert` to turn a notebook into `html` and then uses `wkhtmltopdf` to turn that into `PDF`. It basically automates the manual process described in the [`RISE` documentation](https://rise.readthedocs.io/en/stable/exportpdf.html).

# `Markdown` to `PDF` slides

If you want to make your presentation using a `PDF` viewer and not a `Jupyter-RISE` notebook, but still want to write everything in `markdown`, then `pandoc` is your friend. The shell script `md2beamer` is a wrapper around `pandoc` and `LaTex` to produce a `PDF` file. For example:

    md2beamer markdown-for-latex-pdf-conversion.md

will produce `markdown-for-latex-pdf-conversion.pdf`

If you want to "weave" the output of `python` code into your `markdown` text using `pweave`, the shell script `pwv-pandoc` gets the job done by running `pweave`, `pandoc` and `latex` in succession:

    pwv-pandoc markdown-with-embedded-python-file-for-latex-pdf-conversion.pmd

