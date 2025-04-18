import os

# --- User Configuration ---

# Define the root of your repository. Use '.' for the current directory
# where you run the script, or provide a specific path.
REPO_ROOT = '.'

# Define the list of filtered relative file paths.
# This list should contain all the files you want to include in the output.
# Example:
# FILTERED_FILE_LIST = [
#     'src/main.py',
#     'src/utils/helper.py',
#     'tests/test_main.py'
# ]
FILTERED_FILE_LIST = []

# Define the name of the output text file where the formatted content will be written.
# Example: 'formatted_code_context.md'
OUTPUT_FILE = 'formatted_code_context.md'

# --- Helper Functions ---

def build_tree_structure_dict(paths):
    """Builds a nested dictionary representing the directory tree from a list of paths."""
    root = {}
    for path in paths:
        parts = path.split(os.sep)
        current_level = root
        for i, part in enumerate(parts):
            if i == len(parts) - 1: # It's a file
                current_level[part] = None # Use None to mark files
            else: # It's a directory
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
    return root

def tree_dict_to_string(tree_dict, indent=""):
    """Converts the nested dictionary tree representation to an ASCII string."""
    lines = []
    items = sorted(list(tree_dict.keys()))

    for i, item in enumerate(items):
        is_last = (i == len(items) - 1)
        branch = "└── " if is_last else "├── "
        item_path = indent + branch + item

        if isinstance(tree_dict[item], dict): # It's a directory
            lines.append(item_path + "/") # Append / for directories
            next_indent = indent + ("    " if is_last else "│   ")
            lines.extend(tree_dict_to_string(tree_dict[item], next_indent).splitlines())
        else: # It's a file (value is None)
            lines.append(item_path)

    return "\n".join(lines)

def generate_filtered_tree_string(filtered_paths):
    """Generates the complete ASCII tree string for the filtered paths starting from './'."""
    if not filtered_paths:
        return "./\n(No filtered files)"

    root_contents = build_tree_structure_dict(filtered_paths)

    tree_lines = ["./"]
    top_level_items = sorted(list(root_contents.keys()))

    for i, item in enumerate(top_level_items):
        is_last = (i == len(top_level_items) - 1)
        branch = "└── " if is_last else "├── "
        next_indent = "    " if is_last else "│   "

        if root_contents[item] is None: # Direct file under root
             tree_lines.append(branch + item)
        else: # Directory under root
             tree_lines.append(branch + item + "/")
             tree_lines.extend(tree_dict_to_string(root_contents[item], next_indent).splitlines())

    return "\n".join(tree_lines)

def get_language_hint(file_path):
    """Determines a language hint based on file extension."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    lang_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.html': 'html',
        '.css': 'css',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.md': 'markdown',
        '.sh': 'bash',
        '.c': 'c',
        '.cpp': 'cpp',
        '.h': 'c',
        '.hpp': 'cpp',
        '.java': 'java',
        '.go': 'go',
        '.rs': 'rust',
        '.txt': 'text',
    }

    return lang_map.get(ext, 'text')

def generate_llm_formatted_output(repo_root, filtered_paths, output_file):
    """
    Generates the formatted output by reading actual file content
    and writes it to a file.
    """
    if not filtered_paths:
        print("No filtered files to process.")
        with open(output_file, 'w', encoding='utf-8') as f:
             f.write("## Repository Content (Filtered)\n\nNo files matched the filtering criteria.")
        return

    print(f"Generating formatted output to '{output_file}' by reading files from '{repo_root}'...")

    sorted_filtered_paths = sorted(filtered_paths)
    tree_string = generate_filtered_tree_string(sorted_filtered_paths)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("## Repository Content (Filtered)\n\n")
        f.write("This section provides a filtered view of the repository structure and the content of the included files.\n\n")

        f.write("### Filtered Directory Structure:\n")
        f.write("```\n")
        f.write(tree_string)
        f.write("\n```\n\n")

        f.write("--- File Content Below ---\n\n")

        for relative_path in sorted_filtered_paths:
            full_path = os.path.join(repo_root, relative_path)

            try:
                with open(full_path, 'r', encoding='utf-8') as infile:
                    file_content = infile.read()

                f.write(f"--- File: {relative_path} ---\n")

                lang_hint = get_language_hint(relative_path)
                f.write(f"```{lang_hint}\n")
                f.write(file_content)
                f.write("```\n")

                f.write("---\n\n")

            except FileNotFoundError:
                print(f"Warning: File not found, skipping: {full_path}")
                f.write(f"--- File: {relative_path} ---\n")
                f.write("```text\n")
                f.write(f"# ERROR: File not found at {full_path}\n")
                f.write("```\n")
                f.write("---\n\n")

            except UnicodeDecodeError:
                print(f"Warning: Could not decode file, skipping content: {full_path}")
                f.write(f"--- File: {relative_path} ---\n")
                f.write("```text\n")
                f.write(f"# ERROR: Could not read this file due to encoding issues.\n")
                f.write(f"# Path: {full_path}\n")
                f.write(f"# Please check the file encoding (expected utf-8).\n")
                f.write("```\n")
                f.write("---\n\n")

            except Exception as e:
                print(f"Warning: An unexpected error occurred reading file {full_path}: {e}")
                f.write(f"--- File: {relative_path} ---\n")
                f.write("```text\n")
                f.write(f"# ERROR: An unexpected error occurred while reading this file.\n")
                f.write(f"# Path: {full_path}\n")
                f.write(f"# Error: {e}\n")
                f.write("```\n")
                f.write("---\n\n")

        f.write("--- End of Repository Content (Filtered) ---\n")

    print("Formatted output generated successfully.")

# --- Main Execution Block ---
if __name__ == "__main__":
    output_dir = os.path.dirname(OUTPUT_FILE)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    generate_llm_formatted_output(REPO_ROOT, FILTERED_FILE_LIST, OUTPUT_FILE) 