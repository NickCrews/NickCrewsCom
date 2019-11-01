#!/usr/bin/python3

import staticjinja as sj
import json as jsonlib
import os
import shutil
import codecs
import markdown
import re

import addphotos


def clean_build(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)


class MySite(sj.Site):

    STATIC_PATTERNS = [
        '.*\.jpg',
        '.*\.jpeg',
        '.*\.ico',
        '.*\.png',
        '.*\.gif',
    ]

    def is_static(self, filename):
        for pattern in self.STATIC_PATTERNS:
            if re.match(pattern, filename):
                return True
        return False


# def render_md(path):
#     html = None
#     with codecs.open(path, mode="r", encoding="utf-8") as md_file:
#         html = markdown.markdown(md_file.read(), output_format="html5")
#     if html:
#         with codecs.open("some_file.html", "w",
#                          encoding="utf-8",
#                          errors="xmlcharrefreplace") as of:
#             of.write(html)
#
#
# def compile_site():
#     copy_assets()
#     for project in get_projects():
#         render_project(project)
#     for

def get_md_contents(template):
    with codecs.open(template.filename, mode="r", encoding="utf-8") as md_file:
        html = markdown.markdown(md_file.read(), output_format="html5")
        # print("rendered ", html)
        return {'post_content': html}


def render_md(env, template, **kwargs):
    """Render a template as a post."""
    directory, fname = os.path.split(template.name)
    post_title, _ = fname.split(".")
    post_fname = "%s.html" % post_title

    out_dir = os.path.join(env.outpath, directory)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    out = os.path.join(out_dir, post_fname)

    post_template = env.get_template("projects/_post.html")
    post_template.stream(**kwargs).dump(out, encoding="utf-8")


def render_photo(env, template, **kwargs):
    """Render a template as a post."""
    print("rendering photo!")
    # directory, fname = os.path.split(template.name)
    # post_title, _ = fname.split(".")
    # post_fname = "%s.html" % post_title
    #
    # out_dir = os.path.join(env.outpath, directory)
    # if not os.path.exists(out_dir):
    #     os.makedirs(out_dir)
    # out = os.path.join(out_dir, post_fname)
    #
    # post_template = env.get_template("projects/_post.html")
    # post_template.stream(**kwargs).dump(out, encoding="utf-8")


# def upperstring(input):
#     return input.upper()

# env.filters['upperstring'] = upperstring

def render_pass(env, template, **kwargs):
    pass


def get_projects(src_dir):
    projects_dir = os.path.join(src_dir, 'projects')
    for proj_name in os.listdir(projects_dir):
        proj_path = os.path.join(projects_dir, proj_name)
        if not os.path.isdir(proj_path):
            continue
        proj = {}
        proj['name'] = proj_name
        proj['posts'] = []
        for entry_name in os.listdir(proj_path):
            entry_path = os.path.join(proj_path, entry_name)
            if not os.path.isfile(entry_path):
                continue
            post_title, _ = entry_name.split(".")
            post_path = 'projects/' + proj_name + '/' + post_title
            proj['posts'].append(post_path)
        proj['homepage'] = proj['posts'][0]
        yield proj


def main():
    out_dir = '../build'
    # clean_build(out_dir)

    # addphotos.main()

    project_info = get_projects('../src/')

    # render_md('../src/projects/force_sensor/theory.md')

    with open('../config/photos_generated.json') as photos_handle:
        photos_info = jsonlib.load(photos_handle)
        contexts = dict(photos_info=photos_info,
                        project_info=project_info)
        site_args = dict(searchpath='../src/',
                         outpath=out_dir, env_globals=contexts,
                         staticpaths=["assets/"],
                         contexts=[
                             ('.*.md', get_md_contents),
                         ],
                         rules=[
                             ('.*.md', render_md),
                             ('.*.jpg', render_photo),
                             ('.*.DS_Store', render_pass),
                         ],
                         )
        site = MySite.make_site(**site_args)
        site.render(use_reloader=True)


if __name__ == "__main__":
    main()
