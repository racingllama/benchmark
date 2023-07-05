"""Utility functions."""

import os
import re


def parse_directory(directory):
    """Parse a directory of models.

    Args:
        directory (str): Directory of models.

    Returns:
        list: List of models.
    """
    models = []

    for file in os.listdir(directory):
        if file.endswith(".bin"):
            try:
                tmp_name = re.split(r"\d+[bB]", file.split(".")[0])
                name = tmp_name[0].replace("-", " ").strip()
                if len(tmp_name) != 1 and tmp_name[1] != "":
                    name += f" ({tmp_name[1].replace('-', ' ').strip()})"
                quant = re.findall(r"q\d+[A-Za-z_0-9]*", file)[0]
                parameters = re.findall(r"\d+[bB]", file)[0]
                models.append(
                    {
                        "name": name,
                        "path": os.path.join(directory, file),
                        "quant": quant,
                        "parameters": parameters.upper(),
                    }
                )
            except IndexError:
                print(f"Error parsing {file}")
                continue
    return models
