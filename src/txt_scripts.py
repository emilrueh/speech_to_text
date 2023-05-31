import textwrap


def insert_newlines(string, every=64):
    return "\n".join(textwrap.wrap(string, every))


def append_to_or_create_txt_file(input_text, output_file_path):
    # Try to read the current contents of the file
    try:
        with open(output_file_path, "r") as f:
            current_contents = f.read()
    except IOError:
        # If the file doesn't exist, create it by opening it in write mode
        with open(output_file_path, "w") as f:
            f.write(input_text)
            current_contents = ""

    # Append the output to the file only if it's not already present
    if input_text not in current_contents:
        with open(output_file_path, "a") as f:
            if current_contents == "":
                f.write(input_text)
            else:
                # Append a couple of newline characters before the new output
                # to ensure there's some space between it and the previous content
                f.write("\n\n" + input_text)


def open_txt_file(txt_file_path):
    try:
        with open(txt_file_path, "r") as f:
            return f.read()
    except:
        return print(f"Failed to open .txt file at path: {txt_file_path}")
