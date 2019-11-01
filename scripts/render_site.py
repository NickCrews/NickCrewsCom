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

    IGNORED_PATTERNS = [
        '.*info\.json',
        '.*\.DS_Store'
    ]

    def is_static(self, filename):
        for pattern in self.STATIC_PATTERNS:
            if re.match(pattern, filename):
                return True
        return False

    def is_ignored(self, filename):
        for pattern in self.IGNORED_PATTERNS:
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

# def upperstring(input):
#     return input.upper()

# env.filters['upperstring'] = upperstring


def get_project(proj_path):
    print(proj_path)
    _, proj_name = os.path.split(proj_path)

    def path_rel_to_src(path):
        return 'projects/' + proj_name + '/' + path

    proj = {}
    proj['posts'] = []
    for entry_name in os.listdir(proj_path):
        entry_path = os.path.join(proj_path, entry_name)
        if not os.path.isfile(entry_path):
            continue

        if entry_name == 'info.json':
            with open(entry_path) as f:
                info = jsonlib.load(f)
                proj.update(info)

        post_title, extension = entry_name.split(".")
        if extension == 'md':
            proj['posts'].append(path_rel_to_src(post_title))

    proj['homepage'] = proj['posts'][0]
    proj['image'] = path_rel_to_src(proj['image'])
    print(proj)
    return proj


def get_projects(src_dir):
    projects_dir = os.path.join(src_dir, 'projects')
    projects = []
    for proj_name in os.listdir(projects_dir):
        proj_path = os.path.join(projects_dir, proj_name)
        if os.path.isdir(proj_path):
            projects.append(get_project(proj_path))
    return projects


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
                         ],
                         )
        site = MySite.make_site(**site_args)
        site.render(use_reloader=True)


if __name__ == "__main__":
    main()
