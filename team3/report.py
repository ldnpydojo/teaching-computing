#!python3
import os, sys
import string
import random

import options

template_filepath = "report.template"
output_filepath = "report.html"

def render(template, **kwargs):
    with open(output_filepath, "w") as f:
        f.write(template.safe_substitute(**kwargs))

def report(name, subject, how_well, silly_excuse):
    with open(template_filepath) as f:
        template = string.Template(f.read())
    render(template, name=name, subject=subject, how_well=how_well, silly_excuse=silly_excuse)
    os.startfile(output_filepath)

def main(name=None, grade=None):
    name = name or random.choice(options.names)
    subject = random.choice(options.subjects)
    if grade is not None:
        grade = int(grade)
        adjective = random.choice(options.grade_adjective[grade])
    else:
        how_well = random.choice(list(options.grade_adjective))
        adjective = random.choice(list(options.grade_adjective[how_well]))

    n_silly_excuse = random.choice(list(options.silly_excuse))
    silly_excuse = random.choice(options.silly_excuse[n_silly_excuse])
    report(name, subject, adjective, silly_excuse)

if __name__ == '__main__':
    main(*sys.argv[1:])
