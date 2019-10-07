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


def cap(s):
    """Capitalize the first letter of a string, preserving the rest."""
    return s[0].upper() + s[1:]


def md_bullet(bullet_level, data, *, link_file='', exclude_header=False):
    ret = "  " * (bullet_level - 1) + "- "
    if exclude_header:
        link = link_file
    else:
        link = f"{link_file}#{data['name'].replace(' ', '-')}"
    link_text = f"**{cap(data['name'])}**"
    if link:
        ret += f"[{link_text}]({link})"
    else:
        ret += link_text
    ret += " - "
    ret += f"_{data['brief']}_"
    ret += "\n"
    return ret


def md_section(header_level, data, *, title_suffix=''):
    ret = "#" * header_level + " "
    ret += cap(data['name']) + title_suffix
    ret += "\n\n"
    ret += data['full'].strip()
    values = data.get('values')
    if values:
        ret += "\n\n There are " + str(len(values)) + " " + cap(data['name']) + "s:"
    ret += "\n\n"
    return ret


def md_all(header_level, data, **kwargs):
    ret = md_section(header_level, data, **kwargs)
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
    if inners:
        for inner in inners:
            ret += md_bullet(1, inner)
            for value in inner.get('values', []):
                ret += md_bullet(2, value)
        for inner in inners:
            ret += md_all(header_level + 1, inner)
    return ret


index_md = """
# Morphological categories
""".strip() + '\n\n'

for file in sorted(os.listdir(in_dir)):
    if file.startswith('_'):
        continue
    if not file.endswith('.yaml'):
        continue
    in_file = path.join(in_dir, file)
    out_filename = file[:-5] + '.md'
    out_file = path.join(out_dir, out_filename)
    print(f"Making {out_filename}")
    markdown = ''
    with open(in_file) as f:
        category = yaml.load(f, yaml.SafeLoader)
    index_md += md_bullet(1, category, link_file=out_filename, exclude_header=True)
    with open(out_file, 'w') as f:
        f.write(md_all(1, category))
        # f.write(md_section(1, category))
        # if category.get('groups'):
        #     category_values_dict = {}
        #     for category_value in category['values']:
        #         category_values_dict[category_value['abbr']] = category_value
        #     for group in category['groups']:
        #         f.write(md_section(2, group, title_suffix=f" {category['name']}s"))
        #         for member in group['members']:
        #             category_value = category_values_dict[member]
        #             f.write(md_section(3, category_value))
        # else:
        #     for category_value in category['values']:
        #         f.write(md_section(2, category_value))

with open(path.join(out_dir, 'index.md'), 'w') as f:
    f.write(index_md)
