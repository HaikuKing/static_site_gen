import os, shutil

MAX_CHARS = 10000
WORK_DIR = "./"
PUBLIC = "public"
STATIC = "static"



def get_file_content(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    # Error Handling
    if not (abs_file_path.startswith(abs_working + os.sep) or abs_file_path == abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_file_path, "r") as file:
            file_content_string = file.read(MAX_CHARS + 1) # reading one extra char to check truncation
            if len(file_content_string) > MAX_CHARS:
                file_content_string = file_content_string[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return f"Error: {e}"
    
def get_files_info(working_directory, directory="."):
    abs_working = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(abs_working, directory))

    if not (abs_directory.startswith(abs_working + os.sep) or abs_directory == abs_working):
        raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(abs_directory):
        raise Exception(f'Error: "{directory}" is not a directory')


    lines = []
    for file in os.listdir(abs_directory):
        file_entry = os.path.join(abs_directory, file)
        lines.append(f'{file_entry}')
    return "\n".join(lines)


def remove_code(abs_public):

    try:
        public_files = get_files_info(abs_public)
    except Exception as e:
        print(e)
        return

    if not public_files:
        print("Public directory empty")
        pass
    else:
        shutil.rmtree(abs_public)
        os.mkdir(abs_public)
        print(f"Removed things from {abs_public}")

def copy_code(working_directory, abs_public):
    abs_working = os.path.abspath(working_directory)
    
    try:
        files = get_files_info(abs_working)
    except Exception as e:
        print(e)
        return
    
    new_files = files.split("\n")
    
    for file in new_files:
        abs_path = os.path.abspath(file)
        rel_path = os.path.relpath(abs_path, abs_working)
        if os.path.isfile(abs_path):
            shutil.copy(abs_path, abs_public)
            print(f"{rel_path} copied to {abs_public}")
        elif os.path.isdir(abs_path):
            new_dest = os.path.abspath(os.path.join(abs_public, rel_path))
            os.mkdir(new_dest)
            copy_code(abs_path, new_dest)
