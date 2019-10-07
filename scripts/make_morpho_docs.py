#!/usr/bin/env python3

from os import path
import os
import sys


try:
    import yaml
except ModuleNotFoundError:
    print("Cannot run without 'yaml' package")


try:
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
except IndexError:
    print("Supply an input directory and an output directory:")
    print(sys.argv[0] + " <in_dir> <out_dir>")


HEADINGS = '=-^'
BULLETS = '-+*'


def cap(s):
    """Capitalize the first letter of a string, preserving the rest."""
    return s[0].upper() + s[1:]


def rst_heading(heading_level, s):
    return cap(s) + "\n" + HEADINGS[heading_level - 1] * len(s)


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


def rst_section(heading_level, data, *, include_heading=True):
    if include_heading:
        ret = rst_heading(heading_level, data['name'])
        ret += "\n\n"
    else:
        ret = ''
    ret += data['full'].strip()
    ret += "\n\n"
    return ret


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


for file in sorted(os.listdir(in_dir)):
    if file.startswith('_'):
        continue
    if not file.endswith('.yaml'):
        continue
    in_file = path.join(in_dir, file)
    out_filename = file[:-5].replace('_', '-') + '.rst'
    out_file = path.join(out_dir, out_filename)
    print(f"Making {out_filename}")
    markdown = ''
    with open(in_file) as f:
        category = yaml.load(f, yaml.SafeLoader)
    if category.get('groups'):
        heading_level = 1
        include_heading = False
    else:
        heading_level = 2
        include_heading = True
    with open(out_file, 'w') as f:
        f.write(rst_all(heading_level, category, include_heading=include_heading))
