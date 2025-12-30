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

def copy_code(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_code(from_path, dest_path)
