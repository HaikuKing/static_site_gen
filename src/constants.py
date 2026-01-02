import sys

MAX_CHARS = 10000
DOCS = "docs"
STATIC = "static"
CONTENT = "content"
TEMPLATE = "template.html"


if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"
