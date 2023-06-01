import csv
import pandas as pd
import json
import tempfile
import shutil
import os
import textwrap


# CSV
def save_to_csv(data, filename):
    if not data:
        print("No data to save.")
        return

    fieldnames = [
        "Name",
        "Photo",
        "Category",
        "Tags",
        "People",
        "Group Size",
        "Long Description",
        "Summary",
        "Location",
        "Venue",
        "Gmaps link",
        "Date",
        "Time",
        "Price",
        "Link",
        "Keyword",
    ]

    flattened_data = []
    for events in data.values():
        for event_data in events.values():
            # Remove the URL field from the event_data dictionary
            event_data.pop("URL", None)
            flattened_data.append(event_data)

    with open(filename, "w", newline="", encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(flattened_data)


# from CSV function
def load_from_csv(filename):
    df = pd.read_csv(filename)
    return df


def delete_csv_duplicates(file_path, columns_to_compare=None):
    data = pd.read_csv(file_path)

    # Keep one instance of each event with the same name, remove others
    data_no_duplicates = data.drop_duplicates(subset=columns_to_compare, keep="first")

    data_no_duplicates.to_csv(
        f"{file_path.replace('.csv', '')}_no-duplicates.csv", index=False
    )


def manipulate_csv_data(file_path, output_filepath, operations, input_df=None):
    """
    This is how to set parameters:

    operations = [
            # ... other operations
            {'action': 'substring', 'column_name': 'Month', 'start_index': 0, 'end_index': 3},
            {'action': 'uppercase', 'column_name': 'Month'},
            # ... other substring operations
        ]
    """

    if input_df is None:
        df = pd.read_csv(file_path)
    else:
        df = input_df

    if output_filepath == None:
        output_filepath = file_path

    if operations == None:
        return print("No operations specified. Skipping function...")

    # Apply operations
    for operation in operations:
        if operation["action"] == "add_column":
            df[operation["column_name"]] = operation["column_value"]
        elif operation["action"] == "remove_column":
            df.drop(columns=[operation["column_name"]], axis=1, inplace=True)
            if len(df.columns) == 0:
                df.columns = pd.RangeIndex(
                    len(df.columns)
                )  # Reset the columns data type
        elif operation["action"] == "lowercase":
            df[operation["column_name"]] = (
                df[operation["column_name"]].astype(str).str.lower()
            )
        elif operation["action"] == "uppercase":
            df[operation["column_name"]] = (
                df[operation["column_name"]].astype(str).str.upper()
            )
        elif operation["action"] == "titlecase":
            df[operation["column_name"]] = (
                df[operation["column_name"]].astype(str).str.title()
            )
        elif operation["action"] == "split":
            df[operation["new_column_name"]] = (
                df[operation["column_name"]]
                .astype(str)
                .str.split(pat=operation["delimiter"])
            )

        elif operation["action"] == "substring":
            start_index = operation["start_index"]
            end_index = operation["end_index"]
            new_column_name = operation.get("new_column_name", None)

            if new_column_name:
                df[new_column_name] = (
                    df[operation["column_name"]].astype(str).str[start_index:end_index]
                )
            else:
                df[operation["column_name"]] = (
                    df[operation["column_name"]].astype(str).str[start_index:end_index]
                )

        elif operation["action"] == "keyword_filter":
            keyword = operation["keyword"]
            deleted_rows = df[
                df[operation["column_name"]].str.contains(keyword, case=False)
            ]
            print(deleted_rows.iloc[:, operation["column_index"]])
            df = df[~df[operation["column_name"]].str.contains(keyword, case=False)]

        else:
            raise ValueError(f"Invalid action '{operation['action']}'")

    df.to_csv(output_filepath, index=False)

    return df


# JSON
def json_read(json_filename):
    # Specify the filename of the JSON backup file
    # Load JSON data from the file
    with open(json_filename, "r") as file:
        json_data = file.read()

    # Convert the JSON data back into the dictionary
    json_dict = json.loads(json_data)

    return json_dict


def json_save(data, filename):
    # backup
    json_data = json.dumps(data)
    # Save the JSON string to a file
    with open(filename, "w") as file:
        file.write(json_data)


# TXT
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


# BACKUP
def backup_data(input_data, backup_directory, input_name=None):
    # Determine the file extension
    if isinstance(input_data, pd.DataFrame):
        file_extension = ".csv"
    elif isinstance(input_data, str) and input_data.endswith((".csv", ".txt", ".json")):
        file_extension = os.path.splitext(input_data)[1]
    elif isinstance(input_data, dict) or (
        isinstance(input_data, str) and input_data.endswith(".json")
    ):
        file_extension = ".json"
    elif isinstance(input_data, str):
        file_extension = ".txt"
    else:
        raise ValueError("Unsupported data type")

    # Create a temporary file with the desired file name
    with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp_file:
        # Save the input data to the temporary file
        if isinstance(input_data, pd.DataFrame):
            input_data.to_csv(temp_file.name, index=False)
        elif isinstance(input_data, str) and input_data.endswith(
            (".csv", ".txt", ".json")
        ):
            with open(input_data, "r") as data_file:
                temp_file.write(data_file.read())
        elif isinstance(input_data, dict):
            json.dump(input_data, temp_file)
        elif isinstance(input_data, str) and input_data.endswith(".json"):
            with open(input_data, "r") as data_file:
                json_data = json.load(data_file)
            with open(temp_file.name, "w") as temp_json_file:
                json.dump(json_data, temp_json_file)
        elif isinstance(input_data, str):
            temp_file.write(input_data.encode())

        # Determine the backup file name
        if input_name is not None:
            backup_base_name = input_name + "_backup"
        elif isinstance(input_data, str):
            backup_base_name = (
                os.path.basename(input_data)[: -len(file_extension)] + "_backup"
            )
        else:
            raise ValueError(
                "Input name is required for DataFrame or dictionary input_data"
            )

        # Append a number to the backup file name if it already exists
        counter = 1
        backup_file_name = backup_base_name + file_extension
        while os.path.exists(os.path.join(backup_directory, backup_file_name)):
            backup_file_name = f"{backup_base_name}_{counter}{file_extension}"
            counter += 1

        # Copy the temporary file to the backup directory
        backup_file_path = os.path.join(backup_directory, backup_file_name)
        shutil.copy(temp_file.name, backup_file_path)

    # Remove the temporary file
    os.unlink(temp_file.name)

    return input_data
