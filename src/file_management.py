import json
import os.path
import pickle
from datetime import datetime


def save_json(
    content,
    file_path,
    file_name,
    file_extension=".json",
    add_date_prefix=True,
    date_prefix_format="%Y%m%d%H%M%S",
):

    file_path = generate_file_path(
        file_path, file_name, file_extension, add_date_prefix, date_prefix_format
    )

    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(content, json_file, ensure_ascii=False, indent=4)

    return file_path


def generate_file_path(
    file_path,
    file_name,
    extension,
    add_date_prefix=True,
    date_prefix_format="%Y%m%d%H%M%S",
):
    if add_date_prefix:
        timestamp = datetime.now().strftime(date_prefix_format)
        file_path = os.path.join(file_path, f"{timestamp}_{file_name}{extension}")
    else:
        file_path = os.path.join(file_path, f"{file_name}{extension}")
    return file_path


def load_json(file_path):
    with open(file_path, encoding="utf-8") as json_file:
        json_data = json.load(json_file)
        # Si c'est une chaîne, essayer de la parser à nouveau
        if isinstance(json_data, str):
            try:
                json_data = json.loads(json_data)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON string: {json_data}")
        return json_data


def save_pickle(
    content,
    file_path,
    file_name,
    file_extension=".pkl",
    add_date_prefix=True,
    date_prefix_format="%Y%m%d%H%M%S",
):

    file_path = generate_file_path(
        file_path, file_name, file_extension, add_date_prefix, date_prefix_format
    )

    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(file_path, "wb") as f:
        pickle.dump(content, f)

    return file_path


def load_pickle(file_path):
    with open(file_path, "rb") as f:
        loaded_data = pickle.load(f)
        return loaded_data


def get_last_generated_file_path(
    file_path,
    file_name,
    file_extension,
    add_date_prefix=True,
    date_prefix_format="%Y%m%d%H%M%S",
):
    file_paths = _list_generated_file_paths(
        file_path, file_name, file_extension, add_date_prefix, date_prefix_format
    )
    if file_paths:
        return file_paths[0]  # Return the first (latest) file path
    else:
        return None


def get_two_lasts_generated_file_path(
    file_path,
    file_name,
    file_extension,
    add_date_prefix=True,
    date_prefix_format="%Y%m%d%H%M%S",
):
    file_paths = _list_generated_file_paths(
        file_path, file_name, file_extension, add_date_prefix, date_prefix_format
    )
    if file_paths:
        if len(file_paths) == 1:
            return file_paths[0]

        return file_paths[0], file_paths[1]  # Return the first (latest) file path
    else:
        return None


def _list_generated_file_paths(
    file_path,
    file_name,
    file_extension,
    add_date_prefix=True,
    date_prefix_format="%Y%m%d%H%M%S",
):
    file_paths = []

    # Check if directory exists
    if not os.path.exists(file_path):
        return file_paths

    for file in os.listdir(file_path):
        if file.endswith(f"{file_name}{file_extension}"):
            file_paths.append(os.path.join(file_path, file))
    if add_date_prefix:
        file_paths.sort(
            key=lambda x: _get_file_creation_time(x, date_prefix_format), reverse=True
        )
    else:
        file_paths.sort(key=os.path.getctime, reverse=True)
    return file_paths


def _get_file_creation_time(file_path, date_prefix_format):
    file_name = os.path.basename(file_path)
    date_string = file_name.split("_", 1)[0]  # Extract date prefix from file name
    return datetime.strptime(date_string, date_prefix_format)
