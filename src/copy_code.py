import os, shutil
from constants import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    # Error Handling
    if not (abs_file_path.startswith(abs_working + os.sep) or abs_file_path == abs_working):
        return f'GFCError: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'GFCError: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_file_path, "r") as file:
            file_content_string = file.read(MAX_CHARS + 1) # reading one extra char to check truncation
            if len(file_content_string) > MAX_CHARS:
                file_content_string = file_content_string[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return f"GFCError: {e}"
    
def get_files_info(working_directory, directory="."):
    abs_working = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(abs_working, directory))

    if not (abs_directory.startswith(abs_working + os.sep) or abs_directory == abs_working):
        raise Exception(f'GFIError: Cannot list "{abs_directory}" as it is outside the permitted working directory')
    if not os.path.isdir(abs_directory):
        raise Exception(f'GFIError: "{abs_directory}" is not a directory')

    lines = []
    for file in os.listdir(abs_directory):
        file_entry = os.path.join(abs_directory, file)
        lines.append(f'{file_entry}')
    return "\n".join(lines)

def remove_code(abs_docs):

    try:
        docs_files = get_files_info(abs_docs)
    except Exception as e:
        print(e)
        return

    if not docs_files:
        print(f"{abs_docs} directory empty")
        pass
    else:
        shutil.rmtree(abs_docs)
        os.mkdir(abs_docs)
        print(f"Removed things from {abs_docs}")

def copy_code(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok=True)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_code(from_path, dest_path)
