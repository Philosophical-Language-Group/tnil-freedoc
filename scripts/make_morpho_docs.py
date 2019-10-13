#!/usr/bin/env python3
# to deal with the filesystem etc 
from os import path
import os
import sys
# check for yaml dependency
try:
    import yaml
except ModuleNotFoundError:
    print("Cannot run without 'yaml' package")
# check that input & output directories were given
try:
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
except IndexError:
    print("Supply an input directory and an output directory:")
    print(sys.argv[0] + " <in_dir> <out_dir>")
# characters to underline rst headings
HEADINGS = '=-^'
# characters to prefix for rst bullets
BULLETS = '-+*'
# upcase first letter of string
# 
# FYI the string method `title()` will apply title case to a string
# may be more in line with what we want for things like, "case scope"
# and so on
def cap(s):
    """Capitalize the first letter of a string, preserving the rest."""
    return s[0].upper() + s[1:]
# generate an rst heading consisting of 2 lines:
# 1. upcased version of a string
# 2. a string of the same length consisting of appropriate level bullets
def rst_heading(heading_level, s):
    return cap(s) + "\n" + HEADINGS[heading_level - 1] * len(s)
# indent to appropriate level and use the right bullet from BULLETS
def rst_bullet(bullet_level, data):
    ret = "  " * (bullet_level - 1) + BULLETS[bullet_level - 1] + " "
    link = f"`{cap(data['name'])}`_"
    # link = f"{link_file}#{data['name'].replace(' ', '-')}"
    # link_text = f"**{cap(data['name'])}**"
    # if link:
    #     ret += f"[{link_text}]({link})"
    # else:
    #     ret += link_text
    ret += link
    ret += " - "
    ret += f"*{data['brief']}*"
    ret += "\n"
    return ret
# make a section consisting of:
# 1. a heading (optional)
# 2. full description of the item named in heading
# 3. enumeration of values and possibly groups
def rst_section(heading_level, data, *, include_heading=True):
    if include_heading:
        ret = rst_heading(heading_level, data['name'])
        ret += "\n\n"
    else:
        ret = ''
    ret += data['full'].strip()
    values = data.get('values')
    groups = data.get('groups')
    ret += "\n\n"
    if values:
        suffix = '' if data['name'].endswith('s') else 's'
        ret += f"There are {len(values)} {cap(data['name'])}{suffix}"
        if groups:
            ret += f" split into {len(groups)} groups"
        ret += ":"
        ret += "\n\n"
    return ret
# 
def rst_all(heading_level, data, **kwargs):
    ret = rst_section(heading_level, data, **kwargs)
    inners = None
    values = data.get('values')
    if values:
        inners = values
    groups = data.get('groups')
    if groups:
        values_dict = {}
        for value in values:
            values_dict[value['abbr']] = value
        for group in groups:
            group['name'] += f" {data['name']}s"
            group['values'] = list(map(values_dict.get, group['members']))
        inners = groups
    if data.get('values_in_rst') == False:
        inners = None
    if inners:
        for inner in inners:
            ret += rst_bullet(1, inner)
        ret += "\n"
        for inner in inners:
            ret += rst_all(heading_level + 1, inner)
    return ret
# iterate over files in input dir
for file in sorted(os.listdir(in_dir)):
    # skip template
    if file.startswith('_'):
        continue
    # skip all except .yaml files
    if not file.endswith('.yaml'):
        continue
    # save the full path to the input file
    in_file = path.join(in_dir, file)
    # create and format name for rst output
    out_filename = file[:-5].replace('_', '-') + '.rst'
    # save the path to the output file
    out_file = path.join(out_dir, out_filename)
    print(f"Making {out_filename}")
    # hold the produced markdown text
    markdown = ''
    # open the input file
    with open(in_file) as f:
        # read the file as yaml
        category = yaml.load(f, yaml.SafeLoader)
    if category.get('groups'):
        # if category has groups
        # use level indenting
        heading_level = 1
        include_heading = False
    else:
        heading_level = 2
        include_heading = True
    with open(out_file, 'w') as f:
        f.write(rst_all(heading_level, category, include_heading=include_heading))
