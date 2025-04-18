# Repo2LLM

![GitHub last commit](https://img.shields.io/github/last-commit/yuzongmin/Repo2LLM)
[![License](https://img.shields.io/github/license/yuzongmin/Repo2LLM)](https://github.com/yuzongmin/Repo2LLM/blob/main/LICENSE)

## Description

A Python script designed to selectively extract code from a large repository based on configurable rules and format it into a single, structured text file optimized for Large Language Model (LLM) prompts. This helps provide LLMs with relevant codebase context without overwhelming them with unnecessary files.

## Problem Solved

Working with LLMs on codebase-related tasks (like refactoring, analysis, explanation) often requires providing relevant source code as context. Manually navigating a large repository, selecting specific files, copying their contents, and pasting them into a prompt is tedious, time-consuming, and error-prone. This project automates that process.

## How It Works

The tool operates in two conceptual phases:

1. **Filtering:** It traverses your repository starting from a defined root, including only files specified in the `FILTERED_FILE_LIST`.
2. **Formatting:** It takes the list of filtered files, reads their actual content, and compiles it into a single Markdown-formatted file. This output includes a tree visualization of the filtered structure at the beginning, followed by each file's content within language-hinted Markdown code blocks.

## Features

- Filter files based on user-defined lists of paths
- Generates an ASCII tree visualization of the filtered repository structure
- Reads and includes the actual content of filtered files
- Formats output using Markdown, including code blocks with language hints
- Includes clear headers and separators for easy parsing by LLMs (and humans)
- Basic error handling for file reading (e.g., file not found, encoding issues)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yuzongmin/Repo2LLM.git
   cd Repo2LLM
   ```

2. Ensure you have Python 3.6+ installed.

The script uses only standard Python library modules (`os`).

## Usage

1. **Configure the Script:**
   Open the `Repo2llm.py` file in a text editor.

   - Set `REPO_ROOT`: The path to the root of the repository you want to process (e.g., `.` if running the script from within the target repo's root)
   - Set `FILTERED_FILE_LIST`: List of relative file paths you want to include
   - Set `OUTPUT_FILE`: Name of the file where the formatted output will be saved

2. **Run the Script:**
   ```bash
   python Repo2llm.py
   ```

The script will print its progress and indicate when the output file has been generated.

## Output Format

The generated output file uses a structured Markdown format:

```markdown
## Repository Content (Filtered)

[Introductory sentence]

### Filtered Directory Structure:
```

[ASCII tree visualization of included files]

````

--- File Content Below ---

--- File: <relative_path_1> ---
```<language_hint>
[Content of file 1]
````

---

--- File: <relative_path_2> ---

```<language_hint>
[Content of file 2]
```

---

... (blocks for all other filtered files) ...

--- End of Repository Content (Filtered) ---

```

## Configuration Details

Look for the `--- User Configuration ---` section at the top of the `Repo2llm.py` script to set your preferences.

## Potential Future Improvements

* Add command-line arguments for configuration
* Add support for specifying file paths with wildcards or more complex patterns
* Handle very large files by optionally truncating or splitting them
* Add more robust encoding detection or error handling options
* Include file size or line count in the file headers

## Contributing

Contributions are welcome! If you have ideas for improvements or find bugs, please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
