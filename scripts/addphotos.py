#!/usr/local/bin/python3

import argparse
import os
import json as jsonlib
import sys

import PIL
from PIL import Image

picture_suffix = '.jpg'
LARGE_SIZE = 1500
THUMB_SIZE = 500


def clean(args):
    print('cleaning!')
    for suffix in ['.thumb', '.large']:
        for file in os.listdir(args.indir):
            if file.endswith(suffix):
                os.remove(os.path.join(args.indir, file))


def process_photo(args, basename):
    print("processing " + basename)
    in_path = os.path.join(args.indir, basename)
    full_img = Image.open(in_path)

    # if not os.path.exists(args.outdir):
    os.makedirs(args.outdir, exist_ok=True)

    thumb = full_img.copy()
    thumb.thumbnail((args.thumb_size, args.thumb_size))
    thumb_path = os.path.join(args.outdir, basename + '.thumb')
    thumb.save(thumb_path, "JPEG")

    large = full_img.copy()
    large.thumbnail((args.large_size, args.large_size))
    large_path = os.path.join(args.outdir, basename + '.large')
    large.save(large_path, "JPEG")

    info = dict(full=basename, width=full_img.width, height=full_img.height,
                thumb=basename + '.thumb', thumb_width=thumb.width, thumb_height=thumb.height,
                large=basename + '.large', large_width=large.width, large_height=large.height,
                title=basename)
    info['all_info_json'] = jsonlib.dumps(info)
    return info


def main(args=None):
    if not args:
        args = []

    parser = argparse.ArgumentParser(prog="addphotos.py")

    parser.add_argument('-i', '--indir', metavar='i', default='../src/assets/img/photos/', type=str,
                        help='Input directory')

    parser.add_argument('-o', '--outdir', metavar='o', type=str,
                        default='../build/assets/img/photos', help='Output directory')

    parser.add_argument('-t', '--thumb_size', type=int,
                        default=THUMB_SIZE, help='Desired max dimension of thumbnails')
    parser.add_argument('-l', '--large_size', type=int,
                        default=LARGE_SIZE, help='Desired max dimension of fullsize images')
    parser.add_argument('-c', action='store_true', help='Clean output images')

    args = parser.parse_args(args)

    if args.c:
        clean(args)
        exit(0)

    photo_json = []

    for file in os.listdir(args.indir):
        if file.endswith(picture_suffix):
            photo_json.append(process_photo(args, file))

    print(jsonlib.dumps(photo_json, sort_keys=True, indent=4))


if __name__ == '__main__':
    main(sys.argv[1:])
