#!/usr/bin/env python3

# Import modules for dealing with the filesystem etc.
from os import path
from pathlib import Path
import os
import sys

# Check for yaml dependency.
try:
    import yaml
except ModuleNotFoundError:
    print("Cannot run without 'yaml' package")

# Check for jinja2 dependency.
try:
    from jinja2 import Environment, FileSystemLoader
except ModuleNotFoundError:
    print("Cannot run without 'jinja2' package")

# Check that input & output directories were given.
try:
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
except IndexError:
    print("Supply an input directory and an output directory:")
    print(sys.argv[0] + " <in_dir> <out_dir>")
# look for a `templates` directory
template_dir = os.getcwd() + "/templates"
print("Template dir is: " + template_dir)
# Set up template environment
env = Environment(
    loader=FileSystemLoader(template_dir)
)
#
template = env.get_template('morpho.rst')

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
    # if category.get('groups'):
    #     heading_level = 1
    #     include_heading = False
    # else:
    #     heading_level = 2
    #     include_heading = True
    # Write the output.
    with open(out_file, 'w') as f:
        # f.write(rst_all(heading_level, category, include_heading=include_heading))
        f.write(template.render(category))
