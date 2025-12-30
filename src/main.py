import os
from copy_code import remove_code, copy_code
from page_generator import generate_pages_recursive

WORK_DIR = "./"
abs_static = os.path.abspath(os.path.join(WORK_DIR, "static"))
abs_public = os.path.abspath(os.path.join(WORK_DIR, "public"))
abs_content = os.path.abspath(os.path.join(WORK_DIR, "content"))


def main():

    remove_code(abs_public)
    copy_code(abs_static, abs_public)
    generate_pages_recursive(abs_content, "./template.html", abs_public)
    

main()
