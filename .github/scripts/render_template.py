"""Render a Backstage template skeleton the way fetch:template does.

Backstage uses Nunjucks with ${{ }} as the variable delimiter. Jinja2 with the
same delimiter is close enough for CI checks; StrictUndefined makes a typo'd
variable fail the build instead of silently rendering as an empty string.
"""
import pathlib
import shutil
import sys

import jinja2

src, dest = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
values = dict(arg.split("=", 1) for arg in sys.argv[3:])

env = jinja2.Environment(
    variable_start_string="${{",
    variable_end_string="}}",
    keep_trailing_newline=True,
    undefined=jinja2.StrictUndefined,
)


def render(text):
    return env.from_string(text).render(values=values)


for path in sorted(src.rglob("*")):
    if path.is_dir():
        continue
    target = dest / render(str(path.relative_to(src)))
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        target.write_text(render(path.read_text()))
    except UnicodeDecodeError:
        shutil.copy2(path, target)
