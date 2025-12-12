import os
from copy_code import remove_code, copy_code

WORK_DIR = "./"
abs_static = os.path.abspath(os.path.join(WORK_DIR, "static"))
abs_public = os.path.abspath(os.path.join(WORK_DIR, "public"))


def main():

    remove_code(abs_public)
    copy_code(abs_static, abs_public)

main()
