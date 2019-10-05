#!/usr/bin/env bash
# convert files using inkscape
input_dir=$1
output_dir=$2
# produce png images
function export_png() {
    path=$1
    echo $path
    file=${path##*/}
    base=${file%%.*}
    [ -e $path ] && inkscape $path -d 24 -e $output_dir/preview-${base}.png
}
# produce svg images
function export_svg () {
    path=$1
    echo $path
    file=${path##*/}
    base=${file%%.*}
    [ -e $path ] && inkscape $path -d 24 -l $output_dir/preview-${base}.svg
}
for f in $input_dir/*.svg
do
    export_png $f
    export_svg $f
done
