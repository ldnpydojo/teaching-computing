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
    """Produce a school report either by selecting randomly from
    preset lists or by accepting a name and a numeric grade. The
    name will be passed through directly; the grade will result
    in one of a set of appropriate pieces of text.

    The parameters can be passed on the command line or passed
    passed to the function when imported.

    eg report.py Tim 3
    """
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
