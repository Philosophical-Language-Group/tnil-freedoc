#!/usr/bin/env python3

# Import modules for dealing with the filesystem etc.
from os import path
import os
import sys

# Check for yaml dependency.
try:
    import yaml
except ModuleNotFoundError:
    print("Cannot run without 'yaml' package")

# Check that input & output directories were given.
try:
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
except IndexError:
    print("Supply an input directory and an output directory:")
    print(sys.argv[0] + " <in_dir> <out_dir>")

# These are characters used to underline reST headings.
HEADINGS = '=-^'

# These are characters used to prefix for reST list items.
BULLETS = '-+*'


def cap(s):
    """Capitalize the first letter of a string, preserving the rest.

    Note that str.title() may be more appropriate here; e.g. "Case Scope" rather
    than "Case scope". See
    https://github.com/Ithkuilic-Language-Group/tnil-freedoc/issues/4.
    """
    return s[0].upper() + s[1:]


def rst_heading(heading_level, s):
    """Generate a reST heading.

    The result consists of two lines and is terminated by a newline:
    1. Capitalized version of the string (see cap())
    2. String of the same length consisting of heading characters from HEADINGS;
       the exact character depends on the heading level.
    """
    return cap(s) + "\n" + HEADINGS[heading_level - 1] * len(s)


def rst_bullet(bullet_level, data):
    """Generate a reST list item.

    Indent to the appropriate bullet level and use a bullet character from
    BULLETS depending on the level.
    """
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


def rst_section(heading_level, data, *, include_heading=True):
    """Make a section consisting of an item's heading (optional), description,
    and enumeration of values (and groups, if applicable).
    """
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


def rst_all(heading_level, data, **kwargs):
    """Recursively generate nested reST sections.

    Create a section for a category and a subsection for each value, or (if the
    category has groups) a section for a category, a subsection for each group,
    and a subsubsection for each value.
    """
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


# Iterate over files in input directory.
for file in sorted(os.listdir(in_dir)):
    # Skip the template.
    if file.startswith('_'):
        continue
    # Skip all except *.yaml files.
    if not file.endswith('.yaml'):
        continue
    # Save the full path to the input file.
    in_file = path.join(in_dir, file)
    # Create and format output filename for reST output.
    out_filename = file[:-5].replace('_', '-') + '.rst'
    # Save the path to the output file.
    out_file = path.join(out_dir, out_filename)
    print(f"Making {out_filename}")
    # This will hold the reST content to be written to the file.
    markdown = ''
    # Open the input file.
    with open(in_file) as f:
        # Read the file as YAML.
        category = yaml.load(f, yaml.SafeLoader)
    # If the category has groups, indent one level less and exclude
    # top-level heading since this category will be in its own file.
    if category.get('groups'):
        heading_level = 1
        include_heading = False
    else:
        heading_level = 2
        include_heading = True
    # Write the output.
    with open(out_file, 'w') as f:
        f.write(rst_all(heading_level, category, include_heading=include_heading))
