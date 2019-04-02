#!/usr/bin/env bash
# convert files using inkscape
input_dir=$1
output_dir=$2

function svg_to_png () {
    path=$1
    echo $path
    file=${path##*/}
    base=${file%%.*}
    [ -e $path ] && inkscape $path -d 24 -e $output_dir/preview-${base}.png
}
for f in $input_dir/*.svg
do
    svg_to_png $f
done
