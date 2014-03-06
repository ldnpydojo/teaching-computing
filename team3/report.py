#!python3
import os, sys
import string
import random

import options

template_filepath = "report.template"
output_filepath = "report.html"

def render(template, **kwargs):
    print("kwargs=", kwargs)
    with open(output_filepath, "w") as f:
        f.write(template.safe_substitute(**kwargs))

def report(name, subject, how_well):
    with open(template_filepath) as f:
        template = string.Template(f.read())
    render(template, name=name, subject=subject, how_well=how_well)
    os.startfile(output_filepath)

def main():
    name = random.choice(options.names)
    subject = random.choice(options.subjects)
    how_well = random.choice(options.grade_adjective)
    adjective = random.choice(options.grade_adjective[how_well])
    report(name, subject, how_well)

if __name__ == '__main__':
    main(*sys.argv[1:])
