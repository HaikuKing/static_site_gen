import re
import os
from markdown_to_blocks import markdown_to_html_node

def extract_title(markdown):
    pattern = r'^(#{1})\s+(.*)$'
    match = re.search(pattern, markdown, re.MULTILINE)
    if match:
        full_title = match.group()
        return full_title.lstrip("#").strip()
    else:
        return "Untitled"

def write_file(working_directory, file_path, content):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Error Handling
    
    if not (abs_file_path.startswith(os.path.abspath(working_directory) + os.sep) or abs_file_path == os.path.abspath(working_directory)):
        return f'WriteError: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
    
        with open(abs_file_path, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'WriteError: {e}'

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    abs_from = os.path.abspath(os.path.join("./", from_path))
    abs_temp = os.path.abspath(os.path.join("./", template_path))

    with open(abs_from, "r") as f:
        markdown = f.read()

    with open(abs_temp, "r") as f:
        template = f.read()
    
    title = extract_title(markdown)
    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    between_temp = template.replace("{{ Title }}", f"{title}")
    new_template = between_temp.replace("{{ Content }}", f"{html_string}")
    new_href = new_template.replace('href="/', f'href="{base_path.rstrip('/')}{base_path}')
    new_src = new_href.replace('src="/', f'src="{base_path}')
    write_file("./", dest_path, new_src)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    abs_cont = os.path.abspath(dir_path_content)
    abs_temp = os.path.abspath(template_path)
    abs_dest_dir = os.path.abspath(dest_dir_path)

    listed = os.listdir(abs_cont)
    for path in listed:
        new_path = path.replace(".md", ".html")
        abs_path = os.path.abspath(os.path.join(dir_path_content, path))
        abs_dest = os.path.abspath(os.path.join(abs_dest_dir, path))
        abs_new_dest = os.path.abspath(os.path.join(abs_dest_dir, new_path))

        if os.path.isfile(abs_path):
            generate_page(abs_path, abs_temp, abs_new_dest, base_path)

        elif os.path.isdir(abs_path):
            os.mkdir(abs_dest)
            generate_pages_recursive(abs_path, abs_temp, abs_dest, base_path)

        else:
            print(f"GenError: {abs_path} is not a file or a directory")
