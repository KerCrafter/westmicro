#!/usr/bin/env python3
import argparse
import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def render_templates(content_dir, templates_dir, out_dir):
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )

    os.makedirs(out_dir, exist_ok=True)

    site = load_json(os.path.join(content_dir, "site.json"))
    services = load_json(os.path.join(content_dir, "services.json"))

    if load_dotenv:
        env_path = os.path.join(os.getcwd(), ".env")
        if os.path.exists(env_path):
            load_dotenv(env_path)

    formspree_action = None
    fs_id = os.environ.get("FORMSPREE_ID")
    if fs_id:
        formspree_action = f"https://formspree.io/f/{fs_id}"

    index_tpl = env.get_template("index.html")
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_tpl.render(site=site, services=services))

    contact_tpl = env.get_template("contact.html")
    with open(os.path.join(out_dir, "contact.html"), "w", encoding="utf-8") as f:
        f.write(contact_tpl.render(site=site, formspree_action=formspree_action))

    static_src = os.path.join(templates_dir, "static")
    static_dst = os.path.join(out_dir, "static")
    if os.path.isdir(static_src):
        import shutil

        if os.path.exists(static_dst):
            shutil.rmtree(static_dst)
        shutil.copytree(static_src, static_dst)



def main():
    p = argparse.ArgumentParser()
    p.add_argument("--content", default="content")
    p.add_argument("--templates", default="templates")
    p.add_argument("--output", default="build")
    args = p.parse_args()

    render_templates(args.content, args.templates, args.output)


if __name__ == "__main__":
    main()
