#!/usr/bin/python3

import staticjinja as sj
import json as jsonlib
import os
import shutil

import addphotos


def clean_build(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)


def main():
    out_dir = '../build'
    # clean_build(out_dir)

    # addphotos.main()

    with open('../config/photos_generated.json') as photos_handle:
        photos_info = jsonlib.load(photos_handle)
        contexts = dict(photos_info=photos_info)
        site_args = dict(searchpath='../src/',
                         outpath=out_dir, env_globals=contexts,
                         staticpaths=["assets/"],
                         )
        site = sj.Site.make_site(**site_args)
        site.render(use_reloader=True)


if __name__ == "__main__":
    main()
