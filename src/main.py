import os
from copy_code import remove_code, copy_code
from page_generator import generate_pages_recursive
from constants import basepath, DOCS, STATIC, CONTENT, TEMPLATE

abs_static = os.path.abspath(os.path.join("./", STATIC))
abs_docs = os.path.abspath(os.path.join("./", DOCS))
base_docs = os.path.abspath(os.path.join(abs_docs, basepath.strip('/')))
abs_content = os.path.abspath(os.path.join("./", CONTENT))
abs_template = os.path.abspath(os.path.join("./", TEMPLATE))

def main():

    remove_code(abs_docs)
    copy_code(abs_static, base_docs)
    generate_pages_recursive(abs_content, abs_template, abs_docs, basepath.strip('/'))
    

main()
