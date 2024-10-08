import yaml
import os
import sys
from datetime import datetime, timedelta
import re


def read_yaml(file_path):
    # file_path='./config.yaml'
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


# pass the filename and content, then write to the local
def write_to_file(file_name: str, content: str):
    with open(file_name, "a") as file:
        file.write(content)

def write_to_file_overwrite(file_name: str, content: str):
    with open(file_name, "w") as file:
        file.write(content)


def str_to_role(str_role_list):
    """
    extract the content within [ ] and return a list
    """
    f = re.findall("[\[](.*?)[\]]", str_role_list)
    for role_profile in f:
        try:
            print(role_profile)
        except:
            print("Error: " + role_profile)
    return f
