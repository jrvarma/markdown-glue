#!/usr/bin/env python3
import glob
import os
import sys

tex_clean = (".aux", ".bbl", ".blg", ".brf", ".fot", ".glo", ".gls", ".idx",
             ".ilg", ".ind", ".lof", ".log", ".lot", ".nav", ".out", ".snm",
             ".toc", ".url", ".synctex.gz", ".bcf", ".run.xml", ".vrb")
weave_clean = tex_clean + (".tex", )
ht_clean = (".4ct", ".4og", ".4tc", ".css", ".dvi", ".idv", ".lg", ".tmp",
            ".xref")


def delete_matches(to_delete, verbose=False):
    count = 0
    for file in to_delete:
        if verbose:
            print("Deleting ", file)
        try:
            os.remove(file)
            count += 1
        except (IOError, os.error) as why:
            print("Error in deleting ", file, str(why))
    print(count, 'files deleted')


def find_matches(pattern, ext_list, verbose=True):
    count = 0
    to_delete = []
    for file in glob.glob(pattern):
        if file.endswith(ext_list):
            count += 1
            if verbose:
                print(file)
            to_delete.append(file)
    return (to_delete)


if len(sys.argv) < 2:
    print("No arguments provided. Exiting ...\n")
    exit()
path = sys.argv[1].rstrip('\n\r')
(dirname, fname) = os.path.split(path)
if os.path.exists(path):
    (base, ext) = os.path.splitext(fname)
else:
    print("File " + path + " does not exist. Aborting ...")
    exit()

pattern = os.path.join(dirname, base) + '.*'
if ext.lower() == ".rnw" or ext.lower() == ".plw":
    delete_matches(
        find_matches(
            pattern, weave_clean, verbose=False), verbose=True)
else:
    delete_matches(
        find_matches(
            pattern, tex_clean, verbose=False), verbose=True)
